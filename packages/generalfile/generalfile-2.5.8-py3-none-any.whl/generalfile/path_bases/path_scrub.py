
from generallibrary import deco_cache
from generalfile.errors import InvalidCharacterError

import re


class _Path_Scrub:
    @classmethod
    @deco_cache()
    def scrub(cls, str_path):
        """ :param generalfile.Path cls: """
        return cls._scrub(str_path=str_path)

    @classmethod
    def _scrub(cls, str_path):
        """ :param generalfile.Path cls: """
        str_path = "" if str_path is None else str(str_path)
        str_path = cls._replace_delimiters(str_path=str_path)


        match = re.match(fr"(\.+{re.escape(cls.path_delimiter)})", str_path)
        if match:
            dots = match.group()
            rest = str_path[len(dots):]
            index = len(dots) - 2

            rest_path = cls.Path(rest)
            working_dir = cls.Path().absolute()
            dot_path = working_dir.get_parent(depth=index, index=index, include_self=True)
            if dot_path is None:
                dot_path = working_dir.root()
            return str(dot_path / rest_path)


        str_path = cls._invalid_characters(str_path=str_path)
        str_path = cls._trim(str_path=str_path)
        str_path = cls._delimiter_suffix_if_root(str_path=str_path)


        return str_path

    @classmethod
    @deco_cache()
    def _replace_delimiters(cls, str_path):
        """ :param generalfile.Path cls: """
        str_path = str_path.replace("/", cls.path_delimiter)
        str_path = str_path.replace("\\", cls.path_delimiter)
        return str_path

    @classmethod
    @deco_cache()
    def _invalid_characters(cls, str_path):
        """ :param generalfile.Path cls: """
        # Simple invalid characters testing from Windows
        for character in '<>"|?*':
            if character in str_path:
                raise InvalidCharacterError(f"Invalid character '{character}' in '{str_path}'")

        if ":" in str_path:
            if not cls.verInfo.pathRootHasColon:
                raise InvalidCharacterError(f"Path has a colon but '{cls.verInfo.os}' doesn't use colon for path root: '{str_path}'")
            if str_path[1] != ":":
                raise InvalidCharacterError(f"Path has a colon but there's no colon at index 1: '{str_path}'")
            if len(str_path) >= 3 and str_path[2] != cls.path_delimiter:
                raise InvalidCharacterError(f"Path has a colon but index 2 is not a delimiter: '{str_path}'")
            if ":" in str_path[2:]:
                raise InvalidCharacterError(f"Path has a colon that's not at index 1: '{str_path}'")

        if str_path.endswith("."):
            raise InvalidCharacterError(f"Path cannot end with a dot ('.').")
        return str_path

    @classmethod
    @deco_cache()
    def _trim(cls, str_path):
        """ :param generalfile.Path cls: """
        if not cls.verInfo.pathRootIsDelimiter and str_path.startswith(cls.path_delimiter):
            str_path = str_path[1:]
        if str_path.endswith(cls.path_delimiter) and len(str_path) > 1:
            str_path = str_path[0:-1]
        return str_path

    @classmethod
    @deco_cache()
    def _delimiter_suffix_if_root(cls, str_path):
        """ :param generalfile.Path cls: """
        if len(str_path) == 2 and str_path[1] == ":":
            return f"{str_path}{cls.path_delimiter}"
        return str_path