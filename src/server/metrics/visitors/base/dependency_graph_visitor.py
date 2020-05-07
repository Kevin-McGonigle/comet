from typing import TYPE_CHECKING, List, Any

from metrics.visitors.base.graph_visitor import GraphVisitor

if TYPE_CHECKING:
    from metrics.structures.dependency_graph import *


class DependencyGraphVisitor(GraphVisitor):
    """
    Dependency graph visitor.

    Base class for visiting dependency graph structures.
    """

    def __init__(self):
        self._visited = {}

    def visit(self, graph: DependencyGraph) -> Any:
        """
        Visit a dependency graph structure.
        :param graph: The dependency graph to visit.
        :return: The output of the visiting process.
        """
        self._visited = {}

        return super().visit(graph)

    def visit_children(self, cls: Class) -> List[Class]:
        """
        "Visit" each of a class' dependencies. (Actually just returns the list of dependencies to avoid susceptibility
        to cycles).
        :param cls: The parent class whose dependencies to visit.
        :return: A list of the class' dependencies.
        """
        return cls.dependencies

    def visit_class(self, cls: Class) -> Any:
        """
        Visit dependency graph generic class.
        :param cls: The generic class.
        :return: The result of the visit.
        """
        if cls not in self._visited:
            self._visited[cls] = self.visit_children(cls)
        return self._visited[cls]

    def visit_known_class(self, cls: KnownClass) -> Any:
        """
        Visit dependency graph known class.
        :param cls: The known class.
        :return: The result of the visit.
        """
        return self.visit_class(cls)

    def visit_unknown_class(self, cls: UnknownClass) -> Any:
        """
        Visit dependency graph unknown class.
        :param cls: The unknown class.
        :return: The result of the 4visit.
        """
        return self.visit_class(cls)
