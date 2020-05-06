from typing import TYPE_CHECKING

from metrics.structures.base.graph import Graph, Node

if TYPE_CHECKING:
    from metrics.visitors.base.cfg_visitor import CFGVisitor


class CFG(Graph):
    def __init__(self, entry_block=None):
        """
        Control-flow graph.
        :param entry_block: The entry block of the control-flow graph.
        :type entry_block: CFGBlock or None
        """
        super().__init__(entry_block)

    def __str__(self):
        return f"Control-flow graph.\nEntry block: {self.entry_block}"

    def __repr__(self):
        return f"CFG(entry_block={self.entry_block})"

    @property
    def entry_block(self):
        """
        Getter for entry_block property.
        :return: The value of entry_block.
        :rtype: CFGBlock or None
        """
        return self.root

    @entry_block.setter
    def entry_block(self, new_entry):
        """
        Setter for entry_block property.
        :param new_entry: Value to assign to entry_block.
        :type new_entry: CFGBlock or None
        """
        self.root = new_entry

    @entry_block.deleter
    def entry_block(self):
        """
        Deleter for entry_block property.
        """
        del self.root

    def accept(self, visitor):
        """
        Accept a CFG visitor.
        :param visitor: The CFG visitor to accept.
        :type visitor: CFGVisitor
        :return: The result of the accept.
        :rtype: Any
        """
        if isinstance(self.entry_block, CFGBlock):
            return self.entry_block.accept(visitor)


class CFGBlock(Node):
    _exit_block = None

    def __init__(self, *children):
        """
        Basic block.
        :param children: The child blocks of the basic block.
        :type children: CFGBlock
        """
        super().__init__(*children)

    def __str__(self):
        s = f"Basic block.\nChildren: {self.children}\nExit block: {self.exit_block}"

        return s

    def __repr__(self):
        return f"CFGBlock(children={self.children}, exit_block={self.exit_block})"

    @property
    def exit_block(self):
        """
        Getter for exit_block property.
        :return: Value of exit_block.
        :rtype: CFGBlock or None
        """
        return self._exit_block

    @exit_block.setter
    def exit_block(self, new_exit_block):
        """
        Setter for exit_block property.
        :param new_exit_block: Value to assign to exit_block.
        :type new_exit_block: CFGBlock or None.
        """
        if self.exit_block in self.children:
            self.children.remove(self.exit_block)

        self._exit_block = new_exit_block

        if self.exit_block:
            self.children.append(self.exit_block)

    @exit_block.deleter
    def exit_block(self):
        """
        Deleter for exit_block property.
        """
        if self.exit_block in self.children:
            self.children.remove(self.exit_block)

        del self._exit_block

    def accept(self, visitor):
        """
        Accept a CFG visitor and call its visit_block method.
        :param visitor: The CFG visitor to accept.
        :type visitor: CFGVisitor
        :return: The result of the accept.
        :rtype: Any
        """
        return visitor.visit_block(self)


