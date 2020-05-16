from metrics.visitors.base.inheritance_tree_visitor import InheritanceTreeVisitor


class MIDCalculationVisitor(InheritanceTreeVisitor):
    """
    Inheritance tree visitor for calculating maximum inheritance depth.

    Provides functionality for visiting an inheritance tree and returning its maximum inheritance depth, i.e. the
    maximum path length from any class to the base.
    """

    def __init__(self):
        self._visited = {}
        super().__init__()

    def visit(self, tree) -> int:
        self._visited = {}
        return tree.accept(self)

    def visit_children(self, cls) -> int:
        if cls.subclasses:
            return max([subclass.accept(self) for subclass in cls.subclasses])

        return 0

    def visit_class(self, cls) -> int:
        if cls not in self._visited:
            self._visited[cls] = 1 + self.visit_children(cls)
        return self._visited[cls]
