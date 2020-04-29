from metrics.structures.base.graph import *


class InheritanceTree(Graph):
    def __init__(self, base=None):
        """
        Inheritance tree.
        :param base: The base class in the tree.
        :type base: Class or None
        """
        super().__init__(base if base is not None else Class("object"))

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


class Class(Node):
    def __init__(self, name, superclasses=None, methods=None):
        """
        Class.
        :param name: The name of the class represented by the node.
        :type name: str
        :param superclasses: The classes that the class inherits from.
        :type superclasses: list[Class] or None
        :param methods: The class' methods.
        :type methods: list[Method] or None
        """
        self.name = name

        if superclasses is None:
            superclasses = []

        self.methods = methods if methods is not None else []

        super().__init__(*superclasses)

    def __str__(self):
        return f"Class.\nName: {self.name}\nSuperclasses: {self}\nMethods: {self.methods}"

    def __repr__(self):
        return f"Class(name={self.name}, superclasses={self.superclasses}, methods={self.methods})"

    @property
    def superclasses(self):
        """
        Getter for superclasses property.
        :return: The classes that the class inherits from.
        :rtype: list[Class] or None
        """
        return self.children

    @superclasses.setter
    def superclasses(self, new_superclasses):
        """
        Setter for superclasses property.
        :param new_superclasses: The value to assign to superclasses.
        :type new_superclasses: list[Class] or None
        """
        self.children = new_superclasses

    @superclasses.deleter
    def superclasses(self):
        """
        Deleter for the superclasses property.
        """
        del self.children

    def add_subclass(self, subclass):
        """
        Add a subclass to the class.
        :param subclass: The subclass to add.
        :type subclass: Class
        """
        subclass.add_superclass(self)

    def add_superclass(self, superclass):
        """
        Add a superclass to the class.
        :param superclass: The superclass to add.
        :type superclass: Class or UnknownClass or UnknownClasses
        """
        self.add_child(superclass)


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


class UnknownClass(Class):
    def __init__(self, base, name=None, reason=None):
        """
        A class that cannot be evaluated.
        :param base: The base class.
        :type base: Class
        :param name: The name of the unknown class.
        :type name: str or None
        :param reason: The reason for the class being unknown.
        :type reason: str or None
        """
        self.reason = reason

        super().__init__(self.name if self.name else "<UnknownClass>", [base])

    def __str__(self):
        return f"Unknown class.\nName: {self.name}\nReason: {self.reason}"

    def __repr__(self):
        return f"UnknownClass(name={self.name}, reason={self.reason})"

    def add_subclass(self, subclass):
        """
        Add a subclass to the unknown class.
        :param subclass: The subclass to add.
        :type subclass: Class
        """
        subclass.add_superclass(self)


class UnknownClasses(UnknownClass):
    def __init__(self, base, reason=None):
        """
        (Potentially) multiple classes that cannot be evaluated.
        :param base: The base class.
        :type base: Class
        :param reason: The reason for the class being unknown.
        :type reason: str or None
        """
        super().__init__(base, "<UnknownClasses>", reason)

    def __str__(self):
        return f"Unknown classes.\nBase: {self.base}\nReason: {self.reason}"

    def __repr__(self):
        return f"UnknownClass(base={self.base}, reason={self.reason})"

    def add_subclass(self, subclass):
        """
        Add a subclass to the unknown class.
        :param subclass: The subclass to add.
        :type subclass: Class
        """
        subclass.add_superclass(self)
