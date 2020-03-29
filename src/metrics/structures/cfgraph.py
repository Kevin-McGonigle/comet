class CFG(object):
    def __init__(self, entry):
        self.entry = entry
        super().__init__()

    def node_count(self):
        return self.entry.node_count()

    def edge_count(self):
        return self.entry.edge_count()


class CFGNode(object):
    def __init__(self, children=None):
        if children is None:
            self.children = []
        else:
            self.children = children

        super().__init__()

    def add_child(self, child):
        if isinstance(child, CFGNode):
            self.children.append(child)
        else:
            raise ValueError

    def node_count(self, visited=None):
        if visited is None:
            visited = []

        if self in visited:
            return 0

        visited.append(self)
        return 1 + sum([child.node_count(visited) for child in self.children])

    def edge_count(self, visited=None):
        if visited is None:
            visited = []

        if self in visited:
            return 0

        visited.append(self)
        return len(self.children) + sum([child.edge_count(visited) for child in self.children])


class CFGIfNode(CFGNode):
    def __init__(self, success_block=None, exit_block=None):
        if success_block is None:
            success_block = CFGNode()
        self.success_block = success_block

        if exit_block is None:
            exit_block = CFGNode()
        self.exit_block = exit_block

        self.success_block.add_child(self.exit_block)
        super().__init__([self.success_block, self.exit_block])

    def add_child(self, child):
        self.exit_block.add_child(child)


class CFGIfElseNode(CFGNode):
    def __init__(self, success_block=None, fail_block=None, exit_block=None):
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


class CFGWhileNode(CFGNode):
    def __init__(self, success_block=None, exit_block=None):
        if success_block is None:
            success_block = CFGNode()
        self.success_block = success_block

        if exit_block is None:
            exit_block = CFGNode()
        self.exit_block = exit_block

        self.success_block.add_child(self)
        super().__init__([self.success_block, self.exit_block])

    def add_child(self, child):
        self.exit_block.add_child(child)


class CFGWhileElseNode(CFGNode):
    def __init__(self, success_block=None, fail_block=None, exit_block=None):
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


class CFGBreakNode(CFGNode):
    def __init__(self, break_node=None):
        if break_node is None:
            break_node = CFGNode()
        self.break_node = break_node

        super().__init__([self.break_node])


if __name__ == '__main__':
    pass
