
from generalfile import Path
from generallibrary import Date
from requests import ConnectionError


class _PackagerPypi:
    def get_latest_release(self):
        """ Use current datetime if bumped, otherwise fetch.

            :param generalpackager.Packager self: """
        try:
            bumped = self.is_bumped()
        except ConnectionError:
            return "Failed fetching"

        if bumped:
            return Date.now()
        else:
            return self.pypi.get_date()

    @classmethod
    def reserve_name(cls, name):
        """ Reserve a name on PyPI with template files.

            :param generalpackager.Packager cls:
            :param name: """
        path = Path.get_cache_dir() / "python/pypi_reserve/" / name
        packager = cls.create_blank_locally_python(path=path, install=False)
        packager.localrepo.upload()
        path.delete()




























