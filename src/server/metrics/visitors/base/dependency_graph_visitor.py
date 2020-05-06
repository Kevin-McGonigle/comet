from typing import TYPE_CHECKING

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

    def visit(self, graph):
        """
        Visit a dependency graph structure.
        :param graph: The dependency graph to visit.
        :type graph: DependencyGraph
        :return: The output of the visiting process.
        :rtype: Any
        """
        self._visited = {}

        return super().visit(graph)

    def visit_children(self, cls):
        """
        "Visit" each of a class' dependencies. (Actually just returns the list of dependencies to avoid susceptibility
        to cycles).
        :param cls: The parent class whose dependencies to visit.
        :type cls: Class
        :return: A list of the class' dependencies.
        :rtype: list[Class]
        """
        return cls.dependencies

    def visit_class(self, cls):
        """
        Visit dependency graph generic class.
        :param cls: The generic class.
        :type cls: Class
        :return: The result of the visit.
        :rtype: Any
        """
        if cls not in self._visited:
            self._visited[cls] = self.visit_children(cls)
        return self._visited[cls]

    def visit_known_class(self, cls):
        """
        Visit dependency graph known class.
        :param cls: The known class.
        :type cls: KnownClass
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_class(cls)

    def visit_unknown_class(self, cls):
        """
        Visit dependency graph unknown class.
        :param cls: The unknown class.
        :type cls: UnknownClass
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_class(cls)
