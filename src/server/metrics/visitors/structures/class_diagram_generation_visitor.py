from typing import Sequence

from metrics.structures.ast import AST, ASTNode, ASTClassDefinitionNode, ASTFunctionDefinitionNode, \
    ASTVariableDeclarationNode, ASTVisibilityModifier, ASTMiscModifier, ASTIdentifierNode
from metrics.structures.class_diagram import *
from metrics.visitors.base.ast_visitor import ASTVisitor


class ClassDiagramGenerationVisitor(ASTVisitor):
    """
    Class diagram generation visitor.

    Provides functionality for visiting an abstract syntax tree and generating the corresponding class diagram.
    """

    def __init__(self):
        self.classes = {}
        self.relationships = []

    def visit(self, ast: AST) -> ClassDiagram:
        """
        Visit the AST and produce a class diagram.
        :param ast: The AST to visit.
        :return: The generated class diagram.
        """
        self.classes = {}
        self.relationships = []

        super().visit(ast)

        return ClassDiagram(list(self.classes.values()), self.relationships)

    def visit_children(self, node: ASTNode) -> Sequence:
        """
        Visit each of an AST node's children.
        :param node: The parent AST node whose children to visit.
        """
        child_results = []
        for child in node.children:
            child_result = child.accept(self)
            if child_results:
                if isinstance(child_result, list):
                    child_results += child_result
                elif child_result:
                    child_results.append(child_result)

        return child_results

    def visit_class_definition(self, node: ASTClassDefinitionNode):
        name = node.name.accept(self)
        body = node.body.accept(self)

        attributes = [attribute for attribute in body if isinstance(attribute, Attribute)]
        methods = [method for method in body if isinstance(method, Method)]

        class_ = Class(name, attributes, methods)

        nested_classes = [class_ for class_ in body if isinstance(class_, Class)]
        superclasses = node.arguments.accept(self)

        return class_

    def visit_function_definition(self, node: ASTFunctionDefinitionNode):
        return_type = node.return_type.accept(self) if isinstance(node.return_type, ASTIdentifierNode) else None
        visibility = None
        static = False

        for modifier in node.modifiers:
            if isinstance(modifier, ASTVisibilityModifier):
                visibility = self.get_visibility(modifier)
            elif modifier is ASTMiscModifier.STATIC:
                static = True

        return Method(node.name.accept(self), visibility, node.parameters, return_type, static)

    def visit_variable_declaration(self, node: ASTVariableDeclarationNode):
        type_ = node.type.accept(self) if isinstance(node.type, ASTIdentifierNode) else None
        visibility = None
        static = False

        for modifier in node.modifiers:
            if isinstance(modifier, ASTVisibilityModifier):
                visibility = self.get_visibility(modifier)
            elif isinstance(modifier, ASTMiscModifier):
                if modifier is ASTMiscModifier.STATIC:
                    static = True

        attributes = []
        for variable in node.variables.accept(self):
            attributes.append(Attribute(variable, visibility, type_, None, static))

        return attributes if attributes else None

    @staticmethod
    def get_visibility(modifier: ASTVisibilityModifier) -> Visibility:
        return {
            ASTVisibilityModifier.PRIVATE: Visibility.PRIVATE,
            ASTVisibilityModifier.PUBLIC: Visibility.PUBLIC,
            ASTVisibilityModifier.PROTECTED: Visibility.PROTECTED,
            ASTVisibilityModifier.INTERNAL: Visibility.INTERNAL
        }[modifier]
