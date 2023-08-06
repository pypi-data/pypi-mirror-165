# class TestPackager(PathTest):
#     def setUpClass(cls):
#         Packager("genvector").node.download()
#
#     def test_generate_index_js(self):
#         packager = Packager()
#         text = str(packager.generate_index_js())
#         self.assertEqual(True, len(text) > 2)
#
#     def test_generate_npm_ignore(self):
#         packager = Packager()
#         text = str(packager.generate_npm_ignore())
#         self.assertIn(".git", text)
#
#     def test_generate_package_json(self):
#         packager = Packager()
#         text = str(packager.generate_package_json())
#         self.assertIn(".git", text)
#
#     def test_generate_test_node(self):
#         packager = Packager()
#         text = str(packager.generate_test_node())
#         self.assertIn("jest", text)
