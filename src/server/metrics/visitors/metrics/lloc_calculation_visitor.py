from metrics.structures.ast import ASTStatementNode
from metrics.visitors.base.ast_visitor import ASTVisitor


class LLOCCalculationVisitor(ASTVisitor):
    def visit_children(self, node):
        return 1 + sum([child.accept(self) for child in node.children]) if isinstance(node, ASTStatementNode) else \
            sum([child.accept(self) for child in node.children])