class CFGIfBlock(CFGBlock):
    def __init__(self, success_block=None, exit_block=None):
        """
        If statement control flow graph structure.
        :param success_block: The block to visit if the condition is true.
        :type success_block: CFGBlock or None
        :param exit_block: The block following the if statement.
        :type exit_block: CFGBlock or None
        """
        if success_block is None:
            success_block = CFGBlock()
        self._success_block = success_block

        if exit_block is None:
            exit_block = CFGBlock()
        self._exit_block = exit_block

        self.success_block.exit_block = self.exit_block
        super().__init__(self.success_block, self.exit_block)

    def __str__(self):
        return f"If block.\nSuccess block: {self.success_block}\nExit block: {self.exit_block}"

    def __repr__(self):
        return f"CFGIfBlock(success_block={self.success_block}, exit_block={self.exit_block})"

    @property
    def success_block(self):
        """
        Getter for success_block property.
        :return: Value of success_block property.
        :rtype: CFGBlock
        """
        return self._success_block

    @success_block.setter
    def success_block(self, new_success_block):
        """
        Setter for success_block property.
        :param new_success_block: Value to assign to success_block.
        :type new_success_block: CFGBlock
        """
        if self.success_block in self.children:
            self.children.remove(self.success_block)

        self._success_block = new_success_block

        if self.success_block:
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
        :type new_exit_block: CFGBlock
        """
        if self.exit_block in self.children:
            self.children.remove(self.exit_block)

        self.success_block.remove_child(self.exit_block)

        self._exit_block = new_exit_block

        if self.exit_block:
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

    def accept(self, visitor):
        """
        Accept a CFG visitor and call its visit_if_block method.
        :param visitor: The CFG visitor to accept.
        :type visitor: CFGVisitor
        :return: The result of the accept.
        :rtype: Any
        """
        return visitor.visit_if_block(self)

    def add_child(self, child):
        """
        Add a child to the if structure's exit block.
        :param child: The child to add.
        :type child: CFGBlock
        """
        self.exit_block.add_child(child)

    def remove_child(self, child):
        """
        Remove a child from the if structure's exit block.
        :param child: The child to remove.
        :type child: CFGBlock
        """
        self.exit_block.remove_child(child)


class CFGIfElseBlock(CFGBlock):
    def __init__(self, success_block=None, fail_block=None, exit_block=None):
        """
        If-else statement control flow graph structure.
        :param success_block: The block to visit if the condition is true.
        :type success_block: CFGBlock or None
        :param fail_block: The block to visit if the condition is false.
        :type fail_block: CFGBlock or None
        :param exit_block: The block following the if-else statement.
        :type exit_block: CFGBlock or None
        """
        if success_block is None:
            success_block = CFGBlock()
        self._success_block = success_block

        if fail_block is None:
            fail_block = CFGBlock()
        self._fail_block = fail_block

        if exit_block is None:
            exit_block = CFGBlock()
        self._exit_block = exit_block

        self.success_block.add_child(self.exit_block)
        self.fail_block.add_child(self.exit_block)
        super().__init__(self.success_block, self.fail_block)

    def __str__(self):
        return f"If-else block.\nSuccess block: {self.success_block}\nFail block: {self.fail_block}\n" \
               f"Exit block: {self.exit_block}"

    def __repr__(self):
        return f"CFGIfElseBlock(success_block={self.success_block}, fail_block={self.fail_block}, " \
               f"exit_block={self.exit_block})"

    @property
    def success_block(self):
        """
        Getter for success_block property.
        :return: Value of success_block.
        :rtype: CFGBlock
        """
        return self._success_block

    @success_block.setter
    def success_block(self, new_success_block):
        """
        Setter for success_block property.
        :param new_success_block: Value to assign to success_block.
        :type new_success_block: CFGBlock
        """
        if self.success_block in self.children:
            self.children.remove(self.success_block)

        self._success_block = new_success_block

        if self.success_block:
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
        :rtype: CFGBlock
        """
        return self._fail_block

    @fail_block.setter
    def fail_block(self, new_fail_block):
        """
        Setter for fail_block property.
        :param new_fail_block: Value to assign to fail_block.
        :type new_fail_block: CFGBlock or None
        """
        if self.fail_block in self.children:
            self.children.remove(self.fail_block)

        self._fail_block = new_fail_block

        if self.fail_block:
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
        :type new_exit_block: CFGBlock
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

    def accept(self, visitor):
        """
        Accept a CFG visitor and call its visit_if_else_block method.
        :param visitor: The CFG visitor to accept.
        :type visitor: CFGVisitor
        :return: The result of the accept.
        :rtype: Any
        """
        return visitor.visit_if_else_block(self)

    def add_child(self, child):
        """
        Add child to the if-else structure's exit block.
        :param child: The child to add.
        :type child: CFGBlock
        """
        self.exit_block.add_child(child)

    def remove_child(self, child):
        """
        Remove child from the if-else structure's exit block.
        :param child: The child to remove.
        :type child: CFGBlock
        """
        self.exit_block.remove_child(child)


