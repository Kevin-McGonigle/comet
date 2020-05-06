from typing import TYPE_CHECKING

from metrics.visitors.base.dependency_graph_visitor import DependencyGraphVisitor

if TYPE_CHECKING:
    from metrics.structures.dependency_graph import *


class ACCalculationVisitor(DependencyGraphVisitor):
    """
    Dependency graph visitor for calculating afferent coupling.

    Provides functionality for visiting a dependency graph and returning the afferent coupling of each class in the
    graph, where the afferent coupling of a class is the number of classes that directly depend on it.

    """

    def __init__(self):
        self._visited = []
        self.afferent_couplings = {}
        super().__init__()

    def visit(self, graph):
        self._visited = []
        self.afferent_couplings = {cls: 0 for cls in graph.classes}

        for cls in graph.classes:
            cls.accept(self)

        return self.afferent_couplings

    def visit_children(self, cls):
        """
        Visit each of a class' dependencies.
        :param cls: The parent class whose dependencies to visit.
        :type cls: Class
        """
        if cls.dependencies:
            for dependency in cls.dependencies:
                dependency.accept(self)

    def visit_class(self, cls):
        """
        Visit dependency graph generic class and update afferent couplings.
        :param cls: The generic class.
        :type cls: Class
        """
        if cls not in self._visited:
            self._visited.append(cls)

            if cls.dependencies:
                for dependency in cls.dependencies:
                    if dependency in self.afferent_couplings:
                        self.afferent_couplings[dependency] += 1
                    else:
                        self.afferent_couplings[dependency] = 1

            self.visit_children(cls)
