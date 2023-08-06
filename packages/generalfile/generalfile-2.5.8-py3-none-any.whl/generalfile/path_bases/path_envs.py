
from generallibrary import EnvVar

class _Path_Envs:
    """ Get information of path such as venv and package. """
    def is_venv(self):
        """ :param generalfile.Path self: """
        return (self / "Scripts/activate").exists()

    def is_package(self):
        """ :param generalfile.Path self: """
        return bool(self.get_child(filt=lambda path: path.name() == "__pycache__"))

    def is_repo(self):
        """ :param generalfile.Path self: """
        return bool(self.get_child(filt=lambda x: x.name() in (".git", "metadata.json")))

    def get_parent_venv(self):
        """ Return first valid venv in parents or None

            :param generalfile.Path self:
            :rtype: generalfile.Path """
        return self.absolute().get_parent(depth=-1, include_self=True, traverse_excluded=True, filt=type(self).is_venv)

    def get_parent_package(self):
        """ Return last valid package in parents or None.

            :param generalfile.Path self:
            :rtype: generalfile.Path """
        return self.absolute().get_parent(depth=-1, index=-1, include_self=True, traverse_excluded=True, filt=type(self).is_package)

    def get_parent_repo(self):
        """ Return first valid repo in parents or None.

            :param generalfile.Path self:
            :rtype: generalfile.Path """
        return self.absolute().get_parent(depth=-1, include_self=True, traverse_excluded=True, filt=type(self).is_repo)

    @classmethod
    def get_active_venv(cls):
        """ :rtype: generalfile.Path """
        virtual_env = EnvVar("VIRTUAL_ENV", default=None).value
        if virtual_env is not None:
            venv_path = cls(virtual_env)
            assert venv_path.is_venv()
            return venv_path

































