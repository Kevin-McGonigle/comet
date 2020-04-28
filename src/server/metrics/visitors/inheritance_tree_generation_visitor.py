from metrics.structures.ast import AST, ASTTerminalNode, ASTPositionalUnpackExpressionNode, \
    ASTKeywordUnpackExpressionNode
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
        if classes is None:
            classes = {}
        self.classes = {class_.to_dict() for class_ in classes}

        if base is None:
            base = Class("Object")
        self.base = base

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

        # TODO: Generate inheritance tree using self.classes and self.base.

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
        name = node.name.accept(self)
        superclasses = node.arguments.accept(self)
        methods = [method for method in (node.body.accept(self)) if isinstance(method, Method)]

    def visit_function_definition(self, node):
        name = node.name.accept(self)
        parameters = node.parameters.accept(self)

    def visit_argument(self, node):
        if isinstance(node.value, ASTTerminalNode):
            return node.value.accept(self)

        if isinstance(node.value, ASTPositionalUnpackExpressionNode):
            if isinstance(node.value.expression, ASTTerminalNode):
                return UnknownClass(node.value.expression.accept(self), "Unpacking positional arguments from iterable.")

        if isinstance(node.value, ASTKeywordUnpackExpressionNode):
            return UnknownClass(node.value.expression.accept(self), "Unpacking keyword arguments from key-value map.")


    def visit_parameter(self, node):
        return Parameter(node.name.accept(self))

    def visit_positional_arguments_parameter(self, node):
        return PositionalArgumentsParameter(node.name.accept(self))

    def visit_keyword_arguments_parameter(self, node):
        return KeywordArgumentsParameter(node.name.accept(self))

    def visit_assignment_statement(self, node):
        return node.variables.accept(self)