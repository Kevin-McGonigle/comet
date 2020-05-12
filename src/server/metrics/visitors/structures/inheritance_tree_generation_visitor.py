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
            base = KnownClass("object")
        self.base = base

        if classes is None:
            classes = []

        self.classes = {}

        self.add_class(self.base)

        for class_ in classes:
            self.add_class(class_)

        self.scope = None

        super().__init__()
    
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

    def visit(self, ast):
        """
        Visit the AST and produce an inheritance tree.
        :param ast: The AST to visit.
        :type ast: AST
        :return: The generated inheritance tree.
        :rtype: InheritanceTree
        """
        return InheritanceTree(self.base)

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
        name = node.name.accept(self)
        if self.scope:
            name = self.scope + "." + name

        # Class bases
        if node.bases:
            superclasses = node.bases.accept(self)
        else:
            superclasses = [self.base]

        # Class methods
        tmp = self.scope
        self.scope = name

        methods = [method for method in (node.body.accept(self)) if isinstance(method, Method)]

        self.scope = tmp

        # Create class
        cls = KnownClass(name, methods=methods)

        # Add as a subclass to bases
        for superclass in superclasses:
            cls.add_superclass(superclass)

        self.add_class(cls)

    def visit_function_definition(self, node):
        """
        Visit AST function definition node and return a corresponding method object.
        :param node: The AST function definition node.
        :type node: ASTFunctionDefinitionNode
        :return: The corresponding method object.
        :rtype: Method
        """
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
        self.scope = f"{self.scope}.{name}.<locals>" if self.scope else f"{name}.<locals>"

        node.body.accept(self)

        self.scope = tmp

        # Create method
        return Method(name, parameters, return_type)

    def visit_argument(self, node):
        """
        Visit AST argument node and return the corresponding class object. 
        :param node: The AST argument node.
        :type node: ASTArgumentNode
        :return: The corresponding class object. Unknown class/classes object if a corresponding class cannot be found.
        :rtype: Class
        """
        if isinstance(node.value, ASTIdentifierNode) or isinstance(node.value, ASTMemberNode):
            # Superclass name
            name = node.value.accept(self)
            if isinstance(name, UnknownClass):
                return name

            # Check for class at same scope
            if self.scope:
                cls = self.get_class(f"{self.scope}.{name}")
                if cls:
                    return cls

            # Check for class at global scope
            cls = self.get_class(name)
            if cls:
                return cls

            if not self.scope:
                cls = UnknownClass(name, reason=f"Class with name \"{name}\" cannot be found globally.")
            else:
                cls = UnknownClass(name,
                                   reason=f"Class with name \"{name}\" cannot be found at scope {self.scope} "
                                          f"or globally.")

        elif isinstance(node.value, ASTPositionalUnpackExpressionNode):
            cls = UnknownClass(reason="Unpacking positional arguments from iterable.")

        elif isinstance(node.value, ASTKeywordUnpackExpressionNode):
            cls = UnknownClass(reason="Unpacking keyword arguments from key-value map.")

        else:
            cls = UnknownClass(reason=f"{node.value} unsupported for class identification. Type: {type(node.value)}")

        cls.add_superclass(self.base)
        return cls

    def visit_member(self, node):
        """
        Visit AST member node and return the dot-separated string of parent and member. 
        :param node: The AST member node.
        :type node: ASTMemberNode
        :return: Dot-separated string of parent and member. Unknown class if anything other than identifiers are found.
        :rtype: str or UnknownClass
        """
        if isinstance(node.parent, ASTIdentifierNode) or isinstance(node.parent, ASTMemberNode):
            if isinstance(node.member, ASTIdentifierNode or isinstance(node.member, ASTMemberNode)):
                parent = node.parent.accept(self)
                if isinstance(parent, UnknownClass):
                    return parent

                member = node.member.accept(self)
                if isinstance(member, UnknownClass):
                    return member

                return parent + "." + member
            else:
                cls = UnknownClass(reason=f"{node.member} unsupported for class identification. "
                                          f"Type: {type(node.member)}")
        else:
            cls = UnknownClass(reason=f"{node.parent} unsupported for class identification. "
                                      f"Type: {type(node.parent)}")
        cls.add_superclass(self.base)
        return cls

    def visit_parameter(self, node):
        """
        Visit AST parameter node and return the corresponding parameter node.
        :param node: The AST parameter node.
        :type node: ASTParameterNode
        :return: The corresponding parameter node.
        :rtype: Parameter
        """
        return Parameter(node.name.accept(self))

    def visit_positional_arguments_parameter(self, node):
        """
        Visit AST positional arguments parameter node and return the corresponding positional arguments parameter node.
        :param node: The AST positional arguments parameter node.
        :type node: ASTPositionalArgumentsParameterNode
        :return: The corresponding positional arguments parameter node.
        :rtype: PositionalArgumentsParameter
        """
        return PositionalArgumentsParameter(node.name.accept(self))

    def visit_keyword_arguments_parameter(self, node):
        """
        Visit AST keyword arguments parameter node and return the corresponding keyword arguments parameter node.
        :param node: The AST keyword arguments parameter node.
        :type node: ASTKeywordArgumentsParameterNode
        :return: The corresponding keyword arguments parameter node.
        :rtype: KeywordArgumentsParameter
        """
        return KeywordArgumentsParameter(node.name.accept(self))

    def visit_identifier(self, node):
        """
        Visit AST identifier node and return the identifier's name.
        :param node: The AST identifier node.
        :type node: ASTIdentifierNode
        :return: The identifier's name.
        :rtype: str
        """
        return node.name
