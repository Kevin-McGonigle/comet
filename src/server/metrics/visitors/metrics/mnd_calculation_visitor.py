from typing import Union

from metrics.structures.cfg import CFGLoopBlock, CFGIfBlock, CFGIfElseBlock, CFGLoopElseBlock, CFGBlock
from metrics.visitors.base.cfg_visitor import CFGVisitor


class MNDCalculationVisitor(CFGVisitor):
    """
    Control-flow graph visitor for calculating maximum nesting depth.

    Provides functionality for visiting a control-flow graph and returning its maximum nesting depth, i.e. the
    maximum number of encapsulated scopes.
    """

    def visit(self, cfg) -> int:
        return cfg.accept(self)

    def visit_children(self, block) -> int:
        children = [child.accept(self) for child in  block.children.values() if isinstance(child, CFGBlock)]
        return max(children) if children else 1

    def visit_block(self, block) -> int:
        if block in self._visited:
            return 1

        self._visited.append(block)

        if "exit_block" in block and block["exit_block"]:
            exit_depth = block["exit_block"].accept(self)
        else:
            exit_depth = 1

        children_depth = self.visit_children(block)

        return max(exit_depth, children_depth)

    def visit_if_block(self, block) -> int:
        return self.visit_if_or_loop_block(block)

    def visit_if_else_block(self, block) -> int:
        return self.visit_if_or_loop_block(block)

    def visit_loop_block(self, block) -> int:
        return self.visit_if_or_loop_block(block)

    def visit_loop_else_block(self, block) -> int:
        return self.visit_if_or_loop_block(block)

    def visit_switch_block(self, block) -> int:
        if block in self._visited:
            return 1

        self._visited.append(block)

        if "exit_block" in block and block["exit_block"]:
            exit_depth = block["exit_block"].accept(self)
        else:
            exit_depth = 1

        if "case_blocks" in block and block["case_blocks"]:
            cases_depth = 1 + max([case.accept(self) for case in block["case_blocks"]])
        else:
            cases_depth = 2

        return max(exit_depth, cases_depth)

    def visit_if_or_loop_block(self, block: Union[CFGIfBlock, CFGIfElseBlock, CFGLoopBlock, CFGLoopElseBlock]) -> int:
        if block in self._visited:
            return 1

        self._visited.append(block)

        if "exit_block" in block and block["exit_block"]:
            exit_depth = block["exit_block"].accept(self)
        else:
            exit_depth = 1

        if "success_block" in block and block["success_block"]:
            success_depth = 1 + block["success_block"].accept(self)
        else:
            success_depth = 1

        if "fail_block" in block and block["fail_block"]:
            return max(exit_depth, success_depth, 1 + block["fail_block"].accept(self))

        return max(exit_depth, success_depth)
