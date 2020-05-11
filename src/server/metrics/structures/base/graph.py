class Graph(object):
    def __init__(self, root=None):
        """
        Generic graph.
        :param root: The root node of the graph.
        :type root: Node or None
        """
        self.root = root

    def __str__(self):
        return f"Generic graph.\nRoot: {self.root}"

    def __repr__(self):
        return f"Graph(root={self.root})"

    def accept(self, visitor):
        """
        Accept a graph visitor by passing it to the root node's accept method.
        :param visitor: The graph visitor to accept.
        :type visitor: GraphVisitor
        :return: The result of the accept.
        :rtype: Any
        """
        if isinstance(self.root, Node):
            return self.root.accept(visitor)


class Node(object):
    def __init__(self, *children):
        """
        Generic graph node.
        :param children: The child nodes of the node.
        :type children: Node or str
        """
        self.children = list([child for child in children if child is not None])

    def __str__(self):
        return f"Generic graph node.\nChildren: {self.children}"

    def __repr__(self):
        return f"Node(children={self.children})"

    def accept(self, visitor):
        """
        Accept the visitor and visit the node's children.
        :param visitor: The visitor to accept.
        :type visitor: TreeVisitor
        :return: The result of the accept.
        :rtype: Any
        """
        return visitor.visit_children(self)

    def add_child(self, child):
        """
        Add a child node to the node.
        :param child: The child to add.
        :type child: Node
        """
        if (isinstance(child, Node) and child not in self.children) or isinstance(child, str):
            self.children.append(child)
        elif child in self.children:
            raise ValueError(f"Node.remove_child(child): child is a node and is already a child of the parent node.")
        else:
            raise TypeError(f"Node.remove_child(child): child was not Node or str (child={child}, type={type(child)}).")

    def remove_child(self, child):
        """
        Remove a child node from the node.
        :param child: The child to remove.
        :type child: Node
        """
        if isinstance(child, Node) or isinstance(child, str):
            self.children.remove(child)
        else:
            raise TypeError(f"Node.remove_child(child): child was not Node or str (child={child}, type={type(child)}).")
