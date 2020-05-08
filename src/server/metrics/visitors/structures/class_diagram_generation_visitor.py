from typing import Dict

from metrics.structures.ast import ASTVisibilityModifier, ASTMiscModifier, ASTIdentifierNode
from metrics.structures.class_diagram import *
from metrics.visitors.base.ast_visitor import ASTVisitor


class ClassDiagramGenerationVisitor(ASTVisitor):
    """
    Class diagram generation visitor.

    Provides functionality for visiting an abstract syntax tree and generating the corresponding class diagram.
    """

    def __init__(self):
        self.classes: Dict[str, Class] = {}

    def __create_relationships(self) -> None:
        """
        Iterate over the classes and store corresponding relationships based on attributes, method parameters and
        return types, superclasses, etc.
        """
        for cls in self.classes.values():
            # Implementation
            for interface in cls.interfaces:
                if interface in self.classes:
                    self.__add_relationship(cls, self.classes[interface], RelationshipType.IMPLEMENTATION)

            # Inheritance
            for superclass in cls.superclasses:
                if superclass in self.classes:
                    self.__add_relationship(cls, self.classes[superclass], RelationshipType.INHERITANCE)

            # Nesting
            for nested_class in cls.nested_classes:
                if nested_class in self.classes:
                    self.__add_relationship(self.classes[nested_class], cls, RelationshipType.NESTING)

            # Association
            for attribute in cls.attributes:
                if attribute.type in self.classes:
                    relationship_type = RelationshipType.ASSOCIATION
                    relation = self.classes[attribute.type]
                    relation_role = attribute.name

                    # Check if relationship already exists
                    for relationship in cls.relationships:
                        if relationship.type == relationship_type and relationship.relation == relation \
                                and relationship.relation_role == relation_role:
                            break
                    else:
                        for relationship in relation.relationships:
                            # Check if relationship already exists as a bidirectional relationship.
                            if relationship.type == relationship_type and relationship.relation == cls \
                                    and relationship.role == relation_role and relationship.bidirectional:
                                break
                        else:
                            for relationship in relation.relationships:
                                # Check if a relationship between the two classes already exists and update if one does.
                                if relationship.type == relationship_type and relationship.relation == cls \
                                        and not relationship.bidirectional:
                                    relationship.bidirectional = True
                                    relationship.role = relation_role
                                    break
                            else:
                                cls.relationships.append(Relationship(relationship_type, relation,
                                                                      relation_role=relation_role))

            # Dependency
            for method in cls.methods:
                relationship_type = RelationshipType.DEPENDENCY
                relation = None

                if method.return_type in self.classes:
                    relation = self.classes[method.return_type]
                elif method.parameters:
                    for parameter in method.parameters:
                        if parameter.type in self.classes:
                            relation = self.classes[parameter.type]
                            break

                if relation:
                    cls.relationships.append(Relationship, relationship_type, relation)

    @staticmethod
    def __add_relationship(cls: Class, relation: Class, relationship_type: RelationshipType) -> Relationship:
        for relationship in cls.relationships:
            if relationship.type == relationship_type and relationship.relation == relation:
                break
            else:
                new_relationship = Relationship(relationship_type, relation)
                cls.relationships.append(new_relationship)
                return new_relationship

    def visit(self, ast) -> ClassDiagram:
        """
        Visit the AST and produce a class diagram.
        :param ast: The AST to visit.
        :return: The generated class diagram.
        """
        self.classes = {}

        super().visit(ast)

        self.__create_relationships()

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

        return Parameter(name, type_, default)

    def visit_positional_arguments_parameter(self, node):
        name = "*" + node.name.accept(self)
        type_ = node.type.accept(self) if isinstance(node.type, ASTIdentifierNode) else None

        return Parameter(name, type_)

    def visit_keyword_arguments_parameter(self, node):
        name = "**" + node.name.accept(self)
        type_ = node.type.accept(self) if isinstance(node.type, ASTIdentifierNode) else None

        return Parameter(name, type_)

    @staticmethod
    def get_visibility(modifier: ASTVisibilityModifier) -> Visibility:
        return {
            ASTVisibilityModifier.PRIVATE: Visibility.PRIVATE,
            ASTVisibilityModifier.PUBLIC: Visibility.PUBLIC,
            ASTVisibilityModifier.PROTECTED: Visibility.PROTECTED,
            ASTVisibilityModifier.INTERNAL: Visibility.INTERNAL
        }[modifier]
