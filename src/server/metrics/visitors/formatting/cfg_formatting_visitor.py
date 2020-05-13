from typing import List, Dict, Tuple

from metrics.structures.cfg import CFGBlock
from metrics.visitors.base.cfg_visitor import CFGVisitor


class CFGFormattingVisitor(CFGVisitor):
    """
    CFG formatting visitor.

    Provides functionality for visiting a CFG and producing a list of blocks and a list of links,
    both formatted for front-end request response.
    """

    def __init__(self):
        """
        CFG formatting visitor.
        """
        super().__init__()
        self._visited: Dict[CFGBlock, str] = {}
        self.current_id: int = 1
        self._blocks: List[Dict[str, str]] = []
        self._links: List[Dict[str, str]] = []

    def visit(self, tree) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
        """
        Visit an CFG structure and return a list of classes and a list of links, formatted for front-end
        request response.

        :param tree: The CFG to visit.
        :return: Formatted lists of classes and links respectively.
        """
        self._visited = {}
        self.current_id = 1

        self._blocks = []
        self._links = []

        tree.accept(self)

        return self._blocks, self._links

    def visit_children(self, block) -> List[str]:
        """
        Visit each of a block's children.

        :param block: The parent block whose subclasses to visit.
        :return: A list of the child blocks' ids.
        """
        results = []
        if block.children:
            for child in block.children:
                result = child.accept(self)
                if result:
                    if isinstance(result, list):
                        results.extend(result)
                    else:
                        results.append(result)
        return results

    def visit_block(self, block) -> str:
        """
        Visit a block.

        If the block has not yet been visited, add it to visited, add it to blocks and add its child links.

        :param block: The block to visit.
        :return: The block's id.
        """
        if block in self._visited:
            return self._visited[block]
        else:
            id_ = str(self.current_id)
            self.current_id += 1

            self._visited[block] = id_
        
            self._blocks.append({"id": id_})

            for child_id in self.visit_children(block):
                self._links.append({"source": id_, "target": child_id})

            return id_
