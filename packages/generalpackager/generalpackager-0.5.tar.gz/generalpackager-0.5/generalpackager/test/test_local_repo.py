from generalfile import Path
from generallibrary import Ver
from generalpackager.api.localrepo.base.localrepo import LocalRepo
from generalpackager.api.localrepo.python.localrepo_python import LocalRepo_Python
from generalfile.test.test_path import PathTest


class TestLocalRepo(PathTest):
    def test_metadata_exists(self):
        self.assertEqual(True, LocalRepo().metadata_exists())
        self.assertEqual(False, LocalRepo("doesntexist").metadata_exists())

    def test_load_metadata(self):
        self.assertEqual(True, LocalRepo().metadata.enabled)
        self.assertEqual("generalpackager", LocalRepo().name)
        self.assertIsInstance(LocalRepo().metadata.version, Ver)
        self.assertIsInstance(LocalRepo().metadata.description, str)
        self.assertIsInstance(LocalRepo().metadata.topics, list)
        self.assertIsInstance(LocalRepo().metadata.manifest, list)

        self.assertIsInstance(LocalRepo().targetted().metadata.install_requires, list)
        self.assertIsInstance(LocalRepo().targetted().metadata.extras_require, dict)

    def test_exists(self):
        self.assertEqual(True, LocalRepo().exists())
        self.assertEqual(True, LocalRepo.repo_exists(LocalRepo().path))

        self.assertEqual(False, LocalRepo("doesntexist").exists())

    def test_get_test_paths(self):
        self.assertLess(2, len(list(LocalRepo().get_test_paths())))
        self.assertIn(LocalRepo().get_test_path() / "test_local_repo.py", LocalRepo().get_test_paths())

    def test_text_in_tests(self):
        self.assertEqual(True, LocalRepo().text_in_tests("stringthatexists"))
        self.assertEqual(False, LocalRepo().text_in_tests("stringthat" + "doesntexist"))

    def test_get_package_paths(self):
        package_paths = list(LocalRepo().get_package_paths_gen())
        self.assertIn(LocalRepo().get_test_path(), package_paths)
        self.assertIn(LocalRepo().path / LocalRepo().name, package_paths)
        self.assertNotIn(LocalRepo().path, package_paths)

    def test_get_changed_files(self):
        local_repo = LocalRepo_Python()
        version = local_repo.metadata.version

        local_repo.bump_version()
        self.assertNotEqual(local_repo.metadata.version, version)
        self.assertIn("metadata.json", local_repo.git_changed_files())

        local_repo.metadata.version = version
        self.assertEqual(local_repo.metadata.version, version)

    def test_wrong_localrepo_for_target(self):
        local_repo = LocalRepo()
        self.assertRaises(AssertionError, local_repo.bump_version)

    def test_targets(self):
        self.assertEqual(LocalRepo().metadata.target, LocalRepo.Targets.python)

    def test_format_file_function(self):
        Path("foo").text.write(
            "def camelCase():\n"
            '    """ '
            '        Bad docstrings\n'
            '    """'
        )

        LocalRepo.format_file("foo")

        self.assertEqual(
            'def camel_case():\n'
            '    """ Bad docstrings """',
            Path("foo").text.read())

    def test_format_file_method(self):
        Path("foo").text.write(
            "class FooBar:\n"
            "    def camelCase(self):\n"
            '        """ '
            '            Bad docstrings\n'
            '        """'
        )

        LocalRepo.format_file("foo")

        self.assertEqual(
            'class FooBar:\n'
            '    def camel_case(self):\n'
            '        """ Bad docstrings """',
            Path("foo").text.read())

    def test_get_paths(self):
        self.assertIn("generalpackager", LocalRepo().get_readme_path())
        self.assertIn("generalpackager", LocalRepo().get_org_readme_path())
        self.assertIn("generalpackager", LocalRepo().get_metadata_path())
        self.assertIn("generalpackager", LocalRepo().get_git_exclude_path())
        self.assertIn("generalpackager", LocalRepo().get_setup_path())
        self.assertIn("generalpackager", LocalRepo().get_manifest_path())
        self.assertIn("generalpackager", LocalRepo().get_license_path())
        self.assertIn("generalpackager", LocalRepo().get_workflow_path())
        self.assertIn("generalpackager", LocalRepo().get_test_path())
        self.assertIn("generalpackager", LocalRepo().get_test_template_path())
        self.assertIn("generalpackager", LocalRepo().get_init_path())
        self.assertIn("generalpackager", LocalRepo().get_randomtesting_path())
        self.assertIn("generalpackager", LocalRepo().get_generate_path())
        self.assertIn("generalpackager", LocalRepo().get_exetarget_path())
        self.assertIn("generalpackager", LocalRepo().get_exeproduct_path())
        self.assertIn("generalpackager", LocalRepo().get_git_ignore_path())
        self.assertIn("generalpackager", LocalRepo().get_npm_ignore_path())
        self.assertIn("generalpackager", LocalRepo().get_index_js_path())
        self.assertIn("generalpackager", LocalRepo().get_test_js_path())
        self.assertIn("generalpackager", LocalRepo().get_package_json_path())

    def test_is_target(self):
        self.assertEqual(True, LocalRepo().is_python())
        self.assertEqual(False, LocalRepo().is_exe())
        self.assertEqual(False, LocalRepo().is_node())
        self.assertEqual(False, LocalRepo().is_django())



class TestLocalRepoPython(PathTest):
    def test_get_venv_path(self):
        venv = LocalRepo_Python().get_venv_path()
        self.assertEqual(True, venv is None or venv.is_venv())
























