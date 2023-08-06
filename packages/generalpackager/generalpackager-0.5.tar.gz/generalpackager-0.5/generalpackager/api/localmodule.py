
import pkg_resources
from generalfile import Path
from generallibrary import ObjInfo, deco_cache, EnvVar, get, import_module, deco_require, Log
from generalpackager.api.shared import _SharedAPI, _SharedName


class LocalModule(_SharedAPI, _SharedName):
    """ Tools to interface a Local Python Module. """

    # _deco_require_module = deco_require(lambda self: self.exists(), lambda func: f"{func.__name__} requires module.")

    def __init__(self, name=None):
        self._module = None

    def __repr__(self):
        return f"<{type(self).__name__}: {self.name}>"

    @property
    def module(self):
        if self._module is not None:
            return self._module
        else:
            return import_module(self.name, error=False)

    def exists(self):
        """ Return whether this API's target exists. """
        return bool(self.module)

    @property
    @deco_require(exists)
    def path(self):
        return Path(self.module.__file__)

    def _filter(self, objinfo):
        """ :param ObjInfo objinfo: """
        return objinfo.module().__name__.startswith(self.name) and (objinfo.from_class() or objinfo.from_module()) and not objinfo.is_instance()

    @property
    @deco_cache()
    def objInfo(self):
        if self.module is None:
            return None

        objInfo = ObjInfo(self.module)
        assert objInfo.is_module()

        # objInfo.children_states = ObjInfo.children_states.copy()
        # objInfo.children_states[ObjInfo.is_instance] = False

        objInfo.get_children(depth=-1, filt=self._filter, traverse_excluded=False)
        objInfo.disconnect(lambda node: not self._filter(node))

        return objInfo

    @deco_cache()
    @deco_require(exists, default=[])
    def get_env_vars(self, error=True):
        """ Get a list of EnvVar instances available directly in module.

            :rtype: list[generallibrary.EnvVar] """
        new_objInfo = ObjInfo(self.module)
        new_objInfo.all_identifiers = []  # Bad fix for bad circularity prevention
        return [objInfo.obj for objInfo in new_objInfo.get_children() if isinstance(objInfo.obj, EnvVar)]

    @staticmethod
    # @deco_cache()
    def get_all_local_modules():
        """ Get a list of all available LocalModules. """
        return [LocalModule(name=pkg.project_name) for pkg in pkg_resources.working_set]

    # @deco_cache()
    def get_dependencies(self):
        """ Get a list of LocalModules that this module depends on. """
        pkg = get(pkg_resources.working_set.by_key, self.name.lower())
        if not pkg:
            Log().debug(f"pkg empty for {self.name}")
            return []

        try:
            requires = pkg.requires()
        except FileNotFoundError:
            Log().debug(f"FileNotFoundError for {self.name}")
            return []
        return [LocalModule(name=str(name)) for name in requires]

    # @deco_cache()
    def get_dependants(self):
        """ Get a list of LocalModules that depend on this module. """
        return [local_module for local_module in self.get_all_local_modules() if self in local_module.get_dependencies()]


























