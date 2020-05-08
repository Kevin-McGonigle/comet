from __future__ import annotations

from enum import IntEnum, unique, Enum
from typing import List, Any, Optional

DEFAULT_RETURN_TYPE = "void"


# region Classes

class ClassDiagram:
    """
    Class diagram.
    """

    def __init__(self, classes: Optional[List[Class]] = None) -> None:
        """
        Class diagram.

        :param classes: The classes to display in the class diagram.
        """
        self.classes = classes if classes is not None else []

    def __str__(self) -> str:
        return f"Class diagram.\nClasses: {self.classes}"

    def __repr__(self) -> str:
        return f"ClassDiagram(classes={self.classes})"


class Relationship:
    """
    Relationship.
    """

    def __init__(self, type_: RelationshipType, relation: Class, multiplicity: Optional[str] = None,
                 relation_multiplicity: Optional[str] = None, role=None, relation_role=None,
                 bidirectional: bool = False) -> None:
        """
        Relationship.

        :param type_: The type of relationship.
        :param relation: The class to draw the arrow to.
        :param multiplicity: The multiplicity of the class.
        :param relation_multiplicity: The multiplicity of the related class.
        :param role: The role of the class.
        :param relation_role: The role of the related class.
        :param bidirectional: Whether or not the relationship is bidirectional.
        """
        self.type = type_
        self.relation = relation
        self.multiplicity = multiplicity
        self.relation_multiplicity = relation_multiplicity
        self.role = role
        self.relation_role = relation_role
        self.bidirectional = bidirectional

    def __str__(self) -> str:
        return f"Relationship.\nType: {self.type}\nRelation: {self.relation}\nMultiplicity: {self.multiplicity}\n" \
               f"Relation multiplicity: {self.relation_multiplicity}\nRole: {self.role}\n" \
               f"Relation role: {self.relation_role}\nBidirectional: {self.bidirectional}"

    def __repr__(self) -> str:
        return f"Relationship(type={self.type}, relation={self.relation}, multiplicity={self.multiplicity}, " \
               f"relation_multiplicity={self.relation_multiplicity}, role={self.role}, " \
               f"relation_role={self.relation_role}, bidirectional={self.bidirectional})"


class Class:
    """
    Class.
    """

    def __init__(self, name: str, attributes: Optional[List[Attribute]] = None, methods: Optional[List[Method]] = None,
                 superclasses: Optional[List[str]] = None, interfaces: Optional[List[str]] = None,
                 nested_classes: Optional[List[str]] = None, relationships: Optional[List[Relationship]] = None):
        """
        Class.

        :param name: The class' name/identifier.
        :param attributes: The class' attributes.
        :param methods: The class' methods.
        :param superclasses: The classes that the class inherits from.
        :param interfaces: The interfaces that the class implements.
        :param nested_classes: The classes defined within the class.
        :param relationships: The class' relationships to other classes.
        """
        self.name = name
        self.attributes = attributes if attributes is not None else []
        self.methods = methods if methods is not None else []
        self.superclasses = superclasses if superclasses is not None else []
        self.interfaces = interfaces if interfaces is not None else []
        self.nested_classes = nested_classes if nested_classes is not None else []
        self.relationships = relationships if relationships is not None else []

    def __str__(self) -> str:
        return f"Class.\nName: {self.name}\nAttributes: {self.attributes}\nMethods: {self.methods}\n" \
               f"Superclasses: {self.superclasses}\nInterfaces: {self.interfaces}\n" \
               f"Nested classes: {self.nested_classes}\nRelationships: {self.relationships}"

    def __repr__(self) -> str:
        return f"Class(name={self.name}, attributes={self.attributes}, methods={self.methods}, " \
               f"superclasses={self.superclasses}, interfaces={self.interfaces}, " \
               f"nested_classes={self.nested_classes}, relationships={self.relationships})"


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
