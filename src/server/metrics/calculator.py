from typing import Optional

from metrics.structures.ast import AST
from metrics.structures.cfg import CFG
from metrics.structures.inheritance_tree import InheritanceTree
from metrics.structures.dependency_graph import DependencyGraph
from metrics.structures.class_diagram import ClassDiagram


from metrics.visitors.structures.cfg_generation_visitor import CFGGenerationVisitor
from metrics.visitors.structures.inheritance_tree_generation_visitor import InheritanceTreeGenerationVisitor
from metrics.visitors.structures.dependency_graph_generation_visitor import DependencyGraphGenerationVisitor
from metrics.visitors.structures.class_diagram_generation_visitor import ClassDiagramGenerationVisitor

from metrics.visitors.metrics.lloc_calculation_visitor import LLOCCalculationVisitor
from metrics.visitors.metrics.ac_calculation_visitor import ACCalculationVisitor
from metrics.visitors.metrics.ec_calculation_visitor import ECCalculationVisitor
from metrics.visitors.metrics.cc_calculation_visitor import CCCalculationVisitor
from metrics.visitors.metrics.mid_calculation_visitor import MIDCalculationVisitor
from metrics.visitors.metrics.mnd_calculation_visitor import MNDCalculationVisitor



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

    def dependency_graph(self, ast: Optional[AST]) -> DependencyGraph:
        """
        Calculate dependency graph.
        :param ast: Abstract syntax tree to generetate dependency graph from.
        :return: The corresponding DependencyGraph
        """
        if ast:
            return DependencyGraphGenerationVisitor().visit(ast)
        
        if not self.dg:
            self.dg = DependencyGraphGenerationVisitor().visit(self.ast)

        return self.dg

    def class_diagram(self, ast: Optional[AST]) -> ClassDiagram:
        """
        Calculate Class Diagram graph.
        :param ast: Abstract syntax tree to generetate class diagram from.
        :return: The corresponding ClassDiagram
        """
        if ast:
            return ClassDiagramGenerationVisitor().visit(ast)
        
        if not self.cd:
            self.cd = ClassDiagramGenerationVisitor().visit(self.ast)

        return self.cd

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

    def afferent_coupling(self, ast: Optional[ast]) -> dict:
        """
        Calculate afferent couplings within code.
        :param ast: Abstract syntax tree to calculate afferent couplings of code from.
        :return: The corresponding afferent couplings of code.
        """
        if ast:
            return ACCalculationVisitor().visit(ast)

        return ACCalculationVisitor().visit(self.ast)

    def efferent_coupling(self, ast: Optional[ast]) -> dict:
        """
        Calculate efferent couplings within code.
        :param ast: Abstract syntax tree to calculate efferent couplings of code from.
        :return: The corresponding efferent couplings of code.
        """
        if ast:
            return ECCalculationVisitor().visit(ast)

        return ECCalculationVisitor().visit(self.ast)
    
    def cyclomatic_complexity(self, ast: Optional[ast]) -> int:
        """
        Calculate cyclomatic complexity within code.
        :param ast: Abstract syntax tree to calculate cyclomatic complexity of code from.
        :return: The corresponding cyclomatic complexity of code.
        """
        if ast:
            return CCCalculationVisitor().visit(ast)

        return CCCalculationVisitor().visit(self.ast)

    def maximum_inheritance_depth(self, ast: Optional[ast]) -> dict:
        """
        Calculate the inheritance depth in code.
        :param ast: Abstract syntax tree to calculate inheritance depth of code from.
        :return: The corresponding inheritance depth of code.
        """
        if ast:
            return MIDCalculationVisitor().visit(ast)

        return MIDCalculationVisitor().visit(self.ast)
    
    def maximum_nesting_depth(self, ast: Optional[ast]) -> dict:
        """
        Calculate maximum nesting depth within code.
        :param ast: Abstract syntax tree to calculate maximum nesting depth of code from.
        :return: The corresponding maximum nesting depth of code.
        """
        if ast:
            return MNDCalculationVisitor().visit(ast)

        return MNDCalculationVisitor().visit(self.ast)

    # endregion

