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

    def visit_children(self, node):
        """
        Visit each of a node's children.
        :param node: The node whose children to visit.
        :type node: Node
        :return: A dictionary mapping each child to their visit result.
        :rtype: dict[Node, Any]
        """
        return super().visit_children(node)
