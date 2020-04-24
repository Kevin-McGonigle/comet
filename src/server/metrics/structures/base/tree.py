from metrics.structures.base.graph import Graph, Node as GraphNode
from metrics.visitors.base.tree_visitor import TreeVisitor


class Tree(Graph):
    def __init__(self, root=None):
        """
        Generic tree.
        :param root: The root node of the tree.
        :type root: Node
        """
        super().__init__(root)

    def __str__(self):
        return f"Root: {self.entry}"

    def accept(self, visitor):
        """
        Accept a visitor.
        :param visitor: The visitor to accept.
        :type visitor: TreeVisitor
        :return: The result of the accept.
        :rtype: Any
        """
        return super().accept(visitor)


class Node(GraphNode):
    def __init__(self, name, *children):
        """
        Generic tree node.
        :param name: The name of the node.
        :type name: str
        :param children: The child nodes of the node.
        :type children: Node
        """
        self.name = name
        super().__init__(*children)

    def __str__(self):
        return f"Name: {self.name}, Children: {self.children}"
