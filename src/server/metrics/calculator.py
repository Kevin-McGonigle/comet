from typing import Type

from antlr4 import InputStream, CommonTokenStream, Lexer, ParseTreeVisitor

from metrics.parsers.parser import Parser
from metrics.structures.ast import AST, ASTStatementsNode, ASTIfStatementNode, ASTLiteralNode, \
    ASTLiteralType, ASTPassStatementNode
from metrics.structures.cfg import CFG, CFGIfElseBlock
from metrics.structures.class_diagram import *
from metrics.structures.dependency_graph import DependencyGraph, KnownClass as DGKnownClass
from metrics.structures.inheritance_tree import InheritanceTree, Class as ITKnownClass
from metrics.visitors.metrics.ac_calculation_visitor import ACCalculationVisitor
from metrics.visitors.metrics.cc_calculation_visitor import CCCalculationVisitor
from metrics.visitors.metrics.ec_calculation_visitor import ECCalculationVisitor
from metrics.visitors.metrics.lloc_calculation_visitor import LLOCCalculationVisitor
from metrics.visitors.metrics.mid_calculation_visitor import MIDCalculationVisitor
from metrics.visitors.metrics.mnd_calculation_visitor import MNDCalculationVisitor
from metrics.visitors.structures.cfg_generation_visitor import CFGGenerationVisitor
from metrics.visitors.structures.class_diagram_generation_visitor import ClassDiagramGenerationVisitor
from metrics.visitors.structures.dependency_graph_generation_visitor import DependencyGraphGenerationVisitor
from metrics.visitors.structures.inheritance_tree_generation_visitor import InheritanceTreeGenerationVisitor


class Calculator(object):
    """
    Metric/model calculator.

    Class for calculating metrics and generating models for a given AST.
    """

    def __init__(self, content: str, lexer_type: Type[Lexer], parser_type: Type[Parser],
                 visitor_type: Type[ParseTreeVisitor]):
        """
        Metric/model calculator.

        :param content: The content for which to calculate metrics and models.
        :param lexer_type: The lexer to use when lexing the content.
        :param parser_type: The parser_type to use when parsing the content.
        :param visitor_type: The visitor to use when visiting the parse tree to generate an AST.
        """
        input_stream = InputStream(content)
        lexer = lexer_type(input_stream)
        tokens = CommonTokenStream(lexer)
        parser = parser_type(tokens)
        parse_tree = parser.parse()
        visitor = visitor_type()

        self.__ast = visitor.visit(parse_tree)
        self.models = {}

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
        self.models = {}

    # endregion

    # region Models

    def control_flow_graph(self, ast: Optional[AST]) -> CFG:
        """
        Generate control-flow graph.

        :param ast: Abstract syntax tree to generate CFG from.
        :return: The corresponding control-flow graph.
        """
        if ast:
            return CFGGenerationVisitor().visit(ast)

        if CFG not in self.models or not isinstance(self.models[CFG], CFG):
            self.models[CFG] = CFGGenerationVisitor().visit(self.ast)

        return self.models[CFG]

    def inheritance_tree(self, ast: Optional[AST]) -> InheritanceTree:
        """
        Generate inheritance tree.

        :param ast: Abstract syntax tree to generate inheritance tree from.
        :return: The corresponding inheritance tree.
        """
        if ast:
            return InheritanceTreeGenerationVisitor().visit(ast)

        if InheritanceTree not in self.models or not isinstance(self.models[InheritanceTree], InheritanceTree):
            self.models[InheritanceTree] = InheritanceTreeGenerationVisitor().visit(self.ast)

        return self.models[InheritanceTree]

    def dependency_graph(self, ast: Optional[AST]) -> DependencyGraph:
        """
        Generate dependency graph.

        :param ast: Abstract syntax tree to generate dependency graph from.
        :return: The corresponding dependency graph.
        """
        if ast:
            return DependencyGraphGenerationVisitor().visit(ast)

        if DependencyGraph not in self.models or not isinstance(self.models[DependencyGraph], DependencyGraph):
            self.models[DependencyGraph] = DependencyGraphGenerationVisitor().visit(self.ast)

        return self.models[DependencyGraph]

    def class_diagram(self, ast: Optional[AST]) -> ClassDiagram:
        """
        Generate class diagram.

        :param ast: Abstract syntax tree to generate class diagram from.
        :return: The corresponding class diagram.
        """
        if ast:
            return ClassDiagramGenerationVisitor().visit(ast)

        if ClassDiagram not in self.models or not isinstance(self.models[ClassDiagram], ClassDiagram):
            self.models[ClassDiagram] = ClassDiagramGenerationVisitor().visit(self.ast)

        return self.models[ClassDiagram]

    # endregion

    # region Metrics

    def logical_lines_of_code(self, ast: Optional[AST] = None) -> int:
        """
        Calculate logical lines of code.

        :param ast: Abstract syntax tree to calculate logical lines of code from.
        :return: The corresponding logical lines of code.
        """
        if ast:
            return LLOCCalculationVisitor().visit(ast)

        return LLOCCalculationVisitor().visit(self.ast)

    def afferent_coupling(self, dg: Optional[DependencyGraph] = None) -> dict:
        """
        Calculate afferent coupling within code.
        :param dg: Dependency graph to calculate afferent coupling of code from.
        :return: The corresponding afferent coupling of code.
        """
        if dg:
            return ACCalculationVisitor().visit(dg)

        return ACCalculationVisitor().visit(self.models[DependencyGraph])

    def efferent_coupling(self, dg: Optional[DependencyGraph] = None) -> dict:
        """
        Calculate efferent coupling within code.

        :param dg: Dependency graph to calculate efferent coupling of code from.
        :return: The corresponding efferent coupling of code.
        """
        if dg:
            return ECCalculationVisitor().visit(dg)

        return ECCalculationVisitor().visit(self.models[DependencyGraph])

    def cyclomatic_complexity(self, cfg: Optional[CFG] = None) -> int:
        """
        Calculate cyclomatic complexity within code.

        :param cfg: Control-flow graph to calculate cyclomatic complexity of code from.
        :return: The corresponding cyclomatic complexity of code.
        """
        if cfg:
            return CCCalculationVisitor().visit(cfg)

        return CCCalculationVisitor().visit(self.models[CFG])

    def maximum_inheritance_depth(self, it: Optional[InheritanceTree] = None) -> int:
        """
        Calculate the inheritance depth in code.
        :param it: Inheritance tree to calculate inheritance depth of code from.
        :return: The corresponding inheritance depth of code.
        """
        if it:
            return MIDCalculationVisitor().visit(it)

        return MIDCalculationVisitor().visit(self.models[InheritanceTree])

    def maximum_nesting_depth(self, cfg: Optional[CFG] = None) -> int:
        """
        Calculate maximum nesting depth within code.
        :param cfg: Control-flow graph to calculate maximum nesting depth of code from.
        :return: The corresponding maximum nesting depth of code.
        """
        if cfg:
            return MNDCalculationVisitor().visit(cfg)

        return MNDCalculationVisitor().visit(self.models[CFG])

    # endregion


