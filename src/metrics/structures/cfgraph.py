class CFG(object):
    def __init__(self, entry):
        """
        Initialise a control flow graph.
        :param entry: The entry node for the control flow graph.
        :type entry: CFGNode
        """
        self.entry = entry
        super().__init__()

    def node_count(self):
        """
        Get the number of nodes in the control flow graph.
        :return: Number of nodes in control flow graph.
        """
        return self.entry.node_count()

    def edge_count(self):
        """
        Get the number of edges in the control flow graph.
        :return: Number of nodes in control flow graph.
        """
        return self.entry.edge_count()


class CFGNode(object):
    def __init__(self, children=None):
        """
        Initialise a generic control flow graph node.
        :param children: List of child nodes.
        :type children: list
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
        """
        visited = [self]
        return 1 + sum([child.r_node_count(visited) for child in self.children])

    def r_node_count(self, visited):
        """
        Recursive helper for calculating node count.
        :param visited: Nodes already visited during this count.
        :type visited: list
        :return: 1 + the sum of the node counts of all child nodes. 0 if already visited.
        """
        if self in visited:
            return 0

        visited.append(self)
        return 1 + sum([child.r_node_count(visited) for child in self.children])

    def edge_count(self):
        """
        Get the number of reachable edges for this node (inclusive).
        :return: The number of reachable edges for this node (inclusive).
        """
        visited = [self]
        return len(self.children) + sum([child.r_edge_count(visited) for child in self.children])

    def r_edge_count(self, visited):
        """
        Recursive helper for calculating edge count.
        :param visited: Nodes already visited during this count.
        :type visited: list
        :return: The number of child nodes + the sum of the edge counts for all child nodes. 0 if already visited.
        """
        if self in visited:
            return 0

        visited.append(self)
        return len(self.children) + sum([child.edge_count(visited) for child in self.children])

    def add_child(self, child):
        """
        Add a child to this node.
        :param child: The child to add.
        :type child: CFGNode
        """
        if isinstance(child, CFGNode) and child not in self.children:
            self.children.append(child)
        else:
            raise ValueError


class CFGIfNode(CFGNode):
    def __init__(self, success_block=None, exit_block=None):
        """
        Initialise an if statement control flow graph structure.
        :param success_block: The node to visit if the condition is true.
        :type success_block: CFGNode
        :param exit_block: The node following the if statement.
        :type exit_block: CFGNode
        """
        if success_block is None:
            success_block = CFGNode()
        self.success_block = success_block

        if exit_block is None:
            exit_block = CFGNode()
        self.exit_block = exit_block

        self.success_block.add_child(self.exit_block)
        super().__init__([self.success_block, self.exit_block])

    def add_child(self, child):
        """
        Add a child to the if structure's exit block.
        :param child: The child to add.
        :type child: CFGNode
        """
        self.exit_block.add_child(child)


class CFGIfElseNode(CFGNode):
    def __init__(self, success_block=None, fail_block=None, exit_block=None):
        """
        Initialise an if-else statement control flow graph structure.
        :param success_block: The node to visit if the condition is true.
        :type success_block: CFGNode
        :param fail_block: The node to visit if the condition is false.
        :type fail_block: CFGNode
        :param exit_block: The node following the if-else statement.
        :type exit_block: CFGNode
        """
        if success_block is None:
            success_block = CFGNode()
        self.success_block = success_block

        if fail_block is None:
            fail_block = CFGNode()
        self.fail_block = fail_block

        if exit_block is None:
            exit_block = CFGNode()
        self.exit_block = exit_block

        self.success_block.add_child(self.exit_block)
        self.fail_block.add_child(self.exit_block)
        super().__init__([self.success_block, self.fail_block])

    def add_child(self, child):
        """
        Add child to the if-else structure's exit block.
        :param child: The child to add.
        :type child: CFGNode
        """
        self.exit_block.add_child(child)


class CFGWhileNode(CFGNode):
    def __init__(self, success_block=None, exit_block=None):
        """
        Initialise a while statement control flow graph structure.
        :param success_block: The node to visit if the condition is true.
        :type success_block: CFGNode
        :param exit_block: The node to following the while statement.
        :type exit_block: CFGNode
        """
        if success_block is None:
            success_block = CFGNode()
        self.success_block = success_block

        if exit_block is None:
            exit_block = CFGNode()
        self.exit_block = exit_block

        self.success_block.add_child(self)
        super().__init__([self.success_block, self.exit_block])

    def add_child(self, child):
        """
        Add a child to the while structure's exit block.
        :param child: The child to add.
        :type child: CFGNode
        """
        self.exit_block.add_child(child)


class CFGWhileElseNode(CFGNode):
    def __init__(self, success_block=None, fail_block=None, exit_block=None):
        """
        Initialise a while-else statement control flow graph structure.
        :param success_block: The node to visit if the condition is true.
        :type success_block: CFGNode
        :param fail_block: The node to visit if the condition is false.
        :type fail_block: CFGNode
        :param exit_block: The node following the while-else statement.
        :type exit_block: CFGNode
        """
        if success_block is None:
            success_block = CFGNode()
        self.success_block = success_block

        if fail_block is None:
            fail_block = CFGNode()
        self.fail_block = fail_block

        if exit_block is None:
            exit_block = CFGNode()
        self.exit_block = exit_block

        self.success_block.add_child(self)
        self.fail_block.add_child(self.exit_block)

        super().__init__([self.success_block, self.fail_block])

    def add_child(self, child):
        """
        Add a child to the while-else structure's exit block.
        :param child: The child to add.
        :type child: CFGNode
        """
        self.exit_block.add_child(child)


class CFGBreakNode(CFGNode):
    def __init__(self, break_to_block=None):
        """
        Initialise a breaks statement control flow graph structure.
        :param break_to_block: The node to break to.
        :type break_to_block: CFGNode
        """
        if break_to_block is None:
            break_to_block = CFGNode()
        self.break_to_block = break_to_block

        super().__init__([self.break_to_block])

    def add_child(self, child):
        """
        Add a child to the break structure's break-to block.
        :param child: The child to add.
        :type child: CFGNode
        """
        self.break_to_block.add_child(child)


if __name__ == '__main__':
    pass
