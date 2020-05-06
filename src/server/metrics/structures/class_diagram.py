from __future__ import annotations

from enum import IntEnum, unique, Enum
from typing import List, Any, Optional

DEFAULT_RETURN_TYPE = "void"


# region Classes

class ClassDiagram:
    """
    Class diagram.
    """

    def __init__(self, classes: Optional[List[Class]] = None,
                 relationships: Optional[List[Relationship]] = None) -> None:
        """
        Class diagram.

        :param classes: The classes to display in the class diagram.
        :param relationships: The relationships between the classes.
        """
        self.classes = classes if classes is not None else []
        self.relationships = relationships if relationships is not None else []

    def __str__(self) -> str:
        return f"Class diagram.\nClasses: {self.classes}\nRelationships: {self.relationships}"

    def __repr__(self) -> str:
        return f"ClassDiagram(classes={self.classes}, relationships={self.relationships})"


class Relationship:
    """
    Relationship.
    """

    def __init__(self, type_: RelationshipType, from_class: Class, to_class: Class,
                 from_multiplicity: Optional[str] = None, to_multiplicity: Optional[str] = None, from_role=None,
                 to_role=None, bidirectional: bool = False) -> None:
        """
        Relationship.

        :param from_role:
        :param to_role:
        :param type_: The type of relationship.
        :param from_class: The class to draw the arrow from.
        :param to_class: The class to draw the arrow to.
        :param from_multiplicity: The multiplicity of the class to draw the arrow from.
        :param to_multiplicity: The multiplicity of the class to draw the arrow to.
        :param bidirectional: Whether or not the relationship is bidirectional.
        """
        self.type = type_
        self.from_class = from_class
        self.to_class = to_class
        self.from_multiplicity = from_multiplicity
        self.to_multiplicity = to_multiplicity
        self.from_role = from_role
        self.to_role = to_role
        self.bidirectional = bidirectional

    def __str__(self) -> str:
        return f"Relationship.\nType: {self.type}\nFrom: {self.from_class}\nTo: {self.to_class}\n" \
               f"From multiplicity: {self.from_multiplicity}\nTo multiplicity: {self.to_multiplicity}\n" \
               f"Bidirectional: {self.bidirectional}"

    def __repr__(self) -> str:
        return f"Relationship(type={self.type}, from_class={self.from_class}, to_class={self.to_class}, " \
               f"from_multiplicity={self.from_multiplicity}, to_multiplicity={self.to_multiplicity}, " \
               f"bidirectional={self.bidirectional})"


class Class:
    """
    Class.
    """

    def __init__(self, name: str, attributes: Optional[List[Attribute]] = None,
                 methods: Optional[List[Method]] = None) -> None:
        """
        Class.

        :param name: The class' name/identifier.
        :param attributes: The class' attributes.
        :param methods: The class' methods.
        """
        self.name = name
        self.attributes = attributes if attributes is not None else []
        self.methods = methods if methods is not None else []

    def __str__(self) -> str:
        return f"Class.\nName: {self.name}\nAttributes: {self.attributes}\nMethods: {self.methods}"

    def __repr__(self) -> str:
        return f"Class(name={self.name}, attributes={self.attributes}, methods={self.methods})"


class Method:
    """
    Method.
    """

    def __init__(self, name: str, visibility: Visibility, parameters: Optional[List[Parameter]] = None,
                 return_type: Optional[str] = None, static: bool = False) -> None:
        """
        Method.

        :param name: The method's name/identifier.
        :param visibility: The method's visibility.
        :param parameters: The method's parameters.
        :param return_type: The method's return type.
        :param static: Whether or not the method is static.
        """
        self.name = name
        self.visibility = visibility
        self.parameters = parameters if parameters is not None else []
        self.return_type = return_type if return_type is not None else DEFAULT_RETURN_TYPE
        self.static = static

    def __str__(self) -> str:
        return f"Method.\nName: {self.name}\nVisibility: {self.visibility}\n" \
               f"Parameters: {self.parameters}\nReturn type: {self.return_type}\nStatic: {self.static}"

    def __repr__(self) -> str:
        return f"Method(name={self.name}, visibility={self.visibility}, " \
               f"parameters={self.parameters}, return_type={self.return_type}, static={self.static})"


class Variable:
    """
    Variable.
    """

    def __init__(self, name: str, type_: Optional[str] = None, default: Optional[str] = None) -> None:
        """
        Variable.

        :param name: The variable's name/identifier.
        :param type_: The variable's type.
        :param default: The default value of the variable.
        """
        self.name = name
        self.type = type_
        self.default = default

    def __str__(self) -> str:
        return f"Variable.\nName: {self.name}\nType: {self.type}\nDefault: {self.default}"

    def __repr__(self) -> str:
        return f"Variable(name={self.name}, type={self.type}, default={self.default})"


class Parameter(Variable):
    """
    Parameter.
    """

    def __init__(self, name: str, type_: Optional[str] = None, default: Any = None) -> None:
        """
        Parameter.

        :param name: The parameter's name/identifier.
        :param type_: The parameter's type.
        :param default: The default value of the parameter.
        """
        super().__init__(name, type_, default)

    def __str__(self) -> str:
        return f"Parameter.\nName: {self.name}\nType: {self.type}\nDefault: {self.default}"

    def __repr__(self) -> str:
        return f"Parameter(name={self.name}, type={self.type}, default={self.default})"


class Attribute(Variable):
    """
    Attribute.
    """

    def __init__(self, name: str, visibility: Visibility, type_: Optional[str] = None, default: Optional[str] = None,
                 static: bool = False) -> None:
        """
        Attribute.

        :param name: The attribute's name/identifier.
        :param visibility: The attribute's visibility.
        :param type_: The attribute's type.
        :param default: The default value of the attribute.
        :param static: Whether or not the attribute is static.
        """
        super().__init__(name, type_, default)
        self.visibility = visibility,
        self.static = static

    def __str__(self) -> str:
        return f"Attribute.\nName: {self.name}\nVisibility: {self.visibility}\nType: {self.type}\n" \
               f"Default: {self.default}\nStatic: {self.static}"

    def __repr__(self) -> str:
        return f"Attribute(name={self.name}, visibility={self.visibility}, type={self.type}, " \
               f"default={self.default}, static={self.static})"


# endregion

# region Enums

class ClassDiagramEnum(Enum):
    """
    Base class for enums.
    """

    pass


@unique
class Visibility(ClassDiagramEnum):
    """
    Visibility.
    """

    PUBLIC = "public"
    PROTECTED = "protected"
    INTERNAL = "internal"
    PRIVATE = "private"

    def __str__(self):
        return f"Visibility.\nName: {self.name}\nValue: {self.value}"

    def __repr__(self):
        return f"Visibility(name={self.name}, value={self.value})"


@unique
class RelationshipType(IntEnum):
    """
    Relationship type.
    """

    ASSOCIATION = "association"
    INHERITANCE = "inheritance"
    IMPLEMENTATION = "implementation"
    DEPENDENCY = "dependency"
    # AGGREGATION = "aggregation    Aggregation and composition relationships are extremely difficult/impossible to
    # COMPOSITION = "composition"   infer from code. Summarised as association relationships.
    NESTING = "nesting"

    def __str__(self):
        return f"Relationship type.\nName: {self.name}\nValue: {self.value}"

    def __repr__(self):
        return f"RelationshipType(name={self.name}, value={self.value})"

# endregion
