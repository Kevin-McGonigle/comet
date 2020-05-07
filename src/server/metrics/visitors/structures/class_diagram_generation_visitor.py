from metrics.structures.ast import ASTVisibilityModifier, ASTMiscModifier, ASTIdentifierNode
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

    def create_relationships(self) -> None:
        """
        Iterate over the classes and create corresponding relationships based on attributes, method parameters and
        return types, superclasses, etc.
        :return:
        """
        pass

    def visit(self, ast) -> ClassDiagram:
        """
        Visit the AST and produce a class diagram.
        :param ast: The AST to visit.
        :return: The generated class diagram.
        """
        self.classes = {}

        super().visit(ast)

        self.create_relationships()

        return ClassDiagram(list(self.classes.values()))

    def visit_children(self, node) -> List:
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

    def visit_class_definition(self, node):
        name = node.name.accept(self)

        superclasses = node.superclasses.accept(self) if node.superclasses else None
        interfaces = node.interfaces.accept(self) if node.interfaces else None

        if node.body:
            body = node.body.accept(self)

            attributes = [attribute for attribute in body if isinstance(attribute, Attribute)]
            methods = [method for method in body if isinstance(method, Method)]
            nested_classes = [nested_class.name for nested_class in body if isinstance(nested_class, Class)]

            class_ = Class(name, attributes, methods, superclasses, interfaces, nested_classes)
        else:
            class_ = Class(name, superclasses=superclasses, interfaces=interfaces)

        self.classes[name] = class_

        return class_

    def visit_function_definition(self, node):
        return_type = node.return_type.accept(self) if isinstance(node.return_type, ASTIdentifierNode) else None

        visibility = None
        static = False

        for modifier in node.modifiers:
            if isinstance(modifier, ASTVisibilityModifier):
                visibility = self.get_visibility(modifier)
            elif modifier is ASTMiscModifier.STATIC:
                static = True

        parameters = node.parameters.accept(self) if node.parameters else None

        return Method(node.name.accept(self), visibility, parameters, return_type, static)

    def visit_variable_declaration(self, node):
        type_ = node.type.accept(self) if isinstance(node.type, ASTIdentifierNode) else None

        visibility = None
        static = False

        for modifier in node.modifiers:
            if isinstance(modifier, ASTVisibilityModifier):
                visibility = self.get_visibility(modifier)
            elif modifier is ASTMiscModifier.STATIC:
                static = True

        attributes = []
        for variable in node.variables.accept(self):
            attributes.append(Attribute(variable, visibility, type_, None, static))

        return attributes if attributes else None

    def visit_argument(self, node):
        return node.value.accept(self) if isinstance(node.value, ASTIdentifierNode) else None

    def visit_keyword_argument(self, node):
        return None

    def visit_parameter(self, node):
        name = node.name.accept(self)
        type_ = node.type.accept(self) if isinstance(node.type, ASTIdentifierNode) else None
        default = node.default.accept(self) if isinstance(node.default, ASTIdentifierNode) else None
        return Parameter(node.name.accept(self))

    def visit_positional_arguments_parameter(self, node):
        return super().visit_positional_arguments_parameter(node)

    def visit_keyword_arguments_parameter(self, node):
        return super().visit_keyword_arguments_parameter(node)

    @staticmethod
    def get_visibility(modifier: ASTVisibilityModifier) -> Visibility:
        return {
            ASTVisibilityModifier.PRIVATE: Visibility.PRIVATE,
            ASTVisibilityModifier.PUBLIC: Visibility.PUBLIC,
            ASTVisibilityModifier.PROTECTED: Visibility.PROTECTED,
            ASTVisibilityModifier.INTERNAL: Visibility.INTERNAL
        }[modifier]
