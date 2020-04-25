from metrics.structures.base.graph import Graph, Node as GraphNode
from metrics.visitors.base.tree_visitor import TreeVisitor


class Tree(Graph):
    def __init__(self, root=None):
        """
        Generic tree.
        :param root: The root node of the tree.
        :type root: Node or None
        """
        super().__init__(root)

    def __str__(self):
        s = "Tree"

        if self.root:
            s += f"\nRoot: {self.root}"

        return s

    @property
    def root(self):
        """
        Getter for root property.
        :return: The root node of the tree.
        :rtype: Node or None
        """
        return self.entry

    @root.setter
    def root(self, new_root):
        """
        Setter for root property.
        :param new_root: The value to assign to root.
        :type new_root: Node or None
        """
        self.entry = new_root

    @root.deleter
    def root(self):
        """
        Deleter for root property.
        """
        del self.entry

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
        s = "Node"

        if self.name:
            s += f"\nName: {self.name}"

        if self.children:
            s += f"\nChildren: {self.children}"

        return s

    def __repr__(self):
        return self.name
