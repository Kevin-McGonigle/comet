from metrics.structures.base.graph import *


class CFG(Graph):
    pass


class CFGNode(Node):
    pass


class CFGIfNode(CFGNode):
    def __init__(self, success_block=None, exit_block=None):
        """
        If statement control flow graph structure.
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
        super().__init__(self.success_block, self.exit_block)

    def add_child(self, child):
        """
        Add a child to the if structure's exit block.
        :param child: The child to add.
        :type child: CFGNode
        """
        self.exit_block.add_child(child)


class CFGIfElseNode(CFGNode):
    def __init__(self, success_block, fail_block, exit_block=None):
        """
        If-else statement control flow graph structure.
        :param success_block: The node to visit if the condition is true.
        :type success_block: CFGNode
        :param fail_block: The node to visit if the condition is false.
        :type fail_block: CFGNode
        :param exit_block: The node following the if-else statement.
        :type exit_block: CFGNode or None
        """
        self.success_block = success_block
        self.fail_block = fail_block

        if exit_block is None:
            exit_block = CFGNode()
        self.exit_block = exit_block

        self.success_block.add_child(self.exit_block)
        self.fail_block.add_child(self.exit_block)
        super().__init__(self.success_block, self.fail_block)

    def add_child(self, child):
        """
        Add child to the if-else structure's exit block.
        :param child: The child to add.
        :type child: CFGNode
        """
        self.exit_block.add_child(child)


class CFGLoopNode(CFGNode):
    def __init__(self, success_block, exit_block=None):
        """
        Loop control flow graph structure.
        :param success_block: The node to visit if the condition is true.
        :type success_block: CFGNode
        :param exit_block: The node to following the while statement.
        :type exit_block: CFGNode or None
        """
        self.success_block = success_block

        if exit_block is None:
            exit_block = CFGNode()
        self.exit_block = exit_block

        self.success_block.add_child(self)
        super().__init__(self.success_block, self.exit_block)

    def add_child(self, child):
        """
        Add a child to the while structure's exit block.
        :param child: The child to add.
        :type child: CFGNode
        """
        self.exit_block.add_child(child)


class CFGLoopElseNode(CFGNode):
    def __init__(self, success_block, fail_block, exit_block=None):
        """
        Loop-else control flow graph structure.
        :param success_block: The node to visit if the condition is true.
        :type success_block: CFGNode
        :param fail_block: The node to visit if the condition is false.
        :type fail_block: CFGNode
        :param exit_block: The node following the while-else statement.
        :type exit_block: CFGNode or None
        """
        self.success_block = success_block
        self.fail_block = fail_block

        if exit_block is None:
            exit_block = CFGNode()
        self.exit_block = exit_block

        self.success_block.add_child(self)
        self.fail_block.add_child(self.exit_block)

        super().__init__(self.success_block, self.fail_block)

    def add_child(self, child):
        """
        Add a child to the while-else structure's exit block.
        :param child: The child to add.
        :type child: CFGNode
        """
        self.exit_block.add_child(child)


class CFGSwitchNode(CFGNode):
    def __init__(self, case_blocks, exit_block=None):
        """
        Switch statement control flow graph structure.
        :param case_blocks: The nodes representing each respective case.
        :type case_blocks: list[CFGNode]
        :param exit_block: The node following the switch statement.
        :type exit_block: CFGNode or None
        """
        self.case_blocks = case_blocks

        if exit_block is None:
            exit_block = CFGNode
        self.exit_block = exit_block

        for case_block in self.case_blocks:
            case_block.add_child(self.exit_block)

        super().__init__(*self.case_blocks)

    def add_child(self, child):
        """
        Add a child to the switch structure's exit block.
        :param child: The child to add.
        :type child: CFGNode
        """
        self.exit_block.add_child(child)


class CFGBreakNode(CFGNode):
    def __init__(self, break_to_block=None):
        """
        Break statement control flow graph structure.
        :param break_to_block: The node to break to.
        :type break_to_block: CFGNode
        """
        if break_to_block is None:
            break_to_block = CFGNode()
        self.break_to_block = break_to_block

        super().__init__(self.break_to_block)

    def add_child(self, child):
        """
        Add a child to the break structure's break-to block.
        :param child: The child to add.
        :type child: CFGNode
        """
        self.break_to_block.add_child(child)


class CFGContinueNode(CFGNode):
    def __init__(self, loop=None):
        """
        Continue statement control flow graph structure.
        :param loop: The root node of the encapsulating loop of the continue statement.
        :type loop: CFGNode or None
        """

        self.loop = loop
        super().__init__(loop)

    def add_child(self, child):
        """
        Add a child to the continue structure's encapsulating loop.
        :param child: The child to add
        :type child: CFGNode
        """
        self.loop.add_child(child)


if __name__ == '__main__':
    pass
