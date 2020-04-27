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

    def accept(self, visitor):
        return super().accept(visitor)


class DependencyGraphNode(Node):
    def __init__(self, dependencies=None):
        """
        Dependency Graph Node.
        :param dependencies: The nodes that this node directly depends on.
        :type dependencies: list[DependencyGraphNode] or None
        """
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
    pass


class Class(DependencyGraphNode):
    pass


class Method(DependencyGraphNode):
    pass
