
from generallibrary import TreeDiagram
import os


class _Path_Diagram(TreeDiagram):
    def view_paths(self, spawn=True):
        """ :param generalfile.Path self: """
        self.view(spawn=spawn, custom_repr=lambda path: path.name())

    def spawn_parents(self):
        """ :param generalfile.Path self: """
        if not self.get_parent(spawn=False) and self.path and not self.is_root():
            try:
                index = self.path.rindex(self.path_delimiter) + 1
            except ValueError:
                index = 0
            self.set_parent(self.Path(path=self.path[:index]))

    def spawn_children(self):
        """ :param generalfile.Path self: """
        if self.is_folder():
            old_children = {path.name() for path in self.get_children(spawn=False)}

            try:
                new_children = set(os.listdir(self.path if self.path else "."))
            except PermissionError:
                new_children = set()

            for name in old_children - new_children:
                self.Path(path=self / name).set_parent(parent=None)

            for name in new_children - old_children:
                self.Path(path=self / name).set_parent(parent=self)
        else:
            self._children.clear()



