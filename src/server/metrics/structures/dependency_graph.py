from metrics.structures.base.graph import Graph, Node


class DependencyGraph(Graph):
    def __init__(self, base=None):
        """
        Dependency Graph.
        :param base: The base class in the given language.
        :type base: Class
        """

        super().__init__(base)

    def __str__(self):
        return f"Dependency graph.\nBase: {self.base}"

    def __repr__(self):
        return f"DependencyGraph(base={self.base})"

    @property
    def base(self):
        return self.root

    @base.setter
    def base(self, new_base):
        self.root = new_base

    @base.deleter
    def base(self):
        del self.root

    def accept(self, visitor):
        """
        Accept a dependency graph visitor.
        :param visitor: The dependency graph visitor to accept.
        :type visitor: DependencyGraphVisitor
        :return: The result of the accept.
        :rtype: Any
        """
        return super().accept(visitor)


class Class(Node):
    def __init__(self, name, dependencies=None):
        """
        Class.
        :param name: The name of the class.
        :type name: str
        :param dependencies: The classes that the class directly depends on.
        :type dependencies: list[Class] or None
        """
        self.name = name

        if dependencies is None:
            dependencies = []

        super().__init__(*dependencies)

    def __str__(self):
        return f"Class.\nDependencies: {self.dependencies}"

    def __repr__(self):
        return f"Class(dependencies={self.dependencies})"

    @property
    def dependencies(self):
        """
        Getter for dependencies property.
        :return: Value of dependencies.
        :rtype: list[DependencyGraphNode] or None
        """
        return self.children

    @dependencies.setter
    def dependencies(self, new_dependencies):
        """
        Setter for dependencies property.
        :param new_dependencies: Value to assign to dependencies.
        :type new_dependencies: list[DependencyGraphNode] or None
        """
        self.children = new_dependencies

    @dependencies.deleter
    def dependencies(self):
        """
        Deleter for dependencies property.
        """
        del self.children
