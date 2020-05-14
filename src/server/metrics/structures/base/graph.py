from typing import Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from metrics.visitors.base.graph_visitor import GraphVisitor


class Graph(object):
    def __init__(self, root: Optional["Node"] = None):
        """
        Generic graph.

        :param root: The root node of the graph.
        """
        self.root = root

    def __str__(self):
        return f"Generic graph.\nRoot: {self.root}"

    def __repr__(self):
        return f"Graph(root={self.root})"

    def accept(self, visitor: "GraphVisitor") -> Any:
        """
        Accept a graph visitor by passing it to the root node's accept method.

        :param visitor: The graph visitor to accept.
        :return: The result of the accept.
        """
        if isinstance(self.root, Node):
            return self.root.accept(visitor)


class Node(object):
    def __init__(self, *children: "Node"):
        """
        Generic graph node.

        :param children: The child nodes of the node.
        """
        self.children = list([child for child in children if child is not None])

    def __str__(self):
        return f"Generic graph node.\nChildren: {self.children}"

    def __repr__(self):
        return f"Node(children={self.children})"

    def accept(self, visitor: "GraphVisitor") -> Any:
        """
        Accept the visitor and visit the node's children.

        :param visitor: The visitor to accept.
        :return: The result of the accept.
        """
        return visitor.visit_children(self)

    def add_child(self, child: "Node") -> None:
        """
        Add a child node to the node.

        :param child: The child to add.
        """
        if isinstance(child, Node) and child not in self.children:
            self.children.append(child)
        elif not isinstance(child, Node):
            raise TypeError(f"Node.remove_child(child): child is not Node (child={child}, type={type(child)}).")
        else:
            raise ValueError(f"Node.remove_child(child): supplied child is already a child of the parent node.")

    def remove_child(self, child: "Node") -> None:
        """
        Remove a child node from the node.

        :param child: The child to remove.
        """
        if isinstance(child, Node) and child in self.children:
            self.children.remove(child)
        elif not isinstance(child, Node):
            raise TypeError(f"Node.remove_child(child): child is not Node (child={child}, type={type(child)}).")
        else:
            raise ValueError(f"Node.remove_child(child): supplied child is not a child of the parent node.")
