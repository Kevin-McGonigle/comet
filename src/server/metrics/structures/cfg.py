from metrics.structures.base.graph import *


class CFG(Graph):
    def cyclomatic_complexity(self):
        connected_components_count = 1
        return self.edge_count() - self.node_count() + 2 * connected_components_count


class CFGNode(Node):
    _exit_block = None

    @property
    def exit_block(self):
        """
        Getter for exit_node property.
        :return: Value of exit_node.
        :rtype: CFGNode or None
        """
        return self._exit_block

    @exit_block.setter
    def exit_block(self, new_exit_block):
        """
        Setter for exit_node property.
        :param new_exit_block: Value to assign to exit_node.
        :type new_exit_block: CFGNode or None.
        """
        if self.exit_block in self.children:
            self.children.remove(self.exit_block)

        self._exit_block = new_exit_block

        self.children.append(self.exit_block)

    @exit_block.deleter
    def exit_block(self):
        """
        Deleter for exit_node property.
        """
        if self.exit_block in self.children:
            self.children.remove(self.exit_block)

        del self._exit_block


class CFGIfNode(CFGNode):
    def __init__(self, success_block=None, exit_block=None):
        """
        If statement control flow graph structure.
        :param success_block: The node to visit if the condition is true.
        :type success_block: CFGNode or None
        :param exit_block: The node following the if statement.
        :type exit_block: CFGNode or None
        """
        if success_block is None:
            success_block = CFGNode()
        self._success_block = success_block

        if exit_block is None:
            exit_block = CFGNode()
        self._exit_block = exit_block

        self.success_block.add_child(self.exit_block)
        super().__init__(self.success_block, self.exit_block)

    @property
    def success_block(self):
        """
        Getter for success_block property.
        :return: Value of success_block property.
        :rtype: CFGNode
        """
        return self._success_block

    @success_block.setter
    def success_block(self, new_success_block):
        """
        Setter for success_block property.
        :param new_success_block: Value to assign to success_block.
        :type new_success_block: CFGNode
        """
        if self.success_block in self.children:
            self.children.remove(self.success_block)

        self._success_block = new_success_block

        self.success_block.add_child(self.exit_block)

        self.children.append(self.success_block)

    @success_block.deleter
    def success_block(self):
        """
        Deleter for success_block property.
        """
        if self.success_block in self.children:
            self.children.remove(self.success_block)

        del self._success_block

    @property
    def exit_block(self):
        return super().exit_block

    @exit_block.setter
    def exit_block(self, new_exit_block):
        """
        Setter for exit_block property.
        :param new_exit_block: Value to assign to exit_block.
        :type new_exit_block: CFGNode
        """
        if self.exit_block in self.children:
            self.children.remove(self.exit_block)

        self.success_block.remove_child(self.exit_block)

        self._exit_block = new_exit_block

        self.success_block.add_child(self.exit_block)

        self.children.append(self.exit_block)

    @exit_block.deleter
    def exit_block(self):
        """
        Deleter for exit_block property.
        """
        if self.exit_block in self.children:
            self.children.remove(self.exit_block)

        self.success_block.remove_child(self.exit_block)

        del self._exit_block

    def add_child(self, child):
        """
        Add a child to the if structure's exit block.
        :param child: The child to add.
        :type child: CFGNode
        """
        self.exit_block.add_child(child)

    def remove_child(self, child):
        """
        Remove a child from the if structure's exit block.
        :param child: The child to remove.
        :type child: CFGNode
        """
        self.exit_block.remove_child(child)


class CFGIfElseNode(CFGNode):
    def __init__(self, success_block=None, fail_block=None, exit_block=None):
        """
        If-else statement control flow graph structure.
        :param success_block: The node to visit if the condition is true.
        :type success_block: CFGNode or None
        :param fail_block: The node to visit if the condition is false.
        :type fail_block: CFGNode or None
        :param exit_block: The node following the if-else statement.
        :type exit_block: CFGNode or None
        """
        if success_block is None:
            success_block = CFGNode()
        self._success_block = success_block

        if fail_block is None:
            fail_block = CFGNode()
        self._fail_block = fail_block

        if exit_block is None:
            exit_block = CFGNode()
        self._exit_block = exit_block

        self.success_block.add_child(self.exit_block)
        self.fail_block.add_child(self.exit_block)
        super().__init__(self.success_block, self.fail_block)

    @property
    def success_block(self):
        """
        Getter for success_block property.
        :return: Value of success_block.
        :rtype: CFGNode
        """
        return self._success_block

    @success_block.setter
    def success_block(self, new_success_block):
        """
        Setter for success_block property.
        :param new_success_block: Value to assign to success_block.
        :type new_success_block: CFGNode
        """
        if self.success_block in self.children:
            self.children.remove(self.success_block)

        self._success_block = new_success_block

        self.children.append(self.success_block)

    @success_block.deleter
    def success_block(self):
        """
        Deleter for success_block property.
        """
        if self.success_block in self.children:
            self.children.remove(self.success_block)

        del self._success_block

    @property
    def fail_block(self):
        """
        Getter for fail_block property.
        :return: Value of fail_block.
        :rtype: CFGNode
        """
        return self._fail_block

    @fail_block.setter
    def fail_block(self, new_fail_block):
        """
        Setter for fail_block property.
        :param new_fail_block: Value to assign to fail_block.
        :type new_fail_block: CFNode
        """
        if self.fail_block in self.children:
            self.children.remove(self.fail_block)

        self._fail_block = new_fail_block

        self.children.append(self.fail_block)

    @fail_block.deleter
    def fail_block(self):
        """
        Deleter for fail_block property.
        """
        if self.fail_block in self.children:
            self.children.remove(self.fail_block)

        del self._fail_block

    @property
    def exit_block(self):
        return super().exit_block

    @exit_block.setter
    def exit_block(self, new_exit_block):
        """
        Setter for exit_block property.
        :param new_exit_block: Value to assign to exit_block.
        :type new_exit_block: CFGNode
        """
        self.success_block.remove_child(self.exit_block)
        self.fail_block.remove_child(self.exit_block)

        self._exit_block = new_exit_block

        self.success_block.add_child(self.exit_block)
        self.fail_block.add_child(self.exit_block)

    @exit_block.deleter
    def exit_block(self):
        """
        Deleter for exit_block property.
        """
        self.success_block.remove_child(self.exit_block)
        self.fail_block.remove_child(self.exit_block)

        del self._exit_block

    def add_child(self, child):
        """
        Add child to the if-else structure's exit block.
        :param child: The child to add.
        :type child: CFGNode
        """
        self.exit_block.add_child(child)

    def remove_child(self, child):
        """
        Remove child from the if-else structure's exit block.
        :param child: The child to remove.
        :type child: CFGNode
        """
        self.exit_block.remove_child(child)


class CFGLoopNode(CFGNode):
    def __init__(self, success_block=None, exit_block=None):
        """
        Loop control flow graph structure.
        :param success_block: The node to visit if the condition is true.
        :type success_block: CFGNode or None
        :param exit_block: The node to following the while statement.
        :type exit_block: CFGNode or None
        """
        if success_block is None:
            success_block = CFGNode()
        self._success_block = success_block

        if exit_block is None:
            exit_block = CFGNode()
        self._exit_block = exit_block

        self.success_block.add_child(self)
        super().__init__(self.success_block, self.exit_block)

    @property
    def success_block(self):
        """
        Getter for success_block property.
        :return: Value of success_block property.
        :rtype: CFGNode
        """
        return self._success_block

    @success_block.setter
    def success_block(self, new_success_block):
        """
        Setter for success_block property.
        :param new_success_block: Value to assign to success_block.
        :type new_success_block: CFGNode
        """
        if self.success_block in self.children:
            self.children.remove(self.success_block)

        self._success_block = new_success_block

        self.success_block.add_child(self)

        self.children.append(self.success_block)

    @success_block.deleter
    def success_block(self):
        """
        Deleter for success_block property.
        """
        if self.success_block in self.children:
            self.children.remove(self.success_block)

        del self._success_block

    def add_child(self, child):
        """
        Add a child to the while structure's exit block.
        :param child: The child to add.
        :type child: CFGNode
        """
        self.exit_block.add_child(child)

    def remove_child(self, child):
        """
        Remove a child from the while structure's exit block.
        :param child: The child to remove.
        :type child: CFGNode
        """
        self.exit_block.remove_child(child)


