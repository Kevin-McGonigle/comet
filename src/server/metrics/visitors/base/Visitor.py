from metrics.structures.base.tree import Node


class Visitor(object):
    def visit(self, tree):
        return tree.accept(self)

    def visit_children(self, node):
        """
        Visit all of a node's children.
        :param node: The node whose children to visit.
        :type node: Node
        :return: A dictionary mapping each child to their visit result.
        :rtype: dict[Node, Any]
        """
        results = {}
        for child in node.children:
            results[child] = child.accept(self)
