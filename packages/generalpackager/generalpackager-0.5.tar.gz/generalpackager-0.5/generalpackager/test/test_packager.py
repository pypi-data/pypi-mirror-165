

import unittest

from generalpackager import Packager


class TestPackager(unittest.TestCase):
    def test_name(self):
        self.assertEqual("generalpackager", Packager().name)

    def test_all_packages(self):
        all_packages = Packager.Packages.all_packages()
        self.assertIn("generallibrary", all_packages)
        self.assertIn("generalfile", all_packages)
        self.assertIn("genlibrary", all_packages)

        self.assertIn("generallibrary", Packager.Packages.python)
        self.assertIn("generalfile", Packager.Packages.python)
        self.assertIn("genlibrary", Packager.Packages.node)

    def test_summary_packagers(self):
        self.assertEqual(True, Packager.summary_packagers()[0].localrepo.exists())
        self.assertEqual(True, Packager.summary_packagers()[1].localrepo.exists())



