from typing import TYPE_CHECKING

from metrics.structures.base.graph import *

if TYPE_CHECKING:
    from metrics.visitors.base.inheritance_tree_visitor import *


class InheritanceTree(Graph):
    def __init__(self, base=None):
        """
        Inheritance tree.
        :param base: The base class in the given language.
        :type base: Class or None
        """
        super().__init__(base if base is not None else KnownClass("object"))

    def __str__(self):
        return f"Inheritance tree.\nBase: {self.base}"

    def __repr__(self):
        return f"InheritanceTree(base={self.base})"

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
        Accept an inheritance tree visitor.
        :param visitor: The inheritance tree visitor to accept.
        :type visitor: InheritanceTreeVisitor
        :return: The result of the accept.
        :rtype: Any
        """
        return self.base.accept(visitor)


class Class(Node):
    """
    Class.
    
    Inheritance tree representation of a class, with a list of subclasses that
    directly inherit the class.
    """
    def __init__(self, name=None, subclasses=None):
        """
        Class.
        :param name: The name of the class
        :type name: str
        :param subclasses: The classes that directly inherit from the class. 
        :type subclasses: list[Class]
        """
        self.name = name
        
        if subclasses is None:
            subclasses = []
            
        super().__init__(*subclasses)
        
    def __str__(self):
        return f"Class.\nName: {self.name}\nSubclasses: {self.subclasses}"

    def __repr__(self):
        return f"Class(name={self.name}, dependencies={self.subclasses})"

    @property
    def subclasses(self):
        """
        Getter for subclasses property.
        :return: The classes that directly inherit from the class.
        :rtype: list[Class]
        """
        return self.children

    @subclasses.setter
    def subclasses(self, new_subclasses):
        """
        Setter for subclasses property.
        :param new_subclasses: The value to assign to subclasses.
        :type new_subclasses: list[Class]
        """
        self.children = new_subclasses

    @subclasses.deleter
    def subclasses(self):
        """
        Deleter for the subclasses property.
        """
        del self.children

    def accept(self, visitor):
        """
        Accept an inheritance tree visitor and call its visit_class method.
        :param visitor: The inheritance tree visitor to accept.
        :type visitor: InheritanceTreeVisitor
        :return: The result of the accept.
        :rtype: Any
        """
        return visitor.visit_class(self)

    def add_subclass(self, subclass):
        """
        Add a subclass to the class.
        :param subclass: The subclass to add.
        :type subclass: Class
        """
        self.add_child(subclass)

    def add_superclass(self, superclass):
        """
        Add a superclass to the class.
        :param superclass: The superclass to add.
        :type superclass: Class
        """
        superclass.add_subclass(self)


class KnownClass(Class):
    """
    Known class.

    A class that is known with a valid identifier.
    """
    def __init__(self, name, subclasses=None, methods=None):
        """
        Known class.
        :param name: The name of the class represented by the node.
        :type name: str
        :param subclasses: The classes that directly inherit from the class.
        :type subclasses: list[Class] or None
        :param methods: The class' methods.
        :type methods: list[Method] or None
        """
        if methods is None:
            methods = []
        self.methods = methods

        super().__init__(name, subclasses)

    def __str__(self):
        return f"Known class.\nName: {self.name}\nSubclasses: {self.subclasses}\nMethods: {self.methods}"

    def __repr__(self):
        return f"KnownClass(name={self.name}, subclasses={self.subclasses}, methods={self.methods})"

    def accept(self, visitor):
        """
        Accept an inheritance tree visitor and call its visit_known_class method.
        :param visitor: The inheritance tree visitor to accept.
        :type visitor: InheritanceTreeVisitor
        :return: The result of the accept.
        :rtype: Any
        """
        return visitor.visit_known_class(self)


class UnknownClass(Class):
    """
    Unknown class.

    A class that cannot be identified due to an unsupported argument/parameter expression
    (e.g. function call, positional/keyword unpacking or generator expression),
    an identifier that does not map to a known class, etc.
    """

    def __init__(self, name=None, subclasses=None, reason=None):
        """
        Unknown class.
        :param name: The name of the class.
        :type name: str
        :param subclasses: The classes that directly inherit from the class.
        :type subclasses: list[Class] or None
        :param reason: The reason that the class cannot be identified.
        :type reason: str or None
        """
        self.reason = reason

        super().__init__(name, subclasses)

    def __str__(self):
        return f"Unknown class.\nName: {self.name}\nSubclasses: {self.subclasses}\nReason: {self.reason}"

    def __repr__(self):
        return f"UnknownClass(name={self.name}, subclasses={self.subclasses}, reason={self.reason})"

    def accept(self, visitor):
        """
        Accept an inheritance tree visitor and call its visit_unknown_class method.
        :param visitor: The inheritance tree visitor to accept.
        :type visitor: InheritanceTreeVisitor
        :return: The result of the accept.
        :rtype: Any
        """
        return visitor.visit_unknown_class(self)


class Method:
    def __init__(self, name, parameters=None, return_type=None):
        """
        Method.
        :param name: The name of the method.
        :type name: str
        :param parameters: The method's parameters.
        :type parameters: list[Parameter or PositionalArgumentsParameter or KeywordArgumentsParameter] or None
        :param return_type: The method's return type.
        :type return_type: str or None
        """
        self.name = name
        self.parameters = parameters if parameters is not None else []
        self.return_type = return_type

    def __str__(self):
        return f"Method.\nName: {self.name}\nParameters: {self.parameters}\nReturn type: {self.return_type}"

    def __repr__(self):
        return f"Method(name={self.name}, parameters={self.parameters}, return_type={self.return_type})"


class Parameter:
    def __init__(self, name, type_=None, default=None):
        """
        Parameter.
        :param name: The name of the parameter
        :type name: str
        :param type_: The parameter's type.
        :type type_: str or None
        :param default: The parameter's default value.
        :type default: str or None
        """
        self.name = name
        self.type = type_
        self.default = default

    def __str__(self):
        return f"Parameter.\nName: {self.name}\nType: {self.type}\nDefault: {self.default}"

    def __repr__(self):
        return f"Parameter(name={self.name}, type={self.type}, default={self.default})"
    
    
class PositionalArgumentsParameter:
    def __init__(self, name, type_=None):
        """
        Positional arguments parameter.
        :param name: The name of the positional arguments parameter
        :type name: str
        :param type_: The parameter's type.
        :type type_: str or None
        """
        self.name = name
        self.type = type_

    def __str__(self):
        return f"Positional arguments parameter.\nName: {self.name}\nType: {self.type}"

    def __repr__(self):
        return f"PositionalArgumentsParameter(name={self.name}, type={self.type})"


class KeywordArgumentsParameter:
    def __init__(self, name, type_=None):
        """
        Keyword arguments parameter.
        :param name: The name of the keyword arguments parameter
        :type name: str
        :param type_: The parameter's type.
        :type type_: str or None
        """
        self.name = name
        self.type = type_

    def __str__(self):
        return f"Keyword arguments parameter.\nName: {self.name}\nType: {self.type}"

    def __repr__(self):
        return f"KeywordArgumentsParameter(name={self.name}, type={self.type})"
