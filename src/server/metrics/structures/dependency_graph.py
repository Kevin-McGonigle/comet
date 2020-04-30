from metrics.structures.base.graph import Graph, Node


class DependencyGraph(Graph):
    def __init__(self, base=None, classes=None):
        """
        Dependency Graph.
        :param base: The base class in the given language.
        :type base: Class
        :param classes: The classes contained in the graph.
        :type classes: list[Class]
        """
        if classes is None:
            classes = []
        self.classes = classes

        super().__init__(base)

    def __str__(self):
        return f"Dependency graph.\nBase: {self.base}\nClasses: {self.classes}"

    def __repr__(self):
        return f"DependencyGraph(base={self.base}, classes={self.classes})"

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
        return f"Class.\nName: {self.name}\nDependencies: {self.dependencies}"

    def __repr__(self):
        return f"Class(name={self.name}, dependencies={self.dependencies})"

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

    def add_dependency(self, dependency):
        """
        Add a dependency to the class.
        :param dependency: The dependency to add.
        :type dependency: Class
        """
        self.add_child(dependency)

    def add_dependent(self, dependent):
        """
        Add the class as a dependency of the dependent.
        :param dependent: The dependent.
        :type dependent: Class
        """
        dependent.add_dependent(self)