class CFGLoopBlock(CFGBlock):
    def __init__(self, success_block=None, exit_block=None):
        """
        Loop control flow graph structure.
        :param success_block: The block to visit if the condition is true.
        :type success_block: CFGBlock or None
        :param exit_block: The block to following the while statement.
        :type exit_block: CFGBlock or None
        """
        if success_block is None:
            success_block = CFGBlock()
        self._success_block = success_block

        if exit_block is None:
            exit_block = CFGBlock()
        self._exit_block = exit_block

        self.success_block.add_child(self)
        super().__init__(self.success_block, self.exit_block)

    def __str__(self):
        return f"Loop block.\nSuccess block: {self.success_block}\nExit block: {self.exit_block}"

    def __repr__(self):
        return f"CFGLoopBlock(success_block={self.success_block}, exit_block={self.exit_block})"

    @property
    def success_block(self):
        """
        Getter for success_block property.
        :return: Value of success_block property.
        :rtype: CFGBlock
        """
        return self._success_block

    @success_block.setter
    def success_block(self, new_success_block):
        """
        Setter for success_block property.
        :param new_success_block: Value to assign to success_block.
        :type new_success_block: CFGBlock
        """
        if self.success_block in self.children:
            self.children.remove(self.success_block)

        self._success_block = new_success_block

        if self.success_block:
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

    def accept(self, visitor):
        """
        Accept a CFG visitor and call its visit_loop_block method.
        :param visitor: The CFG visitor to accept.
        :type visitor: CFGVisitor
        :return: The result of the accept.
        :rtype: Any
        """
        return visitor.visit_loop_block(self)

    def add_child(self, child):
        """
        Add a child to the while structure's exit block.
        :param child: The child to add.
        :type child: CFGBlock
        """
        self.exit_block.add_child(child)

    def remove_child(self, child):
        """
        Remove a child from the while structure's exit block.
        :param child: The child to remove.
        :type child: CFGBlock
        """
        self.exit_block.remove_child(child)


class CFGLoopElseBlock(CFGBlock):
    def __init__(self, success_block=None, fail_block=None, exit_block=None):
        """
        Loop-else control flow graph structure.
        :param success_block: The block to visit if the condition is true.
        :type success_block: CFGBlock or None
        :param fail_block: The block to visit if the condition is false.
        :type fail_block: CFGBlock or None
        :param exit_block: The block following the while-else statement.
        :type exit_block: CFGBlock or None
        """
        if success_block is None:
            success_block = CFGBlock()
        self._success_block = success_block

        if fail_block is None:
            fail_block = CFGBlock()
        self._fail_block = fail_block

        if exit_block is None:
            exit_block = CFGBlock()
        self._exit_block = exit_block

        self.success_block.add_child(self)
        self.fail_block.add_child(self.exit_block)

        super().__init__(self.success_block, self.fail_block)

    def __str__(self):
        return f"Loop-else block.\nSuccess block: {self.success_block}\nFail block: {self.fail_block}\n" \
               f"Exit block: {self.exit_block}"

    def __repr__(self):
        return f"CFGLoopElseBlock(success_block={self.success_block}, fail_block={self.fail_block}, " \
               f"exit_block={self.exit_block})"

    @property
    def success_block(self):
        """
        Getter for success_block property.
        :return: Value of success_block property.
        :rtype: CFGBlock
        """
        return self._success_block

    @success_block.setter
    def success_block(self, new_success_block):
        """
        Setter for success_block property.
        :param new_success_block: Value to assign to success_block.
        :type new_success_block: CFGBlock
        """
        if self.success_block in self.children:
            self.children.remove(self.success_block)

        self._success_block = new_success_block

        if self.success_block:
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
        :rtype: CFGBlock
        """
        return self._fail_block

    @fail_block.setter
    def fail_block(self, new_fail_block):
        """
        Setter for fail_block property.
        :param new_fail_block: Value to assign to fail_block.
        :type new_fail_block: CFGBlock
        """
        if self.fail_block in self.children:
            self.children.remove(self.fail_block)

        self._fail_block = new_fail_block

        if self.fail_block:
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
        :type new_exit_block: CFGBlock
        """
        self.fail_block.remove_child(self.exit_block)

        self._exit_block = new_exit_block

        if self.exit_block:
            self.fail_block.add_child(self.exit_block)

    @exit_block.deleter
    def exit_block(self):
        """
        Deleter for exit_block property.
        """
        self.fail_block.remove_child(self.exit_block)

        del self._exit_block

    def accept(self, visitor):
        """
        Accept a CFG visitor and call its visit_loop_else_block method.
        :param visitor: The CFG visitor to accept.
        :type visitor: CFGVisitor
        :return: The result of the accept.
        :rtype: Any
        """
        return visitor.visit_loop_else_block(self)

    def add_child(self, child):
        """
        Add a child to the while-else structure's exit block.
        :param child: The child to add.
        :type child: CFGBlock
        """
        self.exit_block.add_child(child)

    def remove_child(self, child):
        """
        Remove a child from the while-else structure's exit block.
        :param child: The child to remove.
        :type child: CFGBlock
        """
        self.exit_block.remove_child(child)