class CalculatorStub(Calculator):
    # noinspection PyMissingConstructor
    def __init__(self):
        pass

    @property
    def ast(self) -> Optional[AST]:
        return AST(ASTStatementsNode(
            [ASTIfStatementNode(ASTLiteralNode(ASTLiteralType.BOOLEAN, "True"), ASTPassStatementNode())]))

    @ast.setter
    def ast(self, new_ast):
        raise NotImplementedError

    @ast.deleter
    def ast(self):
        raise NotImplementedError

    def clear(self):
        pass

    def control_flow_graph(self, ast: Optional[AST]) -> CFG:
        return CFG(CFGIfElseBlock())

    def inheritance_tree(self, ast: Optional[AST]) -> InheritanceTree:
        d = ITKnownClass("D")
        c = ITKnownClass("C", [d])
        b = ITKnownClass("B", [d])
        a = ITKnownClass("A", [c])
        base = ITKnownClass("object", [a, b])

        return InheritanceTree(base)

    def dependency_graph(self, ast: Optional[AST]) -> DependencyGraph:
        base = DGKnownClass("object")
        a = DGKnownClass("A", [base])
        b = DGKnownClass("B", [base])
        c = DGKnownClass("C", [a])
        d = DGKnownClass("D", [b, c])

        return DependencyGraph(base, [base, a, b, c, d])

    def class_diagram(self, ast: Optional[AST]) -> ClassDiagram:
        a = Class("A", [Attribute("a_attr", Visibility.PRIVATE)], [Method("a_method", Visibility.PUBLIC)])
        b = Class("B", [Attribute("b_attr", Visibility.PRIVATE)], [Method("b_method", Visibility.PUBLIC)])

        return ClassDiagram([a, b], [Relationship(RelationshipType.ASSOCIATION, a, b)])

    def logical_lines_of_code(self, ast: Optional[AST] = None) -> int:
        return 0

    def afferent_coupling(self, dg: Optional[DependencyGraph] = None) -> dict:
        base = DGKnownClass("object")
        a = DGKnownClass("A", [base])
        b = DGKnownClass("B", [base])
        c = DGKnownClass("C", [a])
        d = DGKnownClass("D", [b, c])

        return {
            base: 2,
            a: 1,
            b: 1,
            c: 1,
            d: 0
        }

    def efferent_coupling(self, dg: Optional[DependencyGraph] = None) -> dict:
        base = DGKnownClass("object")
        a = DGKnownClass("A", [base])
        b = DGKnownClass("B", [base])
        c = DGKnownClass("C", [a])
        d = DGKnownClass("D", [b, c])

        return {
            base: 0,
            a: 1,
            b: 1,
            c: 1,
            d: 2
        }

    def cyclomatic_complexity(self, cfg: Optional[CFG] = None) -> int:
        return 0

    def maximum_inheritance_depth(self, it: Optional[InheritanceTree] = None) -> int:
        return 0

    def maximum_nesting_depth(self, cfg: Optional[CFG] = None) -> int:
        return 0
