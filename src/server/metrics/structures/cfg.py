from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Dict, Sequence, Union

from metrics.structures.base.graph import Graph, Node

if TYPE_CHECKING:
    from metrics.visitors.base.cfg_visitor import CFGVisitor


class CFG(Graph):
    def __init__(self, entry_block: Optional[CFGBlock] = None):
        """
        Control-flow graph.

        :param entry_block: The entry block of the control-flow graph.
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

    def accept(self, visitor: "CFGVisitor"):
        """
        Accept a CFG visitor.

        :param visitor: The CFG visitor to accept.
        :return: The result of the accept.
        """
        if isinstance(self.entry_block, CFGBlock):
            return self.entry_block.accept(visitor)


class CFGBlock(Node):
    def __init__(self, children: Optional[Dict[str, Union[CFGBlock, Sequence[CFGBlock]]]] = None):
        """
        Basic block.

        :param children: The child blocks of the basic block.
        """
        super().__init__()
        self.children = children if children is not None else {}

    def __str__(self):
        s = f"Basic block.\nChildren: {self.children}"

        return s

    def __repr__(self):
        return f"CFGBlock(children={self.children})"

    def __getitem__(self, item):
        return self.children[item]

    def __setitem__(self, key, value: CFGBlock):
        self.children[key] = value

    def __contains__(self, item):
        return item in self.children

    def values(self):
        return list(self.children.values())

    def append(self, block: Optional[CFGBlock]) -> None:
        """
        Add a block to the exit block of the block.

        :param block: The block to append.
        """
        if "exit_block" in self and self["exit_block"] != block:
            self["exit_block"].append(block)
        else:
            self["exit_block"] = block

    def accept(self, visitor: "CFGVisitor"):
        """
        Accept a CFG visitor and call its visit_block method.

        :param visitor: The CFG visitor to accept.
        :return: The result of the accept.
        """
        return visitor.visit_block(self)

    def add_child(self, child: CFGBlock) -> None:
        raise NotImplementedError

    def remove_child(self, child: CFGBlock) -> None:
        raise NotImplementedError


class CFGIfBlock(CFGBlock):
    def __init__(self, success_block: Optional[CFGBlock] = None, exit_block: Optional[CFGBlock] = None):
        """
        If statement control-flow graph structure.

        :param success_block: The block to visit if the condition is true.
        :param exit_block: The block following the if statement.
        """
        if success_block and exit_block:
            success_block.append(exit_block)

        super().__init__({"success_block": success_block, "exit_block": exit_block})

    def __str__(self):
        return f"If block.\nSuccess block: {self['success_block']}\nExit block: {self['exit_block']}"

    def __repr__(self):
        return f"CFGIfBlock(success_block={self['success_block']}, exit_block={self['exit_block']})"

    def accept(self, visitor: "CFGVisitor"):
        """
        Accept a CFG visitor and call its visit_if_block method.

        :param visitor: The CFG visitor to accept.
        :return: The result of the accept.
        """
        return visitor.visit_if_block(self)


class CFGIfElseBlock(CFGBlock):
    def __init__(self, success_block: Optional[CFGBlock] = None, fail_block: Optional[CFGBlock] = None,
                 exit_block: Optional[CFGBlock] = None):
        """
        If-else statement control-flow graph structure.

        :param success_block: The block to visit if the condition is true.
        :param fail_block: The block to visit if the condition is false.
        :param exit_block: The block following the if-else statement.
        """
        if exit_block:
            if success_block:
                success_block.append(exit_block)
            if fail_block:
                fail_block.append(exit_block)

        super().__init__({"success_block": success_block, "fail_block": fail_block})

    def __str__(self):
        return f"If-else block.\nSuccess block: {self['success_block']}\nFail block: {self['fail_block']}]"

    def __repr__(self):
        return f"CFGIfElseBlock(success_block={self['success_block']}, fail_block={self['fail_block']})"

    def accept(self, visitor: "CFGVisitor"):
        """
        Accept a CFG visitor and call its visit_if_else_block method.

        :param visitor: The CFG visitor to accept.
        :return: The result of the accept.
        """
        return visitor.visit_if_else_block(self)


class CFGLoopBlock(CFGBlock):
    def __init__(self, success_block: Optional[CFGBlock] = None, exit_block: Optional[CFGBlock] = None):
        """
        Loop control-flow graph structure.

        :param success_block: The block to visit if the condition is true.
        :param exit_block: The block to following the while statement.
        """
        if success_block:
            success_block.append(self)

        super().__init__({"success_block": success_block, "exit_block": exit_block})

    def __str__(self):
        return f"Loop block.\nSuccess block: {self['success_block']}\nExit block: {self['exit_block']}"

    def __repr__(self):
        return f"CFGLoopBlock(success_block={self['success_block']}, exit_block={self['exit_block']})"

    def accept(self, visitor: "CFGVisitor"):
        """
        Accept a CFG visitor and call its visit_loop_block method.

        :param visitor: The CFG visitor to accept.
        :return: The result of the accept.
        """
        return visitor.visit_loop_block(self)


class CFGLoopElseBlock(CFGBlock):
    def __init__(self, success_block: Optional[CFGBlock] = None, fail_block: Optional[CFGBlock] = None,
                 exit_block: Optional[CFGBlock] = None):
        """
        Loop-else control-flow graph structure.

        :param success_block: The block to visit if the condition is true.
        :param fail_block: The block to visit if the condition is false.
        :param exit_block: The block following the while-else statement.
        """
        if success_block:
            success_block.append(self)

        if fail_block and exit_block:
            fail_block.append(exit_block)

        super().__init__({"success_block": success_block, "fail_block": fail_block})

    def __str__(self):
        return f"Loop-else block.\nSuccess block: {self['success_block']}\nFail block: {self['fail_block']}"

    def __repr__(self):
        return f"CFGLoopElseBlock(success_block={self['success_block']}, fail_block={self['fail_block']})"

    def accept(self, visitor: "CFGVisitor"):
        """
        Accept a CFG visitor and call its visit_loop_else_block method.

        :param visitor: The CFG visitor to accept.
        :return: The result of the accept.
        """
        return visitor.visit_loop_else_block(self)


class CFGSwitchBlock(CFGBlock):
    def __init__(self, case_blocks: Optional[Sequence[CFGBlock]] = None, exit_block: Optional[CFGBlock] = None):
        """
        Switch statement control-flow graph structure.

        :param case_blocks: The blocks representing each respective case.
        :param exit_block: The block following the switch statement.
        """
        if case_blocks:
            for case_block in case_blocks:
                case_block.append(exit_block)

        super().__init__({"case_blocks": case_blocks})

    def __str__(self):
        return f"Switch block.\nCase blocks: {self['case_blocks']}"

    def __repr__(self):
        return f"CFGSwitchBlock(case_blocks={self['case_blocks']})"

    def accept(self, visitor: "CFGVisitor"):
        """
        Accept a CFG visitor and call its visit_switch_block method.

        :param visitor: The CFG visitor to accept.
        :return: The result of the accept.
        """
        return visitor.visit_switch_block(self)


class CFGBreakBlock(CFGBlock):
    def __init__(self, exit_block: Optional[CFGBlock] = None):
        """
        Break statement control-flow graph structure.

        :param exit_block: The block to break to.
        """
        super().__init__({"exit_block": exit_block})

    def __str__(self):
        return f"Break block.\nExit block: {self['exit_block']}"

    def __repr__(self):
        return f"CFGBreakBlock(exit_block={self['exit_block']})"

    def accept(self, visitor: "CFGVisitor"):
        """
        Accept a CFG visitor and call its visit_break_block method.

        :param visitor: The CFG visitor to accept.
        :return: The result of the accept.
        """
        return visitor.visit_break_block(self)


class CFGContinueBlock(CFGBlock):
    def __init__(self, exit_block: Optional[CFGBlock] = None):
        """
        Continue statement control-flow graph structure.

        :param exit_block: The encapsulating loop of the continue statement.
        """
        super().__init__({"exit_block": exit_block})

    def __str__(self):
        return f"Continue block.\nExit block: {self['exit_block']}"

    def __repr__(self):
        return f"CFGContinueBlock(exit_block={self['exit_block']})"

    def accept(self, visitor: "CFGVisitor"):
        """
        Accept a CFG visitor and call its visit_continue_block method.

        :param visitor: The CFG visitor to accept.
        :return: The result of the accept.
        """
        return visitor.visit_continue_block(self)
