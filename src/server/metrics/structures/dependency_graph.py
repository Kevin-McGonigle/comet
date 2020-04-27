from metrics.structures.base.graph import Graph, Node


class DependencyGraph(Graph):
    def __init__(self, entry=None):
        """
        Dependency Graph.
        :param entry: The entry package/class/method in the dependency graph.
        :type entry: DependencyGraphNode
        """
        super().__init__(entry)

    def __str__(self):
        s = "Dependency graph"

        if self.entry:
            s += f"\nEntry: {self.entry}"

        return s

    def __repr__(self):
        return "Dependency graph"


class DependencyGraphNode(Node):
    def __init__(self, name, dependencies=None):
        """
        Dependency Graph Node.
        :param name: The name of the node.
        :type name: str
        :param dependencies: The nodes that the node directly depends on.
        :type dependencies: list[DependencyGraphNode] or None
        """
        self.name = name

        if dependencies is None:
            dependencies = []

        super().__init__(*dependencies)

    def __str__(self):
        s = "Dependency graph node"

        if self.dependencies:
            s += f"\nDependencies: {self.dependencies}"

        return s

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


class Package(DependencyGraphNode):
    def __init__(self, name, dependencies=None, classes=None, functions=None):
        """
        Package.
        :param name: The name of the package.
        :type name: str
        :param dependencies: The nodes that the package directly depends on.
        :type dependencies: list[DependencyGraphNode] or None
        :param classes: The classes contained within the package.
        :type classes: list[Class] or None
        :param functions: The functions contained within the package.
        :type functions: list[Method] or None
        """
        if classes is None:
            classes = []
        self.classes = classes

        if functions is None:
            functions = []
        self.functions = functions

        super().__init__(name, dependencies)

    def __str__(self):
        s = "Package"

        if self.dependencies:
            s += f"\nDependencies: {self.dependencies}"

        if self.classes:
            s += f"\nClasses: {self.classes}"

        if self.functions:
            s += f"\nFunctions: {self.functions}"

        return s


class Class(DependencyGraphNode):
    def __init__(self, name, dependencies=None, methods=None):
        """
        Class.
        :param name: The name of the class.
        :type name: str
        :param dependencies: The nodes that the class directly depends on.
        :type dependencies: list[DependencyGraphNode] or None
        :param methods: The class' methods.
        :type methods: list[Method] or None
        """
        if methods is None:
            methods = []
        self.methods = methods

        super().__init__(name, dependencies)

    def __str__(self):
        s = "Class"

        if self.dependencies:
            s += f"\nDependencies: {self.dependencies}"

        if self.methods:
            s += f"\nMethods: {self.methods}"

        return s


class Method(DependencyGraphNode):
    def __init__(self, name, dependencies=None):
        """
        Method/Function.
        :param name: The name of the method/function.
        :type name: str
        :param dependencies: The nodes that the method/function directly depends on.
        :type dependencies: list[DependencyGraphNode] or None
        """
        super().__init__(name, dependencies)

    def __str__(self):
        s = "Method/Function"

        if self.name:
            s += f"\nName: {self.name}"

        if self.dependencies:
            s += f"\nDependencies: {self.dependencies}"

        return s
