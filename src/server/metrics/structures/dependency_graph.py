from typing import TYPE_CHECKING

from metrics.structures.base.graph import Graph, Node

if TYPE_CHECKING:
    from metrics.visitors.base.dependency_graph_visitor import *


class DependencyGraph(Graph):
    def __init__(self, base=None, classes=None):
        """
        Dependency Graph.
        :param base: The base class in the given language.
        :type base: Class or None
        :param classes: The classes contained in the graph.
        :type classes: list[Class] or None
        """
        if classes is None:
            classes = []
        self.classes = classes

        super().__init__(base if base is not None else KnownClass("object"))

    def __str__(self):
        return f"Dependency graph.\nBase: {self.base}\nClasses: {self.classes}"

    def __repr__(self):
        return f"DependencyGraph(base={self.base}, classes={self.classes})"

    @property
    def base(self):
        """
        Getter for base property.
        :return: The base class in the tree.
        :rtype: Class or None
        """
        return self.root

    @base.setter
    def base(self, new_base):
        """
        Setter for base property.
        :param new_base: The value to assign to base.
        :type new_base: Class or None
        """
        self.root = new_base

    @base.deleter
    def base(self):
        """
        Deleter for base property.
        """
        del self.root

    def accept(self, visitor):
        """
        Accept a dependency graph visitor and visit each of the classes in the graph.
        :param visitor: The dependency graph visitor to accept.
        :type visitor: DependencyGraphVisitor
        :return: The result of the accept.
        :rtype: Any
        """
        return {cls: cls.accept(visitor) for cls in self.classes}


class Class(Node):
    """
    Class.

    Dependency graph representation of a class, with a list of dependencies that
    the class directly depends on.
    """
    def __init__(self, name=None, dependencies=None):
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

    def accept(self, visitor):
        """
        Accept a dependency graph visitor and call its visit_class method.
        :param visitor: The dependency graph visitor to accept.
        :type visitor:
        :return:
        :rtype:
        """
        return visitor.visit_class(self)

    @property
    def dependencies(self):
        """
        Getter for dependencies property.
        :return: Value of dependencies.
        :rtype: list[Class] or None
        """
        return self.children

    @dependencies.setter
    def dependencies(self, new_dependencies):
        """
        Setter for dependencies property.
        :param new_dependencies: Value to assign to dependencies.
        :type new_dependencies: list[Class] or None
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
        dependent.add_dependency(self)


class KnownClass(Class):
    """
    Known class.

    A class that is known with a valid identifier.
    """

    def __init__(self, name=None, dependencies=None):
        """
        Known class.
        :param name: The name of the class.
        :type name: str
        :param dependencies: The classes that this class directly depends on.
        :type dependencies: list[Class] or None
        """
        super().__init__(name, dependencies)

    def __str__(self):
        return f"Known class.\nName: {self.name}\nDependencies: {self.dependencies}"

    def __repr__(self):
        return f"KnownClass(name={self.name}, dependencies={self.dependencies})"


class UnknownClass(Class):
    """
    Unknown class.

    A class that cannot be identified due to an unsupported argument/parameter expression
    (e.g. function call, positional/keyword unpacking or generator expression),
    an identifier that does not map to a known class, etc.
    """

    def __init__(self, name=None, dependencies=None, reason=None):
        """
        Unknown class.
        :param name: The name of the class.
        :type name: str
        :param dependencies: The classes that the class directly depends on.
        :type dependencies: list[Class] or None
        :param reason: The reason that the class cannot be identified.
        :type reason: str
        """
        self.reason = reason
        super().__init__(name, dependencies)

    def __str__(self):
        return f"Unknown class.\nName: {self.name}\nDependencies: {self.dependencies}\nReason: {self.reason}"

    def __repr__(self):
        return f"UnknownClass(name={self.name}, dependencies={self.dependencies}, reason={self.reason})"
