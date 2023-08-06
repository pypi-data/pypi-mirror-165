

from generalpackager import Packager

import unittest


class TestPackager(unittest.TestCase):
    def test_get_topics(self):
        self.assertIn("windows", Packager().get_topics())

    def test_get_classifiers(self):
        self.assertIn("Operating System :: Microsoft :: Windows", Packager().get_classifiers())

    def test_is_bumped(self):
        packager = Packager()
        packager.is_bumped()
        version = packager.localrepo.metadata.version
        packager.localrepo.bump_version()
        self.assertEqual(True, packager.is_bumped())
        packager.localrepo.metadata.version = version

