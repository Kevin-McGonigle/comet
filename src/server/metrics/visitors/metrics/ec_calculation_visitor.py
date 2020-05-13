from typing import Dict

from metrics.structures.dependency_graph import *


class ECCalculationVisitor(DependencyGraphVisitor):
    """
    Dependency graph visitor for calculating efferent coupling.

    Provides functionality for visiting a dependency graph and returning the efferent coupling of each class in the
    graph, where the efferent coupling of a class is the number of classes that it directly depends on.
    """

    def __init__(self):
        super().__init__()
        self._visited = []
        self.efferent_couplings = {}

    def visit(self, graph) -> Dict[Class, int]:
        self._visited = []
        self.efferent_couplings = {cls: 0 for cls in graph.classes}

        for cls in graph.classes:
            cls.accept(self)

        return self.efferent_couplings

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
        Visit dependency graph generic class and update efferent couplings.

        :param cls: The generic class.
        """
        if cls not in self._visited:
            self._visited.append(cls)

            if cls.dependencies:
                self.efferent_couplings[cls] = len(cls.dependencies)

            self.visit_children(cls)
