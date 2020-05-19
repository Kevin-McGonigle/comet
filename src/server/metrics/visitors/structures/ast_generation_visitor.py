from typing import Optional, Sequence, Type, Union

from antlr4 import ParserRuleContext, ParseTreeVisitor
from antlr4.tree.Tree import TerminalNodeImpl

from metrics.structures.ast import AST, ASTNode, ASTMultiplesNode, ASTBinaryOperationNode, ASTUnaryOperationNode, \
    ASTOperation


class ASTGenerationVisitor(ParseTreeVisitor):
    # region Behaviour

    def visit(self, tree):
        return AST(super().visit(tree))

    def visitChildren(self, node):
        result = []
        for i in range(node.getChildCount()):
            if not self.shouldVisitNextChild(node, result):
                return result

            result = self.aggregateResult(result, node.getChild(i).accept(self))

        return result

    def visitTerminal(self, node):
        return super().visitTerminal(node)

    def visitErrorNode(self, node):
        return super().visitErrorNode(node)

    def defaultResult(self):
        return super().defaultResult()

    def aggregateResult(self, aggregate, next_result):
        return aggregate + [next_result] if next_result is not None else aggregate

    def shouldVisitNextChild(self, node, current_result):
        return super().shouldVisitNextChild(node, current_result)

    # endregion

    # region Helpers
    def build_multi(self, sequence: Optional[Sequence[ASTNode]], multi_node: Type[ASTMultiplesNode]) -> Optional[
            ASTNode]:
        """
        Build an AST multiples node structure for the supplied sequence.

        :param sequence: The sequence to be represented.
        :param multi_node: The type of multiples node to use.
        :return: The multiples node for the supplied sequence. The single node in the sequence if the sequence has
        only one member. The default result if the sequence is None or empty.
        """
        if not sequence:
            return self.defaultResult()

        if len(sequence) == 1:
            return sequence[0]

        return multi_node(sequence)

    def build_right_associated(self, sequence: Optional[Sequence[ASTNode]], parent_node: Type[ASTNode]):
        """
        Build a right-associated subtree using the supplied sequence and parent node.

        :param sequence: The sequence to be represented.
        :param parent_node: The parent node to use.
        :return: The right-associated subtree for the supplied sequence. The single node in the sequence if
        the sequence has only one member. The default result if the sequence is None or empty.
        """
        if not sequence:
            return self.defaultResult()

        if len(sequence) == 1:
            return sequence[0]

        # noinspection PyArgumentList
        return parent_node(sequence[0], self.build_right_associated(sequence[1:], parent_node))

    def build_left_associated(self, sequence: Optional[Sequence[ASTNode]], parent_node: Type[ASTNode]):
        """
        Build a left-associated subtree using the supplied sequence and parent node.

        :param sequence: The sequence to be represented.
        :param parent_node: The parent node to use.
        :return: The left-associated subtree for the supplied sequence. The single node in the sequence if
        the sequence has only one member. The default result if the sequence is None or empty.
        """
        if not sequence:
            return self.defaultResult()

        if len(sequence) == 1:
            return sequence[0]

        # noinspection PyArgumentList
        return parent_node(self.build_right_associated(sequence[:-1], parent_node), sequence[-1])

    def build_bin_op(self, operation: ASTOperation, expressions: Optional[Sequence[ASTNode]]):
        """
        Build a left-associated subtree using the supplied expressions and binary operation.

        :param operation: The operation to use.
        :param expressions: The expressions to be represented.
        :return: The left-associated subtree for the supplied expressions. The single node in the sequence if
        the sequence has only one member. The default result if the sequence is None or empty.
        """
        if not expressions:
            return self.defaultResult()

        if len(expressions) == 1:
            return expressions[0]

        return ASTBinaryOperationNode(operation, self.build_bin_op(operation, expressions[:-1]), expressions[-1])

    def build_bin_op_choice(self, children: Optional[Sequence]) -> Optional[ASTNode]:
        """
        Build a left-associated subtree using the supplied sequence of expressions and operators.

        :param children: The sequence of expressions and operators to be represented.
        :return: The left-associated subtree for the supplied expressions. The single node in the sequence if
        the sequence has only one member. The default result if the sequence is None or empty.
        """
        if not children:
            return self.defaultResult()

        if len(children) == 1:
            return children[0]

        operator = children[-2]
        if isinstance(operator, list):
            return ASTUnaryOperationNode(operator[0],
                                         ASTBinaryOperationNode(operator[1],
                                                                self.build_bin_op_choice(children[:-2]),
                                                                children[-1]))

        return ASTBinaryOperationNode(operator, self.build_bin_op_choice(children[:-2]), children[-1])

    def build_bin_op_rassoc(self, operation: [ASTOperation],
                            expressions: Optional[Union[Sequence[ASTNode], ASTNode]]) -> Optional[ASTNode]:
        """
        Build a right-associated subtree using the supplied expressions and binary operation.

        :param operation: The operation to use.
        :param expressions: The expressions to be represented.
        :return: The right-associated subtree for the supplied expressions. The single node in the sequence if
        the sequence has only one member. The default result if the sequence is None or empty.
        """
        if not expressions:
            return self.defaultResult()

        if len(expressions) == 1:
            return expressions[0]

        return ASTBinaryOperationNode(operation, expressions[0],
                                      self.build_bin_op_rassoc(operation, expressions[1:]))

    @staticmethod
    def filter_child(child, *contexts):
        """
        Check whether or not the supplied child is an instance of one of the supplied parse rule contexts or
        terminal nodes.

        :param child: The child to be filtered.
        :param contexts: The contexts and terminal nodes to check.
        :return: Whether or not the child is an instance of one of the supplied contexts.
        """
        for context in contexts:
            if isinstance(context, int) and isinstance(child, TerminalNodeImpl) and child.symbol.type == context:
                return True
            elif isinstance(context, type) and issubclass(context, ParserRuleContext) and isinstance(child, context):
                return True

        return False

    # endregion
