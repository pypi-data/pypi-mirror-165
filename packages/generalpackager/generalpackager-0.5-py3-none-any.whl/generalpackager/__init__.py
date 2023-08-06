from generallibrary import interconnect

from generalpackager.other.envvars import PACKAGER_GITHUB_API, TWINE_USERNAME, TWINE_PASSWORD

from generalpackager.packager import Packager

from generalpackager.api.localrepo.base.localrepo import LocalRepo
from generalpackager.api.localrepo.python.localrepo_python import LocalRepo_Python
from generalpackager.api.localrepo.node.localrepo_node import LocalRepo_Node

from generalpackager.api.localmodule import LocalModule
from generalpackager.api.github import GitHub
from generalpackager.api.pypi import PyPI

interconnect(Packager, LocalRepo, LocalModule, GitHub, PyPI)
