class Graph(object):
    def __init__(self, entry=None):
        """
        Generic graph.
        :param entry: The entry node of the graph.
        :type entry: Node or None
        """
        self.entry = entry

    def __str__(self):
        return f"Entry: {self.entry}"

    def accept(self, visitor):
        """
        Accept a visitor and visit the entry node's children.
        :param visitor: The visitor to accept.
        :type visitor: GraphVisitor
        :return: The result of the accept.
        :rtype: Any
        """
        if isinstance(self.entry, Node):
            return self.entry.accept(visitor)


class Node(object):
    def __init__(self, *children):
        """
        Generic graph node.
        :param children: The child nodes of the node.
        :type children: Node
        """
        self.children = list(children)

    def __str__(self):
        return f"Children: {self.children}"

    def accept(self, visitor):
        """
        Accept the visitor and visit this node's children.
        :param visitor: The visitor to accept.
        :type visitor: TreeVisitor
        :return: The result of the accept.
        :rtype: Any
        """
        return visitor.visit_children(self)

    def add_child(self, child):
        """
        Add a child node to this node.
        :param child: The child to add.
        :type child: Node
        """
        if isinstance(child, Node) and child not in self.children:
            self.children.append(child)
        else:
            raise ValueError

    def remove_child(self, child):
        """
        Remove a child node from this node.
        :param child: The child to remove.
        :type child: Node
        """
        if isinstance(child, Node) and child in self.children:
            self.children.remove(child)
        else:
            raise ValueError
