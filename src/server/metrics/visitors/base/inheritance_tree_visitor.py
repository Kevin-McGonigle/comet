from typing import TYPE_CHECKING

from metrics.visitors.base.graph_visitor import GraphVisitor

if TYPE_CHECKING:
    from metrics.structures.inheritance_tree import *


class InheritanceTreeVisitor(GraphVisitor):
    """
    Inheritance tree visitor.

    Base class for visiting inheritance tree structures.
    """

    def __init__(self):
        self._visited = []

    def visit(self, tree):
        """
        Visit an inheritance tree structure.
        :param tree: The inheritance tree to visit.
        :type tree: InheritanceTree
        :return: The output of the visiting process.
        :rtype: Any
        """
        self._visited = []

        return super().visit(tree)

    def visit_children(self, cls):
        """
        Visit each of the class' subclasses.
        :param cls: The parent class whose subclasses to visit.
        :type cls: Class
        :return: Mapping of each subclass to their visit result.
        :rtype: dict{Class, Any}
        """
        return super().visit_children(cls)

    def visit_class(self, cls):
        """
        Visit inheritance tree generic class.
        :param cls: The generic class.
        :type cls: Class
        :return: The result of the visit.
        :rtype: Any
        """
        if cls not in self._visited:
            self._visited.append(cls)
            return self.visit_children(cls)

    def visit_known_class(self, cls):
        """
        Visit inheritance tree known class.
        :param cls: The known class.
        :type cls: KnownClass
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_class(cls)

    def visit_unknown_class(self, cls):
        """
        Visit inheritance tree unknown class.
        :param cls: The unknown class.
        :type cls: UnknownClass
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_class(cls)
