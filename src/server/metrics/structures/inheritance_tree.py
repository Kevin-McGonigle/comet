from typing import TYPE_CHECKING, Optional, Sequence, List, Union

from metrics.structures.base.graph import Graph, Node

if TYPE_CHECKING:
    from metrics.visitors.base.inheritance_tree_visitor import *


class InheritanceTree(Graph):
    """
    Inheritance tree.
    """

    def __init__(self, base: Optional["Class"] = None):
        """
        Inheritance tree.

        :param base: The base class in the given language.
        """
        super().__init__(base if base is not None else KnownClass("object"))

    def __str__(self):
        return f"Inheritance tree.\nBase: {self.base}"

    def __repr__(self):
        return f"InheritanceTree(base={self.base})"

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

    def accept(self, visitor: "InheritanceTreeVisitor"):
        """
        Accept an inheritance tree visitor.

        :param visitor: The inheritance tree visitor to accept.
        :return: The result of the accept.
        """
        return self.base.accept(visitor)


class Class(Node):
    """
    Class.

    Inheritance tree representation of a class, with a list of subclasses that
    directly inherit the class.
    """

    def __init__(self, name: Optional[str] = None, subclasses: Optional[Sequence["Class"]] = None):
        """
        Class.

        :param name: The name of the class.
        :param subclasses: The classes that directly inherit from the class.
        """
        super().__init__(*(subclasses if subclasses is not None else []))
        self.name = name

    def __str__(self):
        return f"Class.\nName: {self.name}\nSubclasses: {self.subclasses}"

    def __repr__(self):
        return f"Class(name={self.name}, subclasses={self.subclasses})"

    @property
    def subclasses(self) -> List["Class"]:
        """
        Getter for subclasses property.

        :return: The classes that directly inherit from the class.
        """
        return self.children

    @subclasses.setter
    def subclasses(self, new_subclasses: List["Class"]):
        """
        Setter for subclasses property.

        :param new_subclasses: The value to assign to subclasses.
        """
        self.children = new_subclasses

    @subclasses.deleter
    def subclasses(self):
        """
        Deleter for the subclasses property.
        """
        del self.children

    def accept(self, visitor: "InheritanceTreeVisitor"):
        """
        Accept an inheritance tree visitor and call its visit_class method.

        :param visitor: The inheritance tree visitor to accept
        :return: The result of the accept.
        """
        return visitor.visit_class(self)

    def add_subclass(self, subclass: "Class"):
        """
        Add a subclass to the class.

        :param subclass: The subclass to add.
        """
        self.add_child(subclass)

    def add_superclass(self, superclass: "Class"):
        """
        Add a superclass to the class.

        :param superclass: The superclass to add.
        """
        superclass.add_subclass(self)


class KnownClass(Class):
    """
    Known class.

    A class that is known with a valid identifier.
    """

    def __init__(self, name: str, subclasses: Optional[Sequence["Class"]] = None,
                 methods: Optional[Sequence["Method"]] = None):
        """
        Known class.

        :param name: The name of the class represented by the node.
        :param subclasses: The classes that directly inherit from the class.
        :type methods: list[Method] or None
        """
        super().__init__(name, subclasses)
        self.methods = methods if methods is not None else []

    def __str__(self):
        return f"Known class.\nName: {self.name}\nSubclasses: {self.subclasses}\nMethods: {self.methods}"

    def __repr__(self):
        return f"KnownClass(name={self.name}, subclasses={self.subclasses}, methods={self.methods})"

    def accept(self, visitor):
        """
        Accept an inheritance tree visitor and call its visit_known_class method.

        :param visitor: The inheritance tree visitor to accept.
        :return: The result of the accept.
        """
        return visitor.visit_known_class(self)


class UnknownClass(Class):
    """
    Unknown class.

    A class that cannot be identified due to an unsupported argument/parameter expression
    (e.g. function call, positional/keyword unpacking or generator expression),
    an identifier that does not map to a known class, etc.
    """

    def __init__(self, name: Optional[str] = None, subclasses: Optional[Sequence["Class"]] = None,
                 reason: Optional[str] = None):
        """
        Unknown class.
        :param name: The name of the class.
        :param subclasses: The classes that directly inherit from the class.
        :param reason: The reason that the class cannot be identified.
        """
        super().__init__(name, subclasses)
        self.reason = reason

    def __str__(self):
        return f"Unknown class.\nName: {self.name}\nSubclasses: {self.subclasses}\nReason: {self.reason}"

    def __repr__(self):
        return f"UnknownClass(name={self.name}, subclasses={self.subclasses}, reason={self.reason})"

    def accept(self, visitor):
        """
        Accept an inheritance tree visitor and call its visit_unknown_class method.

        :param visitor: The inheritance tree visitor to accept.
        :return: The result of the accept.
        """
        return visitor.visit_unknown_class(self)


class Method:
    def __init__(self, name: str, parameters: Optional[
        Sequence[Union["Parameter", "PositionalArgumentsParameter", "KeywordArgumentsParameter"]]] = None,
                 return_type: Optional[str] = None):
        """
        Method.

        :param name: The name of the method.
        :param parameters: The method's parameters.
        :param return_type: The method's return type.
        """
        self.name = name
        self.parameters = parameters if parameters is not None else []
        self.return_type = return_type

    def __str__(self):
        return f"Method.\nName: {self.name}\nParameters: {self.parameters}\nReturn type: {self.return_type}"

    def __repr__(self):
        return f"Method(name={self.name}, parameters={self.parameters}, return_type={self.return_type})"


class Parameter:
    def __init__(self, name: str, type_: Optional[str] = None, default: Optional[str] = None):
        """
        Parameter.

        :param name: The name of the parameter
        :param type_: The parameter's type.
        :param default: The parameter's default value.
        """
        self.name = name
        self.type = type_
        self.default = default

    def __str__(self):
        return f"Parameter.\nName: {self.name}\nType: {self.type}\nDefault: {self.default}"

    def __repr__(self):
        return f"Parameter(name={self.name}, type={self.type}, default={self.default})"


class PositionalArgumentsParameter:
    def __init__(self, name: str, type_: Optional[str] = None):
        """
        Positional arguments parameter.
        :param name: The name of the positional arguments parameter
        :param type_: The parameter's type.
        """
        self.name = name
        self.type = type_

    def __str__(self):
        return f"Positional arguments parameter.\nName: {self.name}\nType: {self.type}"

    def __repr__(self):
        return f"PositionalArgumentsParameter(name={self.name}, type={self.type})"


class KeywordArgumentsParameter:
    def __init__(self, name: str, type_: Optional[str] = None):
        """
        Keyword arguments parameter.

        :param name: The name of the keyword arguments parameter.
        :param type_: The parameter's type.
        """
        self.name = name
        self.type = type_

    def __str__(self):
        return f"Keyword arguments parameter.\nName: {self.name}\nType: {self.type}"

    def __repr__(self):
        return f"KeywordArgumentsParameter(name={self.name}, type={self.type})"
