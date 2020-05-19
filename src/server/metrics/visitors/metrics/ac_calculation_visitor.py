from typing import Dict

from metrics.structures.dependency_graph import *
from metrics.visitors.base.dependency_graph_visitor import DependencyGraphVisitor


class ACCalculationVisitor(DependencyGraphVisitor):
    """
    Dependency graph visitor for calculating afferent coupling.

    Provides functionality for visiting a dependency graph and returning the afferent coupling of each class in the
    graph, where the afferent coupling of a class is the number of classes that directly depend on it.

    """

    def __init__(self):
        super().__init__()
        self._visited = []
        self.afferent_couplings = {}

    def visit(self, graph) -> Dict[Class, int]:
        self._visited = []
        self.afferent_couplings = {}
        for cls in graph.classes:
            for node in cls:
                self.afferent_couplings[node] = 0

        for cls in self.afferent_couplings:
            cls.accept(self)

        return self.afferent_couplings

    def visit_children(self, cls) -> None:
        """
        Visit each of a class' dependencies.

        :param cls: The parent class whose dependencies to visit.
        """
        if cls.dependencies:
            for dependency in cls.dependencies:
                dependency.accept(self)

    def visit_class(self, cls) -> None:
        """
        Visit dependency graph generic class and update afferent couplings.

        :param cls: The generic class.
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
