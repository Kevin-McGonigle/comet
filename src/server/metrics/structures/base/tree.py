from metrics.visitors.base.visitor import Visitor


class Tree(object):
    def __init__(self, root=None):
        """
        Initialise a generic tree.
        :param root: The root node of the tree.
        :type root: Node
        """
        self.root = root
        super().__init__()

    def __str__(self):
        return f"Root: {self.root}"

    def accept(self, visitor):
        return self.root.accept(visitor)


class Node(object):
    def __init__(self, name, *children):
        """
        Initialise a generic tree node.
        :param name: The name of the node.
        :type name: str
        :param children: The child nodes of the node.
        :type children: Node or str
        """
        self.name = name
        self.children = children
        super().__init__()

    def __str__(self):
        return f"Node: {self.name}, Children: {self.children}"

    def accept(self, visitor):
        """
        Accept the visitor and visit this node's children.
        :param visitor: The visitor to accept.
        :type visitor: Visitor
        :return: The result of the accept.
        :rtype: Any
        """
        return visitor.visit_children(self)
