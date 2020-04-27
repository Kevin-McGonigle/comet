class Graph(object):
    def __init__(self, entry=None):
        """
        Generic graph.
        :param entry: The entry node of the graph.
        :type entry: Node or None
        """
        self.entry = entry

    def __str__(self):
        s = "Graph"

        if self.entry:
            s += f"\nEntry: {self.entry}"

        return s

    def __repr__(self):
        return "Graph"

    def accept(self, visitor):
        """
        Accept a graph visitor and visit the entry node's children.
        :param visitor: The graph visitor to accept.
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
        s = "Node"

        if self.children:
            s += f"\nChildren: {self.children}"

        return s

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
