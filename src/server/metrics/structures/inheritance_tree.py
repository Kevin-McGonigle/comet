from metrics.structures.base.tree import *


class InheritanceTree(Tree):
    def __init__(self, base=None):
        """
        Inheritance tree.
        :param base: The base class in the tree.
        :type base: Class or None
        """
        super().__init__(base if base is not None else Class("Object"))

    def __str__(self):
        s = "Inheritance Tree"

        if self.base:
            s += "\nBase: {self.base}"

        return s

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
        Inheritance tree node.
        :param name: The name of the class represented by the node.
        :type name: str
        :param superclasses: The classes that the class inherits from.
        :type superclasses: list[Class] or None
        :param methods: The class' methods.
        :type methods: list[Method] or None
        """
        if superclasses is None:
            superclasses = []

        self.methods = methods if methods is not None else []

        super().__init__(name, *superclasses)

    def __str__(self):
        s = self.name

        if self.methods:
            s += f"\nMethods: {self.methods}"

        if self.superclasses:
            s += f"\nSuperclasses: {self.superclasses}"

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
        Setter for the superclasses property.
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
        Add a subclass to this class.
        :param subclass: The subclass to add.
        :type subclass: Class
        """
        subclass.add_superclass(self)

    def add_superclass(self, superclass):
        """
        Add a superclass to this class.
        :param superclass: The superclass to add.
        :type superclass: Class
        """
        self.add_child(superclass)


class Method:
    def __init__(self, name, parameters=None, return_type=None):
        """
        Method.
        :param name: The name of the method.
        :type name: str
        :param parameters: The method's parameters.
        :type parameters: list[Parameter] or None
        :param return_type: The method's return type.
        :type return_type: str or None
        """
        self.name = name
        self.parameters = parameters if parameters is not None else []
        self.return_type = return_type

    def __str__(self):
        s = self.name

        if self.parameters:
            s += f"\nParameters: {self.parameters}"

        if self.return_type:
            s += f"\nReturn Type: {self.return_type}"

        return s

    def __repr__(self):
        return self.name


class Parameter:
    def __init__(self, name, _type=None, default=None):
        """
        Parameter.
        :param name: The name of the parameter
        :type name: str
        :param _type: The parameter's type.
        :type _type: str or None
        :param default: The parameter's default value.
        :type default: str or None
        """
        self.name = name
        self.type = _type
        self.default = default

    def __str__(self):
        s = self.name

        if self.type:
            s += f"\nType: {self.type}"

        if self.default:
            s += f"\nDefault: {self.default}"

        return s

    def __repr__(self):
        return self.name
