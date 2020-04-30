from typing import TYPE_CHECKING

from metrics.structures.dependency_graph import *
from metrics.visitors.base.ast_visitor import ASTVisitor

if TYPE_CHECKING:
    from metrics.structures.ast import *


class DependencyGraphGenerationVisitor(ASTVisitor):
    def __init__(self, base=None, classes=None):
        """
        Dependency graph generation visitor.
        :param base: The base node of the dependency graph to be generated.
        :type base: Class or None
        :param classes: List of exterior classes.
        :type classes: list[Class] or None
        """
        if base is None:
            base = Class("object")
        self.base = base

        if classes is None:
            classes = []

        self.classes = {}

        self.add_class(self.base)

        for class_ in classes:
            self.add_class(class_)

        self.scope = None

    def add_class(self, class_):
        """
        Add a class to the available class list.
        :param class_: The class to add.
        :type class_: Class
        """
        if class_.name in self.classes:
            if class_ not in self.classes[class_.name]:
                self.classes[class_.name].append(class_)
        else:
            self.classes[class_.name] = [class_]

    def get_class(self, name):
        """
        Get the most recent class binding to the specified name.
        :param name: The name of the class to get.
        :type name: str
        :return: The most recent class binding to the specified name. None if no such class exists/
        :rtype: Class or None
        """
        if name in self.classes:
            return self.classes[name][-1]
        return None

    def visit(self, ast):
        return DependencyGraph(self.base, list(self.classes.values()))

    def visit_children(self, node):
        """
        Visit all of a node's children.
        :param node: The node whose children to visit.
        :type node: ASTNode
        :return: A built sequence of CFGNodes returned by visiting each child. None if no CFGNodes returned.
        :rtype: list[Any]
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
        """
        Visit AST class definition node and add the class to the available class list.
        :param node: The AST class definition node.
        :type node: ASTClassDefinitionNode
        :return: The dependency graph representation of the class.
        :rtype: Class
        """
        # Class name
        name = node.name.name
        if self.scope:
            name = f"{self.scope}.{name}"

        # Class superclasses
        superclasses = [self.base]
        if node.arguments:
            superclasses = node.arguments.accept(self)

        # Dependencies inside the class
        scope_tmp = self.scope
        self.scope = name

        inner_dependencies = [class_ for class_ in node.body.accept(self) if isinstance(class_, Class)]

        self.scope = scope_tmp

        # Create class
        class_ = Class(name, list(set(superclasses + inner_dependencies)))
        self.classes[name] = class_