class CFGLoopElseNode(CFGNode):
    def __init__(self, success_block=None, fail_block=None, exit_block=None):
        """
        Loop-else control flow graph structure.
        :param success_block: The node to visit if the condition is true.
        :type success_block: CFGNode or None
        :param fail_block: The node to visit if the condition is false.
        :type fail_block: CFGNode or None
        :param exit_block: The node following the while-else statement.
        :type exit_block: CFGNode or None
        """
        if success_block is None:
            success_block = CFGNode()
        self._success_block = success_block

        if fail_block is None:
            fail_block = CFGNode()
        self._fail_block = fail_block

        if exit_block is None:
            exit_block = CFGNode()
        self._exit_block = exit_block

        self.success_block.add_child(self)
        self.fail_block.add_child(self.exit_block)

        super().__init__(self.success_block, self.fail_block)

    @property
    def success_block(self):
        """
        Getter for success_block property.
        :return: Value of success_block property.
        :rtype: CFGNode
        """
        return self._success_block

    @success_block.setter
    def success_block(self, new_success_block):
        """
        Setter for success_block property.
        :param new_success_block: Value to assign to success_block.
        :type new_success_block: CFGNode
        """
        if self.success_block in self.children:
            self.children.remove(self.success_block)

        self._success_block = new_success_block

        self.success_block.add_child(self)

        self.children.append(self.success_block)

    @success_block.deleter
    def success_block(self):
        """
        Deleter for success_block property.
        """
        if self.success_block in self.children:
            self.children.remove(self.success_block)

        del self._success_block

    @property
    def fail_block(self):
        """
        Getter for fail_block property.
        :return: Value of fail_block property.
        :rtype: CFGNode
        """
        return self._fail_block

    @fail_block.setter
    def fail_block(self, new_fail_block):
        """
        Setter for fail_block property.
        :param new_fail_block: Value to assign to fail_block.
        :type new_fail_block: CFGNode
        """
        if self.fail_block in self.children:
            self.children.remove(self.fail_block)

        self._fail_block = new_fail_block

        self.fail_block.add_child(self.exit_block)

        self.children.append(self.fail_block)

    @fail_block.deleter
    def fail_block(self):
        """
        Deleter for fail_block property.
        """
        if self.fail_block in self.children:
            self.children.remove(self.fail_block)

        del self._fail_block

    @property
    def exit_block(self):
        return super().exit_block

    @exit_block.setter
    def exit_block(self, new_exit_block):
        """
        Setter for exit_block property.
        :param new_exit_block: Value to assign to exit_block.
        :type new_exit_block: CFGNode
        """
        self.fail_block.remove_child(self.exit_block)

        self._exit_block = new_exit_block

        self.fail_block.add_child(self.exit_block)

    @exit_block.deleter
    def exit_block(self):
        """
        Deleter for exit_block property.
        """
        self.fail_block.remove_child(self.exit_block)

        del self._exit_block

    def add_child(self, child):
        """
        Add a child to the while-else structure's exit block.
        :param child: The child to add.
        :type child: CFGNode
        """
        self.exit_block.add_child(child)

    def remove_child(self, child):
        """
        Remove a child from the while-else structure's exit block.
        :param child: The child to remove.
        :type child: CFGNode
        """
        self.exit_block.remove_child(child)


