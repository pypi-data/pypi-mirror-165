from generalfile.test.test_path import PathTest

from generalpackager import Packager


class TestPackagerAPI(PathTest):
    def test_available(self):
        self.assertEqual(True, Packager().pypi_available())
        self.assertEqual(True, Packager().localrepo_available())
        self.assertEqual(True, Packager().github_available())
        self.assertEqual(True, Packager().localmodule_available())

        self.assertEqual(True, Packager("doesntexist").pypi_available())
        self.assertEqual(True, Packager("doesntexist").localrepo_available())
        self.assertEqual(True, Packager("doesntexist").github_available())
        self.assertEqual(True, Packager("doesntexist").localmodule_available())

    def test_name_is_general(self):
        self.assertEqual(True, Packager.name_is_general("generallibrary"))
        self.assertEqual(True, Packager.name_is_general("genlibrary"))
        self.assertEqual(True, Packager.name_is_general("generalpackager"))
        self.assertEqual(False, Packager.name_is_general("doesntexist"))
        self.assertEqual(False, Packager.name_is_general("django"))
        self.assertEqual(False, Packager.name_is_general("pandas"))

    def test_simple_name(self):
        self.assertEqual("packager", Packager().simple_name)
        self.assertEqual("vector", Packager("genvector").simple_name)
