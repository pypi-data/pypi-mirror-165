
import pathlib

from generallibrary import VerInfo, TreeDiagram, Recycle

from generalfile.path_bases.path_lock import _Path_ContextManager
from generalfile.path_bases.path_operations import _Path_Operations
from generalfile.path_bases.path_strings import _Path_Strings
from generalfile.path_bases.path_envs import _Path_Envs
from generalfile.path_bases.path_scrub import _Path_Scrub
from generalfile.path_bases.path_diagram import _Path_Diagram


from generalfile.optional_dependencies.path_spreadsheet import Path_Spreadsheet
from generalfile.optional_dependencies.path_text import Path_Text
from generalfile.optional_dependencies.path_cfg import Path_Cfg
from generalfile.optional_dependencies.path_pickle import Path_Pickle


class Path(Recycle,
           _Path_ContextManager, _Path_Operations, _Path_Strings, _Path_Envs, _Path_Scrub, _Path_Diagram,
           Path_Spreadsheet, Path_Text, Path_Cfg, Path_Pickle):
    """ Immutable cross-platform Path.
        Built on pathlib and TreeDiagram.
        Implements rules to ensure cross-platform compatability.
        Adds useful methods.
        Todo: Binary extension. """
    verInfo = VerInfo()
    path_delimiter = verInfo.pathDelimiter
    Path = ...

    _recycle_keys = {"path": lambda path: Path.scrub(path)}
    _alternative_chars = {path_delimiter: "&#47;", ":": "&#58", ".": "&#46;"}

    def __init__(self, path=None):  # Don't have parent here because of Recycle
        self.path = self.scrub(path)

        self._path = pathlib.Path(self.path)
        self._latest_listdir = set()

    copy_node = NotImplemented  # Maybe something like this to disable certain methods

    def __str__(self):
        return getattr(self, "path", "<Path not loaded yet>")

    def __repr__(self):
        return f"<Path: '{self.path}'>"

    def __fspath__(self):
        return self.path

    def __format__(self, format_spec):
        return self.path.__format__(format_spec)

    def __truediv__(self, other):
        """ :rtype: generalfile.Path """
        return self.Path(self._path / str(other))

    def __eq__(self, other):
        if other is None:  # None in [Path()] was returning True without this
            return False

        if isinstance(other, Path):
            other = other.path
        else:
            other = self._scrub("" if other is None else str(other))
        return self.path == other

    def __hash__(self):
        return hash(self.path)

    def __contains__(self, item):
        return self.path.__contains__(item)

    def __dumps__(self):
        return str(self)

    @staticmethod
    def __loads__(path):
        return Path(path)

setattr(Path, "Path", Path)













































