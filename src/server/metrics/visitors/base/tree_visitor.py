from metrics.visitors.base.graph_visitor import GraphVisitor
from metrics.structures.base.tree import Tree


class TreeVisitor(GraphVisitor):
    def visit(self, tree):
        """
        Visit a tree structure.
        :param tree: The tree to visit.
        :type tree: Tree
        :return: The output of the visiting process.
        :rtype: Any
        """
        return super().visit(tree)
