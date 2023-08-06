from generallibrary import NetworkDiagram

from generalpackager.api.localrepo.base.localrepo_target import _SharedTarget
from generalpackager.api.shared import _SharedAPI, _SharedName, _SharedPath
from generalpackager.other.packages import Packages
from generalpackager.packager_api import _PackagerAPIs
from generalpackager.packager_files import _PackagerFiles
from generalpackager.packager_github import _PackagerGitHub
from generalpackager.packager_markdown import _PackagerMarkdown
from generalpackager.packager_metadata import _PackagerMetadata
from generalpackager.packager_pypi import _PackagerPypi
from generalpackager.packager_relations import _PackagerRelations
from generalpackager.packager_workflow import _PackagerWorkflow


class Packager(NetworkDiagram,
               _SharedAPI, _SharedName, _SharedTarget, _SharedPath,
               _PackagerMarkdown, _PackagerGitHub, _PackagerFiles, _PackagerMetadata, _PackagerPypi, _PackagerWorkflow, _PackagerRelations, _PackagerAPIs):
    """ Uses APIs to manage 'general' package.
        Contains methods that require more than one API as well as methods specific for ManderaGeneral. """

    author = 'Rickard "Mandera" Abraham'
    email = "rickard.abraham@gmail.com"
    license = "mit"
    python = "3.8", "3.9"  # Only supports basic definition with tuple of major.minor
    os = "windows", "ubuntu"  # , "macos"

    git_exclude_lines = npm_ignore_lines = ".idea", "dist", ".git", "test/tests", ".coverage"
    git_exclude_lines += "build", "*.egg-info", "__pycache__", "PKG-INFO", "setup.cfg"
    npm_ignore_lines += "node_modules", ".parcel-cache"

    Packages = Packages

    def __init__(self, name=None, path=None, target=..., github_owner=None, pypi_owner=None):
        """ Storing pars as is. Name and target have some custom properties. """
        self._target = target
        self._github_owner = github_owner
        self._pypi_owner = pypi_owner


    @staticmethod
    def summary_packagers():
        """ Packagers to hold summary of environment. """
        return [
            Packager(name="Mandera", github_owner="Mandera"),
            Packager(name=".github", github_owner="ManderaGeneral"),
        ]

    def spawn_children(self):
        """ :param generalpackager.Packager self: """
        for packager in self.get_dependants(only_general=True):
            if packager.localrepo.metadata.enabled:
                packager.set_parent(parent=self)

    def spawn_parents(self):
        """ :param generalpackager.Packager self: """
        for packager in self.get_dependencies(only_general=True):
            if packager.localrepo.metadata.enabled:
                self.set_parent(parent=packager)

    def __repr__(self):
        info = [self.target]
        if self.path is None:
            info.append("No Path")
        info = str(info).replace("'", "")
        return f"<Packager {info}: {self.name}>"

















































