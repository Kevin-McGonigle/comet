from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Sequence, Any, List

from metrics.structures.base.graph import Graph, Node

if TYPE_CHECKING:
    from metrics.visitors.base.dependency_graph_visitor import DependencyGraphVisitor


class DependencyGraph(Graph):
    def __init__(self, base: Optional["Class"] = None, classes: Optional[Sequence["Class"]] = None):
        """
        Dependency Graph.

        :param base: The base class in the given language.
        :param classes: The classes contained in the graph.
        """
        super().__init__(base if base is not None else KnownClass("object"))
        self.classes = classes if classes is not None else []

    def __str__(self):
        return f"Dependency graph.\nBase: {self.base}\nClasses: {self.classes}"

    def __repr__(self):
        return f"DependencyGraph(base={self.base}, classes={self.classes})"

    @property
    def base(self) -> Optional["Class"]:
        """
        Getter for base property.

        :return: The base class in the tree.
        """
        return self.root

    @base.setter
    def base(self, new_base: Optional["Class"]):
        """
        Setter for base property.

        :param new_base: The value to assign to base.
        """
        self.root = new_base

    @base.deleter
    def base(self):
        """
        Deleter for base property.
        """
        del self.root

    def accept(self, visitor: "DependencyGraphVisitor"):
        """
        Accept a dependency graph visitor and visit each of the classes in the graph.

        :param visitor: The dependency graph visitor to accept.
        :return: The result of the accept.
        """
        return {cls: cls.accept(visitor) for cls in self.classes}


class Class(Node):
    """
    Class.

    Dependency graph representation of a class, with a list of dependencies that
    the class directly depends on.
    """

    def __init__(self, name: Optional[str] = None, dependencies: Optional[Sequence["Class"]] = None):
        """
        Class.

        :param name: The name of the class.
        :param dependencies: The classes that the class directly depends on.
        """
        super().__init__(*(dependencies if dependencies is not None else []))
        self.name = name

    def __str__(self):
        return f"Class.\nName: {self.name}\nDependencies: {self.dependencies}"

    def __repr__(self):
        return f"Class(name={self.name}, dependencies={self.dependencies})"

    @property
    def dependencies(self) -> List["Class"]:
        """
        Getter for dependencies property.

        :return: Value of dependencies.
        """
        return self.children

    @dependencies.setter
    def dependencies(self, new_dependencies: List["Class"]):
        """
        Setter for dependencies property.

        :param new_dependencies: Value to assign to dependencies.
        """
        self.children = new_dependencies

    @dependencies.deleter
    def dependencies(self):
        """
        Deleter for dependencies property.
        """
        del self.children

    def accept(self, visitor: "DependencyGraphVisitor"):
        """
        Accept a dependency graph visitor and call its visit_class method.

        :param visitor: The dependency graph visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_class(self)

    def add_dependency(self, dependency: "Class"):
        """
        Add a dependency to the class.

        :param dependency: The dependency to add.
        """
        self.add_child(dependency)

    def add_dependent(self, dependent: "Class"):
        """
        Add the class as a dependency of the dependent.

        :param dependent: The dependent.
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
        :param dependencies: The classes that this class directly depends on.
        """
        super().__init__(name, dependencies)

    def __str__(self):
        return f"Known class.\nName: {self.name}\nDependencies: {self.dependencies}"

    def __repr__(self):
        return f"KnownClass(name={self.name}, dependencies={self.dependencies})"

    def accept(self, visitor: "DependencyGraphVisitor"):
        """
        Accept a dependency graph visitor and call its visit_known_class method.

        :param visitor: The dependency graph visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_known_class(self)


class UnknownClass(Class):
    """
    Unknown class.

    A class that cannot be identified due to an unsupported argument/parameter expression
    (e.g. function call, positional/keyword unpacking or generator expression),
    an identifier that does not map to a known class, etc.
    """

    def __init__(self, name=None, dependencies=None, reason: Optional[str] = None):
        """
        Unknown class.

        :param name: The name of the class.
        :param dependencies: The classes that the class directly depends on.
        :param reason: The reason that the class cannot be identified.
        """
        super().__init__(name, dependencies)
        self.reason = reason

    def __str__(self):
        return f"Unknown class.\nName: {self.name}\nDependencies: {self.dependencies}\nReason: {self.reason}"

    def __repr__(self):
        return f"UnknownClass(name={self.name}, dependencies={self.dependencies}, reason={self.reason})"

    def accept(self, visitor: "DependencyGraphVisitor"):
        """
        Accept a dependency graph visitor and call its visit_unknown_class method.

        :param visitor: The dependency graph visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_unknown_class(self)
