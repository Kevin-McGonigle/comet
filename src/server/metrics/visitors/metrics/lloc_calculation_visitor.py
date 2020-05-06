from metrics.visitors.base.ast_visitor import ASTVisitor


class LLOCCalculationVisitor(ASTVisitor):
    """
    Logical lines of code calculation visitor.

    Provides functionality for visiting an abstract syntax tree and returning the number of
    logical lines of code (i.e. the number of statements) present.
    """

    def visit_children(self, node) -> int:
        """
        Visit each of an AST node's children and return the number of statements in the node's subtree.

        :param node: The parent AST node whose children to visit.
        :return: The number of statements in the node's subtree.
        """
        return sum([child.accept(self) for child in node.children])

    @staticmethod
    def visit_identifier(node) -> int:
        """
        Visit AST identifier node.
        :param node: The AST identifier node to visit.
        :return: Zero.
        """

        return 0

    @staticmethod
    def visit_literal(node) -> int:
        """
        Visit AST literal node.
        :param node: The AST literal node to visit.
        :return: Zero.
        """
        return 0

    def visit_statement(self, node) -> int:
        """
        Visit AST statement node.
        :param node: The AST statement node to visit.
        :return: 1 + the number of statements in the statement's subtree.
        """
        return 1 + self.visit_children(node)
