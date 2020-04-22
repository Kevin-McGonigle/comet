from metrics.structures.cfg import *
from metrics.visitors.base.ast_visitor import ASTVisitor, ASTNode


# TODO: Figure out how exit blocks are going to be done. Maybe by passing them down as children are visited,
#  maintaining some kind of global variable that manages scope or by changing CFGNode to have an "add_exit_block"
#  method so that they can be added after-the-fact.


class CFGGenerationVisitor(ASTVisitor):
    def __init__(self):
        self.cfg = CFG()

    def visit(self, tree):
        return super().visit(tree)

    def visit_children(self, node):
        """
        Visit all of a node's children.
        :param node: The node whose children to visit.
        :type node: ASTNode
        :return: The first CFGNode instance returned by visiting children. None if no CFGNodes returned.
        :rtype: CFGNode or None
        """
        for child in node.children:
            child_result = child.accept(self)
            if isinstance(child_result, CFGNode):
                return child_result

        return None

    def visit_break_statement(self, node):
        return CFGBreakNode()

    def visit_continue_statement(self, node):
        return CFGContinueNode()

    def visit_if_statement(self, node):
        return CFGIfNode(node.body.accept(self))

    def visit_if_else_statement(self, node):
        return CFGIfElseNode(node.body.accept(self), node.else_body.accept(self))

    def visit_loop_statement(self, node):
        return CFGLoopNode(node.body.accept(self))

    def visit_loop_else_statement(self, node):
        return CFGLoopElseNode(node.body.accept(self), node.else_body.accept(self))