class CFGSwitchNode(CFGNode):
    def __init__(self, case_blocks, exit_block=None):
        """
        Switch statement control flow graph structure.
        :param case_blocks: The nodes representing each respective case.
        :type case_blocks: list[CFGNode]
        :param exit_block: The node following the switch statement.
        :type exit_block: CFGNode or None
        """
        self._case_blocks = case_blocks

        if exit_block is None:
            exit_block = CFGNode
        self._exit_block = exit_block

        for case_block in self.case_blocks:
            case_block.add_child(self.exit_block)

        super().__init__(*self.case_blocks)

    @property
    def case_blocks(self):
        """
        Getter for case_blocks property.
        :return: Value of case_blocks property.
        :rtype: list[CFGNode] or None
        """
        return self._case_blocks

    @case_blocks.setter
    def case_blocks(self, new_case_blocks):
        """
        Setter for case_blocks property.
        :param new_case_blocks: The value to assign to case_blocks.
        :type new_case_blocks: list[CFGNode] or None
        """
        if self.case_blocks:
            for case_block in self.case_blocks:
                if case_block in self.children:
                    self.children.remove(case_block)

        self._case_blocks = new_case_blocks

        if self.case_blocks:
            if self.exit_block:
                for case_block in self.case_blocks:
                    case_block.add_child(self.exit_block)

            self.children.extend(self.case_blocks)

    @case_blocks.deleter
    def case_blocks(self):
        """
        Deleter for case_block property.
        """
        if self.case_blocks:
            for case_block in self.case_blocks:
                if case_block in self.children:
                    self.children.remove(case_block)

        del self._case_blocks

    @property
    def exit_block(self):
        return super().exit_block

    @exit_block.setter
    def exit_block(self, new_exit_block):
        """
        Setter for exit_block property.
        :param new_exit_block: The value to assign to exit_block.
        :type new_exit_block: CFGNode or None
        :return:
        :rtype:
        """
        if self.case_blocks and self.exit_block:
            for case_block in self.case_blocks:
                case_block.remove_child(self.exit_block)

        self._exit_block = new_exit_block

        if self.case_blocks and self.exit_block:
            for case_block in self.case_blocks:
                case_block.add_child(self.exit_block)

    @exit_block.deleter
    def exit_block(self):
        """
        Deleter for exit_block property.
        """
        if self.case_blocks and self.exit_block:
            for case_block in self.case_blocks:
                case_block.remove_child(self.exit_block)

        del self._exit_block

    def add_child(self, child):
        """
        Add a child to the switch structure's exit block.
        :param child: The child to add.
        :type child: CFGNode
        """
        self.exit_block.add_child(child)

    def remove_child(self, child):
        """
        Remove a child from the switch structure's exit block.
        :param child: The child to remove.
        :type child: CFGNode
        """
        self.exit_block.remove_child(child)


class CFGBreakNode(CFGNode):
    def __init__(self, exit_block=None):
        """
        Break statement control flow graph structure.
        :param exit_block: The block to break to.
        :type exit_block: CFGNode or None
        """
        self._exit_block = exit_block
        super().__init__(self.exit_block)

    # TODO: Evaluate whether "add/remove child" is a valid operation for break blocks.
    def add_child(self, child):
        """
        Add a child to the break structure's exit block.
        :param child: The child to add.
        :type child: CFGNode
        """
        self.exit_block.add_child(child)

    def remove_child(self, child):
        """
        Remove a child from the break structure's exit block.
        :param child: The child to remove.
        :type child: CFGNode
        """
        self.exit_block.remove_child(child)


class CFGContinueNode(CFGNode):
    def __init__(self, exit_block=None):
        """
        Continue statement control flow graph structure.
        :param exit_block: The encapsulating loop of the continue statement.
        :type exit_block: CFGNode or None
        """
        self._exit_block = exit_block
        super().__init__(self.exit_block)

    # TODO: Evaluate whether "add/remove child" is a valid operation for continue blocks.
    def add_child(self, child):
        """
        Add a child to the continue structure's encapsulating loop.
        :param child: The child to add.
        :type child: CFGNode
        """
        self.exit_block.add_child(child)

    def remove_child(self, child):
        """
        Remove a child from the continue structure's encapsulating loop.
        :param child: The child to remove.
        :type child: CFGNode
        """
        self.exit_block.remove_child(child)


if __name__ == '__main__':
    pass
