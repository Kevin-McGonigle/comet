from typing import TYPE_CHECKING

from metrics.visitors.base.cfg_visitor import CFGVisitor

if TYPE_CHECKING:
    from metrics.structures.cfg import *


class CCCalculationVisitor(CFGVisitor):
    """
    Control-flow graph visitor for calculating cyclomatic complexity.

    Provides functionality for visiting a control-flow graph and returning its cyclomatic complexity using
    the formula:

    CC = E - N + 2C

    Where E = the number of edges in the graph, N = the number of nodes/basic blocks in the graph and
    C = the number of connected components (always taken as 1).

    """

    def __init__(self):
        self._node_count = 0
        self._edge_count = 0
        super().__init__()

    def visit(self, cfg):
        """
        Visit a CFG structure and return its cyclomatic complexity.
        :param cfg: The CFG to visit.
        :type cfg: CFG
        :return: The cyclomatic complexity of the CFG.
        :rtype: int
        """
        self._node_count = 0
        self._edge_count = 0
        self._visited = []

        cfg.accept(self)

        return self._edge_count - self._node_count + 2

    def visit_children(self, block):
        """
        Visit each of a block's children.
        :param block: The parent block whose children to visit.
        :type block: CFGBlock
        """
        for child in block.children:
            child.accept()

    def visit_block(self, block):
        """
        Visit a CFG basic block, adding to _node_count and _edge_count accordingly and visiting its children if this block
        has not been visited before.
        :param block: The CFG basic block to visit.
        :type block: CFGBlock
        """
        if block not in self._visited:
            self._visited.append(block)

            self._node_count += 1
            self._edge_count += len(block.children)

            self.visit_children(block)
