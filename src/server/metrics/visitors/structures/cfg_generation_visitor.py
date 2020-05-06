from typing import Optional, Sequence

from metrics.structures.cfg import *
from metrics.visitors.base.ast_visitor import ASTVisitor


class CFGGenerationVisitor(ASTVisitor):
    """
    Control-flow graph generation visitor.

    Provides functionality for visiting an abstract syntax tree and generating the corresponding control-flow graph.
    """

    def __init__(self):
        """
        Control-flow graph generation visitor.
        """
        self.loop_scope = None

    # region Helpers

    def build_sequence(self, sequence: Optional[Sequence[CFGBlock]]) -> Optional[CFGBlock]:
        """
        Build sequence of blocks.
        :param sequence: The list of blocks to build into a sequence.
        :return: The first node of the sequence with built sequence as its exit block.
        None if no/empty sequence supplied.
        """
        if not sequence:
            return None

        if len(sequence) > 1:
            sequence[0].add_child(self.build_sequence(sequence[1:]))

        return sequence[0]

    # endregion

    # region Visits

    def visit(self, ast) -> CFG:
        """
        Visit the AST and produce a CFG.
        :param ast: The AST to visit.
        :return: The generated CFG.
        """
        return CFG(super().visit(ast))

    def visit_children(self, node) -> Optional[CFGBlock]:
        """
        Visit each of an AST node's children.
        :param node: The parent AST node whose children to visit.
        :return: A built sequence of CFGNodes returned by visiting each child. None if no CFGNodes returned.
        """
        sequence = []
        for child in node.children:
            child_result = child.accept(self)
            if isinstance(child_result, CFGBlock):
                sequence.append(child_result)

        return self.build_sequence(sequence)

    def visit_break_statement(self, node) -> CFGBreakBlock:
        """
        Visit AST break statement node and return the corresponding CFG block.
        :param node: The AST break statement node to visit.
        :return: The corresponding CFG block.
        """
        if self.loop_scope is not None:
            return CFGBreakBlock(self.loop_scope.exit_block)

        return CFGBreakBlock()

    def visit_continue_statement(self, node) -> CFGContinueBlock:
        """
        Visit AST continue statement node and return the corresponding CFG block.
        :param node: The AST continue statement node to visit.
        :return: The corresponding CFG block.
        """
        if self.loop_scope is not None:
            return CFGContinueBlock(self.loop_scope)

        return CFGContinueBlock()

    def visit_if_statement(self, node) -> CFGIfBlock:
        """
        Visit AST if statement node and return the corresponding CFG block.
        :param node: The AST if statement node to visit.
        :return: The corresponding CFG block.
        """
        return CFGIfBlock(node.body.accept(self))

    def visit_if_else_statement(self, node) -> CFGIfElseBlock:
        """
        Visit AST if-else statement node and return the corresponding CFG block.
        :param node: The AST if-else statement node to visit.
        :return: The corresponding CFG block.
        """
        return CFGIfElseBlock(node.body.accept(self), node.else_body.accept(self))

    def visit_loop_statement(self, node) -> CFGLoopBlock:
        """
        Visit AST loop statement node and return the corresponding CFG block.
        :param node: The AST loop statement node to visit.
        :return: The corresponding CFG block.
        """
        outer_loop_scope = self.loop_scope
        self.loop_scope = loop = CFGLoopBlock()

        loop.success_block = node.body.accept(self)

        self.loop_scope = outer_loop_scope

        return loop

    def visit_loop_else_statement(self, node) -> CFGLoopElseBlock:
        """
        Visit AST loop-else statement node and return the corresponding CFG block.
        :param node: The AST loop-else statement node to visit.
        :return: The corresponding CFG block.
        """
        outer_loop_scope = self.loop_scope
        self.loop_scope = loop_else = CFGLoopElseBlock()

        loop_else.success_block = node.body.accept(self)

        self.loop_scope = outer_loop_scope

        loop_else.fail_block = node.else_body.accept(self)

        return loop_else

    # endregion
