from typing import Optional

from metrics.structures.ast import AST
from metrics.structures.cfg import CFG
from metrics.structures.inheritance_tree import InheritanceTree
from metrics.visitors.metrics.lloc_calculation_visitor import LLOCCalculationVisitor
from metrics.visitors.structures.cfg_generation_visitor import CFGGenerationVisitor
from metrics.visitors.structures.inheritance_tree_generation_visitor import InheritanceTreeGenerationVisitor


class Calculator(object):
    """
    Metric/model calculator.

    Class for calculating metrics and generating models for a given AST.
    """

    def __init__(self, ast: AST = None):
        """
        Metric/model calculator.

        :param ast: Abstract syntax tree.
        """
        self.__ast = None

        # TODO: Maybe substitute the below for a single dictionary for extensibility and easier clearing.
        self.cd = None
        self.cfg = None
        self.it = None
        self.dg = None

    # region ast Property

    @property
    def ast(self) -> Optional[AST]:
        """
        Getter for ast property.

        :return: Value of ast.
        """
        return self.__ast

    @ast.setter
    def ast(self, new_ast: AST):
        """
        Setter for ast property. Also clears all accompanying structures.

        :param new_ast: Value to assign to ast.
        """
        self.clear()
        self.__ast = new_ast

    @ast.deleter
    def ast(self):
        """
        Deleter for ast property.
        """
        del self.__ast

    # endregion

    # region Helpers

    def clear(self):
        self.__ast = None
        self.cd = None
        self.cfg = None
        self.it = None
        self.dg = None

    # endregion

    # region Models

    def control_flow_graph(self, ast: Optional[AST]) -> CFG:
        """
        Calculate control flow graph.
        :param ast: Abstract syntax tree to generate CFG from.
        :return: The corresponding control-flow graph.
        """
        if ast:
            return CFGGenerationVisitor().visit(ast)

        if not self.cfg:
            self.cfg = CFGGenerationVisitor().visit(self.ast)

        return self.cfg

    def inheritance_tree(self, ast: Optional[AST]) -> InheritanceTree:
        """
        Calculate inheritance tree.
        :param ast: Abstract syntax tree to generate inheritance tree from.
        :return: The corresponding inheritance tree.
        """
        if ast:
            return InheritanceTreeGenerationVisitor().visit(ast)

        if not self.it:
            self.it = InheritanceTreeGenerationVisitor().visit(self.ast)

        return self.it

    # endregion

    # region Metrics

    def logical_lines_of_code(self, ast: Optional[AST]) -> int:
        """
        Calculate logical lines of code.
        :param ast: Abstract syntax tree to calculate logical lines of code from.
        :return: The corresponding logical lines of code.
        """
        if ast:
            return LLOCCalculationVisitor().visit(ast)

        return LLOCCalculationVisitor().visit(self.ast)

    # endregion

    # TODO: Add calculation functions for remaining metrics and structures.
