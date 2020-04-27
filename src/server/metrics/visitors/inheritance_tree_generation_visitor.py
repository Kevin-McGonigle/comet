from metrics.structures.ast import AST
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
        self.classes = {_class.name: {"Superclasses": [superclass.name for superclass in _class.superclasses], "Methods": _class.methods} for _class in classes}

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
        return_type = node.return_type.accept(self)