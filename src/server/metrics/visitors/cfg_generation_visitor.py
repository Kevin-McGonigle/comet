from metrics.structures.cfg import *
from metrics.visitors.base.ast_visitor import ASTVisitor, ASTNode


class CFGGenerationVisitor(ASTVisitor):
    def __init__(self):
        self.cfg = CFG()
        self.loop_scope = None

    def visit_children(self, node):
        """
        Visit all of a node's children.
        :param node: The node whose children to visit.
        :type node: ASTNode
        :return: A built sequence of CFGNodes returned by visiting each child. None if no CFGNodes returned.
        :rtype: CFGNode or None
        """
        sequence = []
        for child in node.children:
            child_result = child.accept(self)
            if isinstance(child_result, CFGNode):
                sequence.append(child_result)

        return build_sequence(sequence)

    def visit_break_statement(self, node):
        if self.loop_scope is not None:
            return CFGBreakNode(self.loop_scope.exit_block)

        return CFGBreakNode()

    def visit_continue_statement(self, node):
        if self.loop_scope is not None:
            return CFGContinueNode(self.loop_scope)

        return CFGContinueNode()

    def visit_if_statement(self, node):
        condition = node.condition.accept(self)
        body = node.body.accept(self)

        if isinstance(condition, CFGNode):
            condition.exit_block = CFGIfNode(body)
            return condition

        return CFGIfNode(body)

    def visit_if_else_statement(self, node):
        condition = node.condition.accept(self)
        body = node.body.accept(self)
        else_body = node.else_body.accept(self)

        if isinstance(condition, CFGNode):
            condition.exit_block = CFGIfElseNode(body, else_body)
            return condition

        return CFGIfElseNode(body, else_body)

    def visit_loop_statement(self, node):
        condition = node.condition.accept(self)

        outer_loop_scope = self.loop_scope
        self.loop_scope = loop = CFGLoopNode()

        if isinstance(condition, CFGNode):
            condition.exit_block = node.body.accept(self)
            loop.success_block = condition
        else:
            loop.success_block = node.body.accept(self)

        self.loop_scope = outer_loop_scope

        return loop

    def visit_loop_else_statement(self, node):
        outer_loop_scope = self.loop_scope
        self.loop_scope = loop_else = CFGLoopElseNode()

        loop_else.success_block = node.body.accept(self)

        self.loop_scope = outer_loop_scope

        loop_else.fail_block = node.else_body.accept(self)

        return loop_else


def build_sequence(sequence):
    """
    Build sequence of blocks.
    :param sequence: The list of blocks to build into a sequence.
    :type sequence: list[CFGNode] or None
    :return: The first node of the sequence with built sequence as its exit block. None if no/empty sequence supplied.
    :rtype: CFGNode or None
    """
    if not sequence:
        return None

    if len(sequence) > 1:
        sequence[0].exit_block = build_sequence(sequence[1:])

    return sequence[0]
