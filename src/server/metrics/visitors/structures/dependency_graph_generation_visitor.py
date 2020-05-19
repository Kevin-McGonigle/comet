from metrics.structures.ast import *
from metrics.structures.dependency_graph import *
from metrics.visitors.base.ast_visitor import ASTVisitor


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
        ast.accept(self)
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
        for child in node.children.values():
            child_result = child.accept(self) if child is not None else None
            if child_result:
                if isinstance(child_result, list):
                    child_results += child_result
                elif child_result:
                    child_results.append(child_result)

        return child_results

    def visit_class_definition(self, node):
        """
        Visit AST class definition node and add the class to the available class list.

        :param node: The AST class definition node.
        :type node: ASTClassDefinitionNode
        """
        # Class name
        name = node['name'].accept(self)
        if self.scope:
            name = f"{self.scope}.{name}"

        # Class bases
        superclasses = [self.base]
        if node['bases']:
            superclasses = node['bases'].accept(self)
            if not isinstance(superclasses, list):
                superclasses = [superclasses]

        # Dependencies inside the class
        scope_tmp = self.scope
        self.scope = name

        inner_dependencies = [class_ for class_ in node['body'].accept(self) if isinstance(class_, Class)]

        self.scope = scope_tmp

        # Create class
        if name in self.classes:
            self.classes[name].append(Class(name, list(set(superclasses + inner_dependencies))))
        else:
            self.classes[name] = [Class(name, list(set(superclasses + inner_dependencies)))]

    def visit_argument(self, node):
        return self.get_dependency(node['value'])

    def visit_function_definition(self, node):
        """
        Visit AST function definition node and return its dependencies.

        :param node: The AST function definition node.
        :type node: ASTFunctionDefinitionNode
        :return: The corresponding method object.
        :rtype: Method
        """
        name = node['name'].accept(self)
        if self.scope:
            name = f"{self.scope}.{name}"

        dependencies = []
        if node['parameters']:
            dependencies = [class_ for class_ in node['parameters'].accept(self) if isinstance(class_, Class)]

        return_dependency = self.get_dependency(node['return_type'])
        if return_dependency:
            dependencies.append(return_dependency)

        scope_tmp = self.scope
        self.scope = f"{self.scope}.{name}.<locals>" if self.scope else f"{name}.<locals>"

        node['body'].accept(self)

        self.scope = scope_tmp

        return dependencies

    def visit_parameter(self, node):
        """
        Visit AST parameter node and return its dependency (if one exists).

        :param node: The AST parameter node.
        :type node: ASTParameterNode
        :return: The parameter's dependency. None if the parameter has no type.
        :rtype: Class or None
        """
        return self.get_dependency(node['type'])

    def visit_positional_arguments_parameter(self, node):
        """
        Visit AST positional arguments parameter node and return its dependency (if one exists).

        :param node: The AST positional arguments parameter node.
        :type node: ASTPositionalArgumentsParameterNode
        :return: The positional arguments parameter's dependency. None if the parameter has no type.
        :rtype: Class or None
        """
        return self.get_dependency(node['type'])

    def visit_member(self, node):
        """
        Visit AST member node and return the dot-separated string of parent and member.

        :param node: The AST member node.
        :type node: ASTMemberNode
        :return: Dot-separated string of parent and member. Unknown class if anything other than identifiers are found.
        :rtype: str or UnknownClass
        """
        if isinstance(node['parent'], (ASTIdentifierNode, ASTMemberNode)):
            if isinstance(node['member'], (ASTIdentifierNode, ASTMemberNode)):
                parent = node['parent'].accept(self)
                if isinstance(parent, UnknownClass):
                    return parent

                member = node['member'].accept(self)
                if isinstance(member, UnknownClass):
                    return member

                return parent + "." + member
            return UnknownClass(dependencies=[self.base],
                                reason=Reason.unsupported(node['member']))
        return UnknownClass(dependencies=[self.base],
                            reason=Reason.unsupported(node['parent']))

    def visit_identifier(self, node):
        return node.name

    def get_dependency(self, type_):
        """
        Get the dependency of a node's type attribute.

        :param type_: The type attribute.
        :type type_: ASTNode or None
        :return: The dependency of the parameter. None if the parameter has no type.
        :rtype: Class or None
        """
        if type_:
            if isinstance(type_, (ASTIdentifierNode, ASTMemberNode)):
                type_name = type_.accept(self)
                if isinstance(type_name, Class):
                    return type_name

                if self.scope:
                    class_ = self.get_class(f"{self.scope}.{type_name}")
                    if class_:
                        return class_

                class_ = self.get_class(type_name)
                if class_:
                    return class_

                return UnknownClass(name=type_name, dependencies=[self.base],
                                    reason=Reason.not_found(type_name, self.scope))
            return UnknownClass(dependencies=[self.base], reason=Reason.unsupported(type_))


class Reason:
    @staticmethod
    def not_found(class_name, scope=None):
        """
        Return a reason string for a class that cannot be found.

        :param class_name: The name of the class that cannot be found.
        :type class_name: str
        :param scope: The scope being searched for local definitions. None if only scope is global.
        :type scope: str or None
        :return: Not found reason string.
        :rtype: str
        """
        if scope:
            return f"A class with name \"{class_name}\" cannot be found at scope {scope} or globally."

        return f"A class with name \"{class_name}\" cannot be found."

    @staticmethod
    def unsupported(node):
        """
        Return a reason string for an AST node that is an unsupported type for class identification.

        :param node: The node that is not supported.
        :type node: ASTNode
        :return: Unsupported reason string. 
        :rtype: str
        """
        return f"{node} is not supported for class identification. Type: {type(node)}"
