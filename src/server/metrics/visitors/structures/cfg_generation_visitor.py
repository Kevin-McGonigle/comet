# TODO: Work on creating connected components based on different packages/classes/methods

from metrics.structures.cfg import *
from metrics.visitors.base.ast_visitor import ASTVisitor

if TYPE_CHECKING:
    from metrics.structures.ast import AST, ASTNode


class CFGGenerationVisitor(ASTVisitor):
    def __init__(self):
        """
        CFG generation visitor.
        """
        self.loop_scope = None

    def visit(self, ast):
        """
        Visit the AST and produce a CFG.
        :param ast: The AST to visit.
        :type ast: AST
        :return: The generated CFG.
        :rtype: CFG
        """
        return CFG(super().visit(ast))

    def visit_children(self, node):
        """
        Visit all of a node's children.
        :param node: The node whose children to visit.
        :type node: ASTNode
        :return: A built sequence of CFGNodes returned by visiting each child. None if no CFGNodes returned.
        :rtype: CFGBlock or None
        """
        sequence = []
        for child in node.children:
            child_result = child.accept(self)
            if isinstance(child_result, CFGBlock):
                sequence.append(child_result)

        return build_sequence(sequence)

    def visit_break_statement(self, node):
        if self.loop_scope is not None:
            return CFGBreakBlock(self.loop_scope.exit_block)

        return CFGBreakBlock()

    def visit_continue_statement(self, node):
        if self.loop_scope is not None:
            return CFGContinueBlock(self.loop_scope)

        return CFGContinueBlock()

    def visit_if_statement(self, node):
        condition = node.condition.accept(self)
        body = node.body.accept(self)

        if isinstance(condition, CFGBlock):
            condition.exit_block = CFGIfBlock(body)
            return condition

        return CFGIfBlock(body)

    def visit_if_else_statement(self, node):
        condition = node.condition.accept(self)
        body = node.body.accept(self)
        else_body = node.else_body.accept(self)

        if isinstance(condition, CFGBlock):
            condition.exit_block = CFGIfElseBlock(body, else_body)
            return condition

        return CFGIfElseBlock(body, else_body)

    def visit_loop_statement(self, node):
        condition = node.condition.accept(self)

        outer_loop_scope = self.loop_scope
        self.loop_scope = loop = CFGLoopBlock()

        if isinstance(condition, CFGBlock):
            condition.exit_block = node.body.accept(self)
            loop.success_block = condition
        else:
            loop.success_block = node.body.accept(self)

        self.loop_scope = outer_loop_scope

        return loop

    def visit_loop_else_statement(self, node):
        outer_loop_scope = self.loop_scope
        self.loop_scope = loop_else = CFGLoopElseBlock()

        loop_else.success_block = node.body.accept(self)

        self.loop_scope = outer_loop_scope

        loop_else.fail_block = node.else_body.accept(self)

        return loop_else


def build_sequence(sequence):
    """
    Build sequence of blocks.
    :param sequence: The list of blocks to build into a sequence.
    :type sequence: list[CFGBlock] or None
    :return: The first node of the sequence with built sequence as its exit block. None if no/empty sequence supplied.
    :rtype: CFGBlock or None
    """
    if not sequence:
        return None

    if len(sequence) > 1:
        sequence[0].exit_block = build_sequence(sequence[1:])

    return sequence[0]
