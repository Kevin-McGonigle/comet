from metrics.structures.ast import *
from metrics.visitors.base.Visitor import Visitor


class ASTVisitor(Visitor):
    def visit_statements(self, node):
        """
        Visit AST statements node.
        :param node: The AST statements node.
        :type node: ASTStatementsNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)
