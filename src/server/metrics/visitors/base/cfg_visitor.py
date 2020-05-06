from typing import TYPE_CHECKING

from metrics.visitors.base.graph_visitor import GraphVisitor

if TYPE_CHECKING:
    from metrics.structures.cfg import *


class CFGVisitor(GraphVisitor):
    """
    Control-flow graph visitor.

    Base class for visiting control-flow graph structures.
    """
    def __init__(self):
        self._visited = []

    def visit(self, cfg):
        """
        Visit a CFG structure.
        :param cfg: The CFG to visit.
        :type cfg: CFG
        :return: The output of the visiting process.
        :rtype: Any
        """
        self._visited = []
        return super().visit(cfg)

    def visit_children(self, block):
        """
        Visit each of a block's children.
        :param block: The parent block whose children to visit.
        :type block: CFGBlock
        :return: Mapping of each child block to their visit result
        :rtype: dict[CFGBlock, Any]
        """
        return super().visit_children(block)

    def visit_block(self, block):
        """
        Visit CFG basic block.
        :param block: The CFG basic block.
        :type block: CFGBlock
        :return: The result of the visit.
        :rtype: Any
        """
        if block not in self._visited:
            self._visited.append(block)
            return self.visit_children(block)

    def visit_if_block(self, block):
        """
        Visit CFG if block.
        :param block: The CFG if block.
        :type block: CFGIfBlock
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_block(block)

    def visit_if_else_block(self, block):
        """
        Visit CFG if-else block.
        :param block: The CFG if-else block.
        :type block: CFGIfElseBlock
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_block(block)

    def visit_loop_block(self, block):
        """
        Visit CFG loop block.
        :param block: The CFG loop block.
        :type block: CFGLoopBlock
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_block(block)

    def visit_loop_else_block(self, block):
        """
        Visit CFG loop-else block.
        :param block: The CFG loop-else block.
        :type block: CFGLoopElseBlock
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_block(block)

    def visit_switch_block(self, block):
        """
        Visit CFG switch block.
        :param block: The CFG switch block.
        :type block: CFGSwitchBlock
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_block(block)

    def visit_break_block(self, block):
        """
        Visit CFG break block.
        :param block: The CFG break block.
        :type block: CFGBreakBlock
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_block(block)

    def visit_continue_block(self, block):
        """
        Visit CFG continue block.
        :param block: The CFG continue block.
        :type block: CFGContinueBlock
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_block(block)
