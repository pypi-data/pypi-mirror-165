

from generalpackager import Packager

import unittest


class TestPackager(unittest.TestCase):
    def test_get_latest_release(self):
        self.assertIn("CE", str(Packager().get_latest_release()))


