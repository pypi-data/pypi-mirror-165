
import re

from generalfile import Path
from generallibrary import deco_cache, deco_require
from git import Repo
from setuptools import find_namespace_packages

from generalpackager.api.localrepo.base.localrepo_paths import _LocalRepo_Paths
from generalpackager.api.localrepo.base.localrepo_target import _LocalRepo_Target
from generalpackager.api.shared import _SharedAPI, _SharedPath, _SharedName


class LocalRepo(_SharedAPI, _SharedName, _SharedPath, _LocalRepo_Paths, _LocalRepo_Target):
    """ Tools to help Path interface a Local Repository.
        Base functionality.
        Inherited by classes in targets folder for extended functionality.
        Packager will chose correct class by using LocalRepo.metadata.target
        Todo: Search for imports to list dependencies. """

    _BASE_CLS_NAME = "LocalRepo"

    # _deco_require_metadata = deco_require(lambda self: self.metadata.exists(), lambda func: f"{func.__name__} requires metadata.")

    def __init__(self, name=None, path=None):
        pass

    @property
    @deco_cache()
    def metadata(self):
        if self.path is None:
            return None
        else:
            return self._cls_metadata(path=self.get_metadata_path())

    @property
    def target(self):
        if self.metadata and self.metadata.exists():
            return self.metadata.target
        else:
            return None

    def metadata_exists(self):
        """ Needed to make deco_require be able to use this. """
        return bool(self.metadata and self.metadata.exists())

    # @property
    # def name(self):
    #     """ Only getter for name to make _SharedAPI work. """
    #     return self.metadata.name if self.metadata_exists() else self.path.stem()

    def __repr__(self):
        return f"<{type(self).__name__} for '{self.path}'>"

    def exists(self):
        """ Return whether this API's target exists. """
        return self.repo_exists(path=self.path)

    @classmethod
    def repo_exists(cls, path):
        if path is None or path.is_file() or not path.exists():
            return False
        return bool(path.get_child(filt=lambda x: x.name() in (".git", "metadata.json"), traverse_excluded=True))  # setup.py was not included in pypi's sdist

    @deco_cache()
    def get_test_paths(self):
        """ List of paths to each test python file.

            :rtype: list[Path] """
        return self.get_test_path().get_children(depth=-1, filt=lambda path: path.endswith(".py") and not path.match("/tests/"), traverse_excluded=True)

    @deco_cache()
    def text_in_tests(self, text):
        """ Return whether text exists in one of the test files. """
        for path in self.get_test_paths():
            if path.contains(text=str(text)):
                return True
        return False

    def get_package_paths_gen(self):
        """ Yield Paths pointing to each folder containing a Python file in this local repo, aka `namespace package`.
            Doesn't include self.path """
        for package in find_namespace_packages(where=str(self.path)):
            path = self.path / package.replace(".", "/")
            if not path.match("/dist", "/build"):
                yield path

    def git_changed_files(self):
        """ Get a list of changed files using local .git folder. """
        repo = Repo(str(self.path))
        return [Path(file) for file in re.findall("diff --git a/(.*) " + "b/", repo.git.diff())]

    @deco_require(metadata_exists)
    def bump_version(self):
        """ Bump micro version in metadata.json. """
        self.metadata.version = self.metadata.version.bump()

    @staticmethod
    def _camel_to_under(match):
        return "".join(f"_{c.lower()}" if c.isupper() else c for c in match[0])

    @classmethod
    def _replace_camel_case(cls, text):
        return re.sub(r"\W([a-z]+(?:[A-Z][a-z]*)+)", cls._camel_to_under, text)

    @staticmethod
    def _strip_line(line):
        return line.replace('"""', "").strip()

    @classmethod
    def _format_docstring(cls, match):
        lines = match[0].splitlines()  # type: list[str]
        indent = lines[0].find('"')

        lines = [x for line in lines if (x := (cls._strip_line(line)))]  # Strip
        lines = [f'{" " * (indent + 4)}{line}' for line in lines]  # Indent all
        lines[0] = f'{" " * indent}""" {lines[0][indent + 4:]}'  # Quotes first line
        lines[-1] += ' """'  # Quotes last line

        return "\n".join(lines)

    @classmethod
    def _replace_docstrings(cls, text):
        return re.sub(r' +""".*?"""', cls._format_docstring, text, flags=re.S)

    @classmethod
    def format_file(cls, path, write=True):
        """ Format a file by overwriting it with proper format.
            Replaces camelCase with under_scores.
            Replaces bad docstrings with good. """
        path = Path(path)
        old_text = path.text.read()
        new_text = cls._replace_camel_case(text=old_text)
        new_text = cls._replace_docstrings(text=new_text)

        if write:
            path.text.write(new_text, overwrite=True)
            return new_text

        else:
            from selenium import webdriver
            from webdriver_manager.chrome import ChromeDriverManager

            driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.get("https://text-compare.com/")
            driver.maximize_window()
            driver.execute_script("arguments[0].value = arguments[1];", driver.find_element_by_id("inputText1"), old_text)
            driver.execute_script("arguments[0].value = arguments[1];", driver.find_element_by_id("inputText2"), new_text)
            driver.find_element_by_class_name("compareButtonText").click()

            while True:
                pass


































