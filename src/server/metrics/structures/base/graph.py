class Graph(object):
    def __init__(self, entry):
        """
        Initialise a generic graph.
        :param entry: The entry node of the graph.
        :type entry: Node
        """
        super().__init__()
        self.entry = entry

    def node_count(self):
        """
        Get the number of nodes in the graph.
        :return: Number of nodes in graph.
        :rtype: int
        """
        return self.entry.node_count()

    def edge_count(self):
        """
        Get the number of edges in the graph.
        :return: Number of nodes in graph.
        :rtype: int
        """
        return self.entry.edge_count()


class Node(object):
    def __init__(self, children=None):
        """
        Initialise a generic graph node.
        :param children: List of child nodes.
        :type children: List[Node]
        """
        if children is None:
            self.children = []
        else:
            self.children = children

        super().__init__()

    def node_count(self):
        """
        Get the number of reachable nodes for this node (inclusive).
        :return: The number of reachable nodes for this node (inclusive).
        :rtype: int
        """
        visited = [self]
        return 1 + sum([child.r_node_count(visited) for child in self.children])

    def r_node_count(self, visited):
        """
        Recursive helper for calculating node count.
        :param visited: Nodes already visited during this count.
        :type visited: List[Node]
        :return: 1 + the sum of the node counts of all child nodes. 0 if already visited.
        :rtype: int
        """
        if self in visited:
            return 0

        visited.append(self)
        return 1 + sum([child.r_node_count(visited) for child in self.children])

    def edge_count(self):
        """
        Get the number of reachable edges for this node (inclusive).
        :return: The number of reachable edges for this node (inclusive).
        :rtype: int
        """
        visited = [self]
        return len(self.children) + sum([child.r_edge_count(visited) for child in self.children])

    def r_edge_count(self, visited):
        """
        Recursive helper for calculating edge count.
        :param visited: Nodes already visited during this count.
        :type visited: List[Node]
        :return: The number of child nodes + the sum of the edge counts for all child nodes. 0 if already visited.
        :rtype: int
        """
        if self in visited:
            return 0

        visited.append(self)
        return len(self.children) + sum([child.r_edge_count(visited) for child in self.children])

    def add_child(self, child):
        """
        Add a child to this node.
        :param child: The child to add.
        :type child: Node
        """
        if isinstance(child, Node) and child not in self.children:
            self.children.append(child)
        else:
            raise ValueError
