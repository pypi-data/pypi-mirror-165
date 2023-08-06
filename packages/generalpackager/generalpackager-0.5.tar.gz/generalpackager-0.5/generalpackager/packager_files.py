
import json

from generalfile import Path
from generallibrary import CodeLine, Markdown, Date, deco_cache, Timer, Log


class GenerateFile:
    """ Handle generation of files. """
    def __init__(self, path, text_func, packager, aesthetic, overwrite=True):
        """ :param generalpackager.Packager packager: """
        self.text_func = text_func
        self.packager = packager
        self.aesthetic = aesthetic
        self.overwrite = overwrite

        Log().debug(f"Creating {text_func.__name__} handler for {packager.name} with path {packager.path}")

        self.relative_path = path.relative(base=packager.path)
        self.path = packager.path / self.relative_path  # HERE ** This doesn't work if Packager's path is None

    def generate(self):
        """ Generate actual file. """
        if self.overwrite or not self.path.exists():
            self.path.text.write(f"{self.text_func()}\n", overwrite=self.overwrite)

    def __str__(self):
        return f"<GenerateFile: {self.packager.name} - {self.relative_path}>"


class _PackagerFiles:
    """ Generates setup, license and gitexclude.
        Only changed non-aesthetic files can trigger a version bump and publish. """
    extra_aesthetic = "randomtesting.py",  # "licenses"
    extra_non_aesthetic = tuple()

    _todo_header = "Todo"

    @property
    @deco_cache()
    def files(self):
        """ Todo: Watermark generated files to prevent mistake of thinking you can modify them directly.
            :param generalpackager.Packager self: """
        files = [
            GenerateFile(self.localrepo.get_git_exclude_path(), self.generate_git_exclude, self, aesthetic=True),
            GenerateFile(self.localrepo.get_license_path(), self.generate_license, self, aesthetic=True),
            GenerateFile(self.localrepo.get_workflow_path(), self.generate_workflow, self, aesthetic=True),
            GenerateFile(self.localrepo.get_readme_path(), self.generate_readme, self, aesthetic=True),
            GenerateFile(self.localrepo.get_generate_path(), self.generate_generate, self, aesthetic=True),
        ]

        if self.is_python():
            files.extend([
                GenerateFile(self.localrepo.get_setup_path(), self.generate_setup, self, aesthetic=False),
                GenerateFile(self.localrepo.get_manifest_path(), self.generate_manifest, self, aesthetic=False),
                GenerateFile(self.localrepo.get_init_path(), self.generate_init, self, aesthetic=False, overwrite=False),
                GenerateFile(self.localrepo.get_randomtesting_path(), self.generate_randomtesting, self, aesthetic=True, overwrite=False),
                GenerateFile(self.localrepo.get_test_template_path(), self.generate_test_python, self, aesthetic=False, overwrite=False),
            ])

        elif self.is_node():
            files.extend([
                GenerateFile(self.localrepo.get_npm_ignore_path(), self.generate_npm_ignore, self, aesthetic=True),
                GenerateFile(self.localrepo.get_index_js_path(), self.generate_index_js, self, aesthetic=False, overwrite=False),
                GenerateFile(self.localrepo.get_test_js_path(), self.generate_test_node, self, aesthetic=False, overwrite=False),
                GenerateFile(self.localrepo.get_package_json_path(), self.generate_package_json, self, aesthetic=False),
            ])

        return files

    @deco_cache()
    def all_files_by_relative_path(self):
        """ :param generalpackager.Packager self: """
        return {file.relative_path: file for file in self.files}

    def file_by_relative_path(self, path):
        """ :param generalpackager.Packager self:
            :param Path or str path:
            :rtype: GenerateFile """
        path = Path(path)
        try:
            return self.all_files_by_relative_path()[path.relative(base=self.path)]
        except KeyError:
            return None

    @property
    @deco_cache()
    def file_secret_readme(self):
        """ :param generalpackager.Packager self: """
        # Organization secret name is .github, user secret name is user
        if self.name == ".github":
            secret_readme_path = self.localrepo.get_org_readme_path()
        else:
            secret_readme_path = self.localrepo.get_readme_path()

        return GenerateFile(secret_readme_path, self.generate_personal_readme, self, aesthetic=True)

    def get_new_packager(self):
        """ Todo: Generalize get_new_packager which calls recycle_clear on all attributes.

            :param generalpackager.Packager self: """
        self.recycle_clear()
        self.localrepo.recycle_clear()
        self.localmodule.recycle_clear()
        self.github.recycle_clear()
        self.pypi.recycle_clear()
        return type(self)(self.name)

    @classmethod
    def create_blank_locally_python(cls, path, install=True):
        """ Create a new general package locally only.

            :param generalpackager.Packager or Any cls:
            :param Path or str path:
            :param install: Whether to pip install. """
        path = Path(path)
        assert path.empty()
        packager = cls(name=path.name(), path=path, target=cls.Targets.python)

        packager.localrepo.metadata.write_config()
        packager.generate_localfiles()

        if install:
            packager.localrepo.pip_install_editable()

        new_self = packager.get_new_packager()  # Reset caches to get updated files
        new_self.generate_localfiles()

    def relative_path_is_aesthetic(self, relative_path):
        """ Relative to package path. False if not defined as a GenerateFile instance.

            :param generalpackager.Packager self:
            :param Path or str relative_path: """
        relative_path = Path(relative_path).relative(self.path)
        aesthetic_attr = getattr(self.all_files_by_relative_path().get(relative_path, None), "aesthetic", None)
        if aesthetic_attr is None:
            if relative_path.match(*self.extra_aesthetic):
                return True
            # elif relative_path.match(*self.extra_non_aesthetic):
            #     return False
            else:
                return False
        return aesthetic_attr

    def filter_relative_filenames(self, *filenames, aesthetic):
        """ If aesthetic is None then it doesn't filter any.
            True will return only aesthetic.
            False will return only non-aesthetic.

            :param generalpackager.Packager self:
            :param bool or None aesthetic: """
        return [path for path in filenames if aesthetic is None or aesthetic is self.relative_path_is_aesthetic(path)]

    @deco_cache()
    def _compare_local(self, platform, aesthetic):
        """ :param generalpackager.Packager self: """
        unpack_target = Path.get_cache_dir() / "Python"
        package_path = platform.download(path=unpack_target, overwrite=True)

        filt = lambda path: not path.match(*self.git_exclude_lines)

        differing_files = self.path.get_differing_files(target=package_path, filt=filt)

        return self.filter_relative_filenames(*differing_files, aesthetic=aesthetic)

    def compare_local_to_github(self, aesthetic=None):
        """ Get a list of changed files compared to remote with optional aesthetic files.

            :param generalpackager.Packager self:
            :param aesthetic: """
        return self._compare_local(platform=self.github, aesthetic=aesthetic)


    def compare_local_to_pypi(self, aesthetic=None):
        """ Get a list of changed files compared to pypi with optional aesthetic files.

            :param generalpackager.Packager self:
            :param aesthetic: """
        return self._compare_local(platform=self.pypi, aesthetic=aesthetic)

    def generate_setup(self):
        """ Generate setup.py.

            :param generalpackager.Packager self: """
        readme_path = self.localrepo.get_readme_path().relative(self.localrepo.get_setup_path().get_parent())
        last_version_split = self.python[-1].split(".")
        last_version_bumped_micro = f"{last_version_split[0]}.{int(last_version_split[1]) + 1}"
        setup_kwargs = {
            "name": f'"{self.localrepo.name}"',
            "author": f"'{self.author}'",
            "author_email": f'"{self.email}"',
            "version": f'"{self.localrepo.metadata.version}"',
            "description": f'"{self.localrepo.metadata.description}"',
            "long_description": "long_description",
            "long_description_content_type": '"text/markdown"',
            "install_requires": self.localrepo.metadata.install_requires,
            "url": f'"{self.github.url}"',
            "license": f'"{self.license}"',
            "python_requires": f'">={self.python[0]}, <{last_version_bumped_micro}"',
            "packages": 'find_namespace_packages(exclude=("build*", "dist*"))',
            "extras_require": self.localrepo.metadata.extras_require,
            "classifiers": self.get_classifiers(),
            # "include_package_data": True,
        }

        top = CodeLine()
        top.add_node(CodeLine("from setuptools import setup, find_namespace_packages", space_before=1))
        top.add_node(CodeLine("from pathlib import Path", space_after=1))

        top.add_node(CodeLine("try:")).add_node(CodeLine("long_description = (Path(__file__).parent / 'README.md').read_text(encoding='utf-8')"))
        top.add_node(CodeLine("except FileNotFoundError:")).add_node(CodeLine("long_description = 'Readme missing'", space_after=1))

        setup = top.add_node(CodeLine("setup("))
        for key, value in setup_kwargs.items():
            if isinstance(value, list) and value:
                list_ = setup.add_node(CodeLine(f"{key}=["))
                for item in value:
                    list_.add_node(CodeLine(f"'{item}',"))
                setup.add_node(CodeLine("],"))
            elif isinstance(value, dict) and value:
                dict_ = setup.add_node(CodeLine(f"{key}={{"))
                for k, v in value.items():
                    dict_.add_node(CodeLine(f"'{k}': {v},"))
                setup.add_node(CodeLine("},"))
            else:
                setup.add_node(CodeLine(f"{key}={value},"))

        top.add_node(CodeLine(")"))

        return top.text()

    def generate_manifest(self):
        """ Generate manifest file.

            :param generalpackager.Packager self: """
        default_manifest = [
            self.localrepo.get_metadata_path().relative(self.path),
        ]
        return "\n".join([f"include {path}" for path in self.localrepo.metadata.manifest + default_manifest])

    def generate_git_exclude(self):
        """ Generate git exclude file.

            :param generalpackager.Packager self: """
        return "\n".join(self.git_exclude_lines)

    def generate_license(self):
        """ Generate LICENSE by using Packager.license.

            :param generalpackager.Packager self: """
        # text = Path(self.localrepo.get_repos_path() / f"generalpackager/generalpackager/licenses/{self.license}").text.read()
        text = (type(self)("generalpackager").path / "generalpackager/licenses" / self.license).text.read()

        assert "$" in text
        text = text.replace("$year", str(Date.now().datetime.year))
        text = text.replace("$author", self.author)
        assert "$" not in text

        return text

    def generate_workflow(self):
        """ Generate workflow.yml.

            :param generalpackager.Packager self: """
        workflow = CodeLine()
        workflow.indent_str = " " * 2

        workflow.add_node(self._get_name())
        workflow.add_node(self._get_triggers())
        workflow.add_node(self._get_defaults())

        jobs = workflow.add_node("jobs:")
        jobs.add_node(self._get_unittest_job())
        jobs.add_node(self._get_sync_job())

        return workflow.text()

    def generate_readme(self):
        """ Generate readme markdown and overwrite README.md in local repo.

            :param generalpackager.Packager self: """
        # Description
        markdown = self.get_description_markdown()

        # Information
        self.get_information_markdown().set_parent(parent=markdown)

        # Table of contents
        contents = Markdown(header="Contents", parent=markdown)

        # Installation
        self.get_installation_markdown().set_parent(parent=markdown)

        # Attributes
        self.get_attributes_markdown().set_parent(parent=markdown)

        # Todos
        self.get_todos_markdown(self, drop_package_col=True).set_parent(parent=markdown)

        # Table of contents - Configuration
        self._configure_contents_markdown(markdown=contents)

        # Generation timestamp
        self.get_footnote_markdown().set_parent(parent=markdown)

        return markdown

    def generate_personal_readme(self):
        """ Generate personal readme markdown and overwrite README.md in local repo.

            :param generalpackager.Packager self: """
        # ordered_packagers = type(self)().get_ordered_packagers()
        ordered_packagers = self.get_ordered_packagers(include_private=False)


        # Description
        markdown = Markdown(header="ManderaGeneral").add_list_lines(
            "A collection of connected packages.",
            "Violently updated with little regard for backwards compatability.",
            "Automatic workflows to unittest, sync and publish.",
        )

        # Package information
        self.get_information_markdown(*ordered_packagers).set_parent(parent=markdown)

        # Todos
        self.get_todos_markdown(*ordered_packagers).set_parent(parent=markdown)

        # Generation timestamp
        self.get_footnote_markdown(commit=False).set_parent(parent=markdown)

        return markdown

    def generate_init(self):
        """ Generate __init__.py.

            :param generalpackager.Packager self: """
        codeline = CodeLine(f"", space_before=1, space_after=50)

        return codeline

    def generate_randomtesting(self):
        """ Generate randomtesting.py.

            :param generalpackager.Packager self: """
        codeline = CodeLine(f"from {self.name} import *", space_before=1, space_after=50)

        return codeline

    def generate_generate(self):
        """ Generate randomtesting.py.

            :param generalpackager.Packager self: """
        top = CodeLine()
        top.add_node(CodeLine(f"from generalpackager import Packager", space_before=1, space_after=1))
        top.add_node(CodeLine(f"""Packager("{self.name}").generate_localfiles(print_out=True)""", space_after=50))

        return top

    def generate_test_python(self):
        """ Generate test template.

            :param generalpackager.Packager self: """
        top = CodeLine()
        top.add_node(CodeLine("from unittest import TestCase", space_after=2))
        top.add_node("class Test(TestCase):").add_node("def test(self):").add_node("pass")

        return top

    def generate_npm_ignore(self):
        """ Generate .npmignore

            :param generalpackager.Packager self: """
        return "\n".join(self.npm_ignore_lines)

    def generate_index_js(self):
        """ Generate index.js

            :param generalpackager.Packager self: """
        top = CodeLine()
        top.add_node(CodeLine('exports.Vec2 = require("./vec2");', space_before=1, space_after=1))

        return top

    def generate_test_node(self):
        """ Generate test template.

            :param generalpackager.Packager self: """
        top = CodeLine()
        top.add_node("/**")
        top.add_node(" * @jest-environment jsdom")
        top.add_node(CodeLine(" */", space_after=1))
        top.add_node(CodeLine("// https://jestjs.io/docs/configuration#testenvironment-string", space_after=1))
        top.add_node(CodeLine('const Vec2 = require("./vec2");', space_after=1))
        top.add_node('test("Vec2 initializing", () => {').add_node("expect(new Vec2().x).toBe(0);")
        top.add_node("})")

        return top

    def generate_package_json(self):
        """ Generate test template.

            :param generalpackager.Packager self: """
        info = {
            "name": self.localrepo.name,
            "version": str(self.localrepo.metadata.version),
            "description": self.localrepo.metadata.description,
            "scripts": {
                "start": "parcel index.html",
                "build": "parcel build index.html",
                "test": "jest"
            },
            "dependencies": {dep: "latest" for dep in self.localrepo.dependencies},
            "devDependencies": {dep: "latest" for dep in self.localrepo.devDependencies},
            "keywords": self.get_topics(),
            "license": self.license,
            "author": self.author,
        }
        return json.dumps(info, indent=4)

    def generate_localfiles(self, aesthetic=True, print_out=False):
        """ Generate all local files.

            :param aesthetic:
            :param generalpackager.Packager self:
            :param print_out: """
        timer = Timer()

        # Not in files because it writes with json not text, it's also a bit unique
        self.localrepo.metadata.write_config()

        for generate in self.files:
            if aesthetic or not generate.aesthetic:
                if print_out:
                    print(f"Generating {generate}")
                generate.generate()
        if print_out:
            timer.print()


























