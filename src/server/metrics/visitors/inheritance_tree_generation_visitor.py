from metrics.structures.ast import *
from metrics.structures.inheritance_tree import *
from metrics.visitors.base.ast_visitor import ASTVisitor


class InheritanceTreeGenerationVisitor(ASTVisitor):
    def __init__(self, base=None, classes=None):
        """
        Inheritance tree generation visitor.
        :param base: The base node of the inheritance tree to be generated.
        :type base: Class or None
        :param classes: List of exterior classes.
        :type classes: list[Class] or None
        """
        if base is None:
            base = Class("object")
        self.base = base

        if classes is None:
            classes = {}
        self.classes = {class_.name: class_ for class_ in classes}
        self.classes[self.base.name] = self.base

        self.scope = None

        super().__init__()

    def visit(self, ast):
        """
        Visit the AST and produce an inheritance tree.
        :param ast: The AST to visit.
        :type ast: AST
        :return: The generated inheritance tree.
        :rtype: InheritanceTree
        """
        super().visit(ast)

    def visit_children(self, node):
        """
        Visit all of a node's children.
        :param node: The node whose children to visit.
        :type node: ASTNode
        :return: A built sequence of CFGNodes returned by visiting each child. None if no CFGNodes returned.
        :rtype: list[Class or Method or Parameter]
        """
        child_results = []
        for child in node.children:
            child_result = child.accept(self)
            if child_results:
                if isinstance(child_result, list):
                    child_results += child_result
                else:
                    child_results.append(child_result)

        return child_results

    def visit_class_definition(self, node):
        # Class name
        name = node.name.accept(self)
        if self.scope:
            name = self.scope + "." + name

        # Class superclasses
        if node.arguments:
            superclasses = node.arguments.accept(self)
        else:
            superclasses = [self.base]

        # Class methods
        tmp = self.scope
        self.scope = name

        methods = [method for method in (node.body.accept(self)) if isinstance(method, Method)]

        self.scope = tmp

        # Create class
        self.classes[name] = Class(name, superclasses, methods)

    def visit_function_definition(self, node):
        # Method name
        name = node.name.accept(self)

        # Method parameters
        parameters = None
        if node.parameters:
            parameters = [parameter for parameter in node.parameters.accept(self) if
                          isinstance(parameter, Parameter)
                          or isinstance(parameter, PositionalArgumentsParameter)
                          or isinstance(parameter, KeywordArgumentsParameter)]

        # Method return type
        return_type = None
        if node.return_type:
            return_type = node.return_type.accept(self)

        # Visit method body
        tmp = self.scope
        self.scope = f"{self.scope}.{name}.<locals>"

        node.body.accept(self)

        self.scope = tmp

        # Create method
        return Method(name, parameters, return_type)

    def visit_argument(self, node):
        if isinstance(node.value, ASTIdentifierNode) or isinstance(node.value, ASTMemberNode):
            # Superclass name
            name = node.value.accept(self)
            if isinstance(name, UnknownClass):
                return name

            # Check for class at same scope
            if self.scope and f"{self.scope}.{name}" in self.classes:
                return self.classes[f"{self.scope}.{name}"]

            # Check for class at global scope
            if name in self.classes:
                return self.classes[name]

            return UnknownClass(name, f"Class with name \"{name}\" cannot be found.")

        if isinstance(node.value, ASTPositionalUnpackExpressionNode):
            return UnknownClasses("Unpacking positional arguments from iterable.")

        if isinstance(node.value, ASTKeywordUnpackExpressionNode):
            return UnknownClasses("Unpacking keyword arguments from key-value map.")

        return UnknownClass(reason=f"{node.value} unsupported for class identification. Type: {type(node.value)}")

    def visit_member(self, node):
        if isinstance(node.parent, ASTIdentifierNode) or isinstance(node.parent, ASTMemberNode):
            if isinstance(node.member, ASTIdentifierNode or isinstance(node.member, ASTMemberNode)):
                parent = node.parent.accept(self)
                if isinstance(parent, UnknownClass):
                    return parent

                member = node.member.accept(self)
                if isinstance(member, UnknownClass):
                    return member

                return parent.accept(self) + "." + member.accept(self)
            return UnknownClass(reason=f"{node.member} unsupported for class identification. Type: {type(node.member)}")
        return UnknownClass(reason=f"{node.parent} unsupported for class identification. Type: {type(node.parent)}")

    def visit_parameter(self, node):
        return Parameter(node.name.accept(self))

    def visit_positional_arguments_parameter(self, node):
        return PositionalArgumentsParameter(node.name.accept(self))

    def visit_keyword_arguments_parameter(self, node):
        return KeywordArgumentsParameter(node.name.accept(self))

    def visit_identifier(self, node):
        return node.name
