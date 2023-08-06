
from itertools import chain

from generallibrary import deco_cache

from generalpackager.api.localrepo.base.localrepo_target import _LocalRepo_Target


class Packages(_LocalRepo_Target.Targets):
    """ Names of all general packages categorized by target.
        Todo: Generate Python file in generalpackager containing general packages. """
    python = [
        "generallibrary",
        "generalfile",
        "generalvector",
        "generalgui",
        "generalbrowser",
        "generalpackager",
    ]
    node = [
        "genlibrary",
        "genvector",
    ]
    django = [

    ]
    exe = [
        "generalmainframe",
    ]

    @classmethod
    @deco_cache()
    def all_packages(cls):
        return list(chain(*cls.field_values_defaults()))