class CFGSwitchBlock(CFGBlock):
    def __init__(self, case_blocks, exit_block=None):
        """
        Switch statement control flow graph structure.
        :param case_blocks: The blocks representing each respective case.
        :type case_blocks: list[CFGBlock]
        :param exit_block: The block following the switch statement.
        :type exit_block: CFGBlock or None
        """
        self._case_blocks = case_blocks

        if exit_block is None:
            exit_block = CFGBlock
        self._exit_block = exit_block

        for case_block in self.case_blocks:
            case_block.add_child(self.exit_block)

        super().__init__(*self.case_blocks)

    def __str__(self):
        return f"Switch block.\nCase blocks: {self.case_blocks}\nExit block: {self.exit_block}"

    def __repr__(self):
        return f"CFGSwitchBlock(case_blocks={self.case_blocks}, exit_block={self.exit_block})"

    @property
    def case_blocks(self):
        """
        Getter for case_blocks property.
        :return: Value of case_blocks property.
        :rtype: list[CFGBlock] or None
        """
        return self._case_blocks

    @case_blocks.setter
    def case_blocks(self, new_case_blocks):
        """
        Setter for case_blocks property.
        :param new_case_blocks: The value to assign to case_blocks.
        :type new_case_blocks: list[CFGBlock] or None
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
        :type new_exit_block: CFGBlock or None
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

    def accept(self, visitor):
        """
        Accept a CFG visitor and call its visit_switch_block method.
        :param visitor: The CFG visitor to accept.
        :type visitor: CFGVisitor
        :return: The result of the accept.
        :rtype: Any
        """
        return visitor.visit_switch_block(self)

    def add_child(self, child):
        """
        Add a child to the switch structure's exit block.
        :param child: The child to add.
        :type child: CFGBlock
        """
        self.exit_block.add_child(child)

    def remove_child(self, child):
        """
        Remove a child from the switch structure's exit block.
        :param child: The child to remove.
        :type child: CFGBlock
        """
        self.exit_block.remove_child(child)


class CFGBreakBlock(CFGBlock):
    def __init__(self, exit_block=None):
        """
        Break statement control flow graph structure.
        :param exit_block: The block to break to.
        :type exit_block: CFGBlock or None
        """
        self._exit_block = exit_block
        super().__init__(self.exit_block)

    def __str__(self):
        return f"Break block.\nExit block: {self.exit_block}"

    def __repr__(self):
        return f"CFGBreakBlock(exit_block={self.exit_block})"

    def accept(self, visitor):
        """
        Accept a CFG visitor and call its visit_break_block method.
        :param visitor: The CFG visitor to accept.
        :type visitor: CFGVisitor
        :return: The result of the accept.
        :rtype: Any
        """
        return visitor.visit_break_block(self)

    # TODO: Evaluate whether "add/remove child" is a valid operation for break blocks.
    def add_child(self, child):
        """
        Add a child to the break structure's exit block.
        :param child: The child to add.
        :type child: CFGBlock
        """
        self.exit_block.add_child(child)

    def remove_child(self, child):
        """
        Remove a child from the break structure's exit block.
        :param child: The child to remove.
        :type child: CFGBlock
        """
        self.exit_block.remove_child(child)


class CFGContinueBlock(CFGBlock):
    def __init__(self, exit_block=None):
        """
        Continue statement control flow graph structure.
        :param exit_block: The encapsulating loop of the continue statement.
        :type exit_block: CFGBlock or None
        """
        self._exit_block = exit_block
        super().__init__(self.exit_block)

    def __str__(self):
        return f"Continue block.\nExit block: {self.exit_block}"

    def __repr__(self):
        return f"CFGContinueBlock(exit_block={self.exit_block})"

    def accept(self, visitor):
        """
        Accept a CFG visitor and call its visit_continue_block method.
        :param visitor: The CFG visitor to accept.
        :type visitor: CFGVisitor
        :return: The result of the accept.
        :rtype: Any
        """
        return visitor.visit_continue_block(self)

    # TODO: Evaluate whether "add/remove child" is a valid operation for continue blocks.
    def add_child(self, child):
        """
        Add a child to the continue structure's encapsulating loop.
        :param child: The child to add.
        :type child: CFGBlock
        """
        self.exit_block.add_child(child)

    def remove_child(self, child):
        """
        Remove a child from the continue structure's encapsulating loop.
        :param child: The child to remove.
        :type child: CFGBlock
        """
        self.exit_block.remove_child(child)
