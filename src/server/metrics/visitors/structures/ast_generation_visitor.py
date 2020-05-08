from typing import Optional, Sequence, Type

from antlr4 import ParseTreeVisitor, ParserRuleContext
from antlr4.tree.Tree import TerminalNodeImpl

from metrics.structures.ast import AST, ASTNode, ASTMultiplesNode, ASTBinaryOperationNode, ASTUnaryOperationNode, \
    ASTVisibilityModifier


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
    def build_multi(self, sequence: Optional[Sequence[ASTNode]], multi_node: Type[ASTMultiplesNode]):
        if not sequence:
            return self.defaultResult()

        if len(sequence) == 1:
            return sequence[0]

        return multi_node(sequence)

    def build_right_associated(self, sequence: Optional[Sequence[ASTNode]], parent_node: Type[ASTNode]):
        if not sequence:
            return self.defaultResult()

        if len(sequence) == 1:
            return sequence[0]

        return parent_node(sequence[0], self.build_right_associated(sequence[1:], parent_node))

    def build_left_associated(self, sequence: Optional[Sequence[ASTNode]], parent_node: Type[ASTNode]):
        if not sequence:
            return self.defaultResult()

        if len(sequence) == 1:
            return sequence[0]

        return parent_node(self.build_right_associated(sequence[:-1], parent_node), sequence[-1])

    def build_bin_op(self, operation, expressions):
        if len(expressions) == 1:
            return expressions[0]
        return ASTBinaryOperationNode(operation, self.build_bin_op(operation, expressions[:-1]), expressions[-1])

    def build_bin_op_choice(self, children):
        if len(children) == 1:
            return children[0]

        operator = children[-2]
        if isinstance(operator, list):
            return ASTUnaryOperationNode(operator[0],
                                         ASTBinaryOperationNode(operator[1],
                                                                self.build_bin_op_choice(children[:-2]),
                                                                children[-1]))

        return ASTBinaryOperationNode(operator, self.build_bin_op_choice(children[:-2]), children[-1])

    def build_bin_op_rassoc(self, operation, expressions):
        if len(expressions) == 1:
            return expressions[0]
        return ASTBinaryOperationNode(operation, expressions[0],
                                      self.build_bin_op_rassoc(operation, expressions[1:]))

    @staticmethod
    def filter_child(child, *contexts):
        for context in contexts:
            if isinstance(context, int) and isinstance(child, TerminalNodeImpl) and child.symbol.type == context:
                return True
            elif isinstance(context, ParserRuleContext) and isinstance(child, context):
                return True

        return False

    @staticmethod
    def get_visibility(name: str) -> ASTVisibilityModifier:
        """
        Get the corresponding visibility modifier for the member's name; with one leading underscore indicating a
        protected member and two indicating a private member
        (according to the PEP 8 style guide
        https://www.python.org/dev/peps/pep-0008/#method-names-and-instance-variables).

        :param name: The member's name/identifier.
        :return: The corresponding visibility/access modifier.
        """
        if name.startswith("__"):
            return ASTVisibilityModifier.PRIVATE

        if name.startswith("_"):
            return ASTVisibilityModifier.PROTECTED

        return ASTVisibilityModifier.PUBLIC

    # endregion
