from requests import Response

from generalpackager.api.github import GitHub

import unittest


class TestGitHub(unittest.TestCase):
    def test_exists(self):
        self.assertEqual(True, GitHub("generalpackager").exists())

    def test_get_owners_packages(self):
        github = GitHub()
        self.assertEqual(set(), {"generallibrary", "generalfile", "generalvector", "generalpackager"}.difference(github.get_owners_packages()))

        github = GitHub(owner="pandas-dev")
        self.assertEqual(True, "pandas" in github.get_owners_packages())

    def test_get_topics(self):
        github = GitHub("generalpackager")
        topics = github.get_topics()
        self.assertTrue(topics)
        self.assertEqual(True, github.set_topics(*topics).ok)

    def test_get_website(self):
        github = GitHub("generalpackager")
        website = github.get_website()
        self.assertEqual(True, "pypi" in website)
        self.assertEqual(True, github.set_website(website).ok)

    def test_get_description(self):
        github = GitHub("generalpackager")
        description = github.get_description()
        self.assertEqual(True, len(description) > 5)
        self.assertEqual(True, github.set_description(description).ok)

    def test_commands(self):
        self.assertIn("generalpackager", GitHub().git_clone_command)
        self.assertIn("generalpackager", GitHub().pip_install_command)

    def test_request_kwargs(self):
        self.assertIn("headers", GitHub().request_kwargs())

