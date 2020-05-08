from typing import List, Dict, Tuple

from metrics.visitors.base.cfg_visitor import CFGVisitor


class ControlFlowGraphFormattingVisitor(CFGVisitor):
    """
    CFG formatting visitor.

    Provides functionality for visiting an CFG and producing a list of nodes and a list of links,
    both formatted for front-end request response.
    """

    def __init__(self):
        """
        CFG formatting visitor.
        """
        super().__init__()
        self._blocks: List[Dict[str, str]] = []
        self._links: List[Dict[str, str]] = []

    def visit(self, tree) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
        """
        Visit an CFG structure and return a list of classes and a list of links, formatted for front-end
        request response.

        :param tree: The CFG to visit.
        :return: Formatted lists of classes and links respectively.
        """
        self._visited = []
        self._blocks = []
        self._links = []

        tree.accept(self)
        return self._blocks, self._links

    def visit_children(self, block) -> None:
        """
        Visit each of a block's children.

        :param block: The parent class whose subclasses to visit.
        """
        if block.children:
            for child in block.children:
                child.accept(self)

    def visit_block(self, block) -> None:
        """
        Visit a block.

        If the block has not yet been visited, add it to visited, add it to blocks and add its child links.

        :param block: The block to visit.
        """
        if block not in self._visited:
            self._visited.append(block)
        
            self._blocks.append({"id": len(self._blocks)})
            if block.children:
                for child in block.children:
                    self._links.append({"source": len(self._blocks), "target": 1})

            self.visit_children(block)
