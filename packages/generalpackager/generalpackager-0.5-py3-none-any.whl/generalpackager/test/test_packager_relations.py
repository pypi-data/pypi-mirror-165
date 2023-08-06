from generallibrary import Log

from generalpackager import Packager

import unittest


class TestPackager(unittest.TestCase):
    def test_get_ordered_packagers(self):
        self.assertLess(3, len(Packager().get_ordered_packagers()))

    def test_get_owners_package_names(self):
        self.assertLess(4, len(Packager().get_owners_package_names()))

    def test_general_bumped_set(self):
        packager = Packager()
        packager.general_bumped_set()

    def test_general_changed_dict(self):
        Packager().general_changed_dict()

    def test_get_untested_objInfo_dict(self):
        self.assertIsInstance(Packager().get_untested_objInfo_dict(), dict)
