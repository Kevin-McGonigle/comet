class TreeVisitor(object):
    def visit(self, tree):
        """
        Visit a tree structure in a top-down manner, starting from the root.
        :param tree: The tree to visit.
        :type tree: Tree
        :return: The output of the visiting process.
        :rtype: Any
        """
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

        return results
