
from generallibrary import DataClass

from generalpackager.api.localrepo.base.metadata import Metadata


class Targets(DataClass):
    python = "python"
    node = "node"
    django = "django"
    exe = "exe"


class _SharedTarget:
    def is_python(self):
        """ :param generalpackager.Packager or generalpackager.LocalRepo self: """
        return self.target == Targets.python

    def is_node(self):
        """ :param generalpackager.Packager or generalpackager.LocalRepo self: """
        return self.target == Targets.node

    def is_django(self):
        """ :param generalpackager.Packager or generalpackager.LocalRepo self: """
        return self.target == Targets.django

    def is_exe(self):
        """ :param generalpackager.Packager or generalpackager.LocalRepo self: """
        return self.target == Targets.exe


class _LocalRepo_Target(_SharedTarget):
    """ Target of None is only for packages without a metadata.json file. """
    Targets = Targets

    _cls_target = None
    _cls_metadata = Metadata
    _cls_target_classes = {}

    assert set(Metadata.field_dict_literals()["target"]) == set(Targets.field_values_defaults()), "Targets aren't synced, couldn't make this DRY."

    def __init_subclass__(cls, **kwargs):
        """ Return another LocalRepo object which has extended functionality based on target of metadata.

            :param generalpackager._LocalRepos_DOCS cls: """
        super().__init_subclass__(**kwargs)

        if cls.__name__ != cls._BASE_CLS_NAME:
            assert cls._cls_target in cls.Targets.field_values_defaults()
            assert cls._cls_metadata is not Metadata

        cls._cls_target_classes[cls._cls_target] = cls

    def targetted(self, target=...):
        """ Return another LocalRepo object which has extended functionality based on target of metadata.

            :param generalpackager._LocalRepos_DOCS self:
            :param target:
            :rtype: generalpackager._LocalRepos_DOCS """

        if target is Ellipsis:
            if self.metadata and self.metadata.exists():
                target = self.metadata.target

        if target in self._cls_target_classes:
            return self._cls_target_classes[target](name=self.name, path=self.path)
        else:
            return self


