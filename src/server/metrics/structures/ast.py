from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Optional, Sequence, Union, Dict, Any

from metrics.structures.base.graph import Node, Graph

if TYPE_CHECKING:
    from metrics.visitors.base.ast_visitor import ASTVisitor


class AST(Graph):
    """
    Abstract syntax tree.

    A tree structure that represents a program in a language-independent
    tree-like manner.
    """

    def __init__(self, root: Optional[ASTNode] = None):
        """
        Abstract syntax tree.

        :param root: The root node of the AST.
        """
        super().__init__(root)

    def __str__(self):
        return f"Abstract syntax tree.\nRoot: {self.root}"

    def __repr__(self):
        return f"AST(root={self.root}"

    def accept(self, visitor: "ASTVisitor"):
        """
        Accept an AST visitor.

        :param visitor: The AST visitor to accept.
        :return: The result of the accept.
        """
        return super().accept(visitor)


class ASTNode(Node):
    """
    Node.

    Generic abstract syntax tree node.
    """

    def __init__(self, children: Optional[Dict[Any, ASTNode]] = None):
        """
        Node.

        :param children: The child nodes of the node.
        """
        super().__init__()
        self.children: Dict[Any, ASTNode] = children if children is not None else {}

    def __str__(self):
        return f"Generic abstract syntax tree node.\nChildren: {self.children}"

    def __repr__(self):
        return f"ASTNode(children={self.children})"

    def __getitem__(self, item):
        return self.children[item]

    def __setitem__(self, key, value: ASTNode):
        self.children[key] = value

    def __contains__(self, item):
        return item in self.children

    def values(self):
        return list(self.children.values())

    def accept(self, visitor: "ASTVisitor"):
        """
        Accept an AST visitor.

        :param visitor: The AST visitor to accept.
        :return: The result of the accept.
        """
        return super().accept(visitor)


# region Terminals

class ASTIdentifierNode(ASTNode):
    """
    Identifier.

    The identifier (name) of a variable, function, class, etc.
    """

    def __init__(self, name: str):
        """
        Identifier.

        :param name: The name of the identifier.
        """
        self.name = name
        super().__init__()

    def __str__(self):
        return f"Identifier.\nName: {self.name}"

    def __repr__(self):
        return f"ASTIdentifierNode(name={self.name})"

    def accept(self, visitor):
        """
        Accept an AST visitor and call its visit_identifier method.

        :param visitor: The AST visitor to accept.
        :return: The result of the accept.
        """
        return visitor.visit_identifier(self)


class ASTLiteralNode(ASTNode):
    """
    Literal.

    A literal value (e.g. integer, string, float, etc.)
    """

    def __init__(self, type_: ASTLiteralType, value: Optional[str] = None):
        """
        Literal.

        :param type_: The type of literal.
        :param value: The value of the literal.
        """
        self.type = type_
        self.value = value
        super().__init__()

    def __str__(self):
        return f"Literal.\nType: {self.type}\nValue: {self.value}"

    def __repr__(self):
        return f"ASTLiteralNode(type={self.type}, value={self.value})"

    def accept(self, visitor):
        """
        Accept an AST visitor and call its visit_literal method.

        :param visitor: The AST visitor to accept.
        :return: The result of the accept.
        """
        return visitor.visit_literal(self)


# endregion

# region Multiples

class ASTMultiplesNode(ASTNode):
    """
    Multiples.

    Base class for representing a series of multiple, consecutive nodes.
    """

    def __init__(self, children: Sequence[ASTNode]):
        """
        Multiples.

        :param children: The sequence of multiple nodes being represented.
        """
        if children is None:
            children = []
        super().__init__(dict(enumerate(children)))

    def __str__(self):
        return f"Multiple, consecutive nodes (generic).\nChildren: {list(self.children.values())}"

    def __repr__(self):
        return f"ASTMultiplesNode(children={self.children})"

    def add_child(self, child: "ASTNode"):
        if isinstance(child, Node) and child not in self.children.values():
            key = 0
            for k in self.children.keys():
                if k >= key:
                    key = k + 1
            self.children[key] = child
        elif not isinstance(child, Node):
            raise TypeError(f"Node.add_child(child): child is not Node (child={child}, type={type(child)}).")
        else:
            raise ValueError(f"Node.add_child(child): supplied child is already a child of the parent node.")

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_multiples method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_multiples(self)


class ASTStatementsNode(ASTMultiplesNode):
    """
    Statements.

    Representation of multiple, consecutive statements.
    """

    def __init__(self, statements: Sequence[ASTNode]):
        """
        Statements.

        :param statements: The statements (in order) to be represented.
        """
        super().__init__(statements)

    def __str__(self):
        return f"Multiple, consecutive statements.\nChildren: {list(self.children.values())}"

    def __repr__(self):
        return f"ASTStatementsNode(children={self.children})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_statements method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_statements(self)


class ASTExpressionsNode(ASTMultiplesNode):
    """
    Expressions.

    Representation of multiple, consecutive expressions.
    """

    def __init__(self, expressions: Sequence[ASTNode]):
        """
        Expressions.

        :param expressions: The expressions (in order) to be represented.
        """
        super().__init__(expressions)

    def __str__(self):
        return f"Multiple, consecutive expressions.\nChildren: {list(self.children.values())}"

    def __repr__(self):
        return f"ASTExpressionsNode(children={self.children})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_expressions method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_expressions(self)


class ASTVariablesNode(ASTMultiplesNode):
    """
    Variables.

    Representation of multiple, consecutive variables.
    """

    def __init__(self, variables: Sequence[ASTNode]):
        """
        Variables.

        :param variables: The variables (in order) to be represented.
        """
        super().__init__(variables)

    def __str__(self):
        return f"Multiple, consecutive variables.\nChildren: {list(self.children.values())}"

    def __repr__(self):
        return f"ASTVariablesNode(children={self.children})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_variables method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_variables(self)


class ASTElementsNode(ASTMultiplesNode):
    """
    Elements.

    Representation of multiple, consecutive list, map or set elements.
    """

    def __init__(self, elements: Sequence[ASTNode]):
        """
        Elements.

        :param elements: The elements (in order) to be represented.
        """
        super().__init__(elements)

    def __str__(self):
        return f"Multiple, consecutive list, map or set elements.\nChildren: {list(self.children.values())}"

    def __repr__(self):
        return f"ASTElementsNode(children={self.children})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_elements method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_elements(self)


class ASTParametersNode(ASTMultiplesNode):
    """
    Parameters.

    Representation of multiple, consecutive parameters.
    """

    def __init__(self, parameters: Sequence[ASTNode]):
        """
        Parameters.

        :param parameters: The parameters (in order) to be represented.
        """
        super().__init__(parameters)

    def __str__(self):
        return f"Multiple, consecutive parameters.\nChildren: {list(self.children.values())}"

    def __repr__(self):
        return f"ASTParametersNode(children={self.children})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_parameters method.

        :param: visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_parameters(self)


class ASTArgumentsNode(ASTMultiplesNode):
    """
    Arguments.

    Representation of multiple, consecutive arguments.
    """

    def __init__(self, arguments: Sequence[ASTNode]):
        """
        Arguments.

        :param arguments: The arguments (in order) to be represented.
        """
        super().__init__(arguments)

    def __str__(self):
        return f"Multiple, consecutive arguments.\nChildren: {list(self.children.values())}"

    def __repr__(self):
        return f"ASTArgumentsNode(children={self.children})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_arguments method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_arguments(self)


class ASTSubscriptsNode(ASTMultiplesNode):
    """
    Subscripts.

    Representation of multiple, consecutive subscripts.
    """

    def __init__(self, subscripts: Sequence[ASTNode]):
        """
        Subscripts.

        :param subscripts: The subscripts (in order) to be represented.
        """
        super().__init__(subscripts)

    def __str__(self):
        return f"Multiple, consecutive subscripts.\nChildren: {list(self.children.values())}"

    def __repr__(self):
        return f"ASTSubscriptsNode(children={self.children})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_subscripts method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_subscripts(self)


class ASTCatchesNode(ASTMultiplesNode):
    """
    Catches.

    Representation of multiple, consecutive catch statements.
    """

    def __init__(self, catches: Sequence[ASTNode]):
        """
        Catches.

        :param catches: The catches (in order) to be represented.
        """
        super().__init__(catches)

    def __str__(self):
        return f"Multiple, consecutive catches.\nChildren: {list(self.children.values())}"

    def __repr__(self):
        return f"ASTCatchesNode(children={self.children})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_catches method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_catches(self)


class ASTDecoratorsNode(ASTMultiplesNode):
    """
    Decorators.

    Representation of multiple, consecutive decorators.
    """

    def __init__(self, decorators: Sequence[ASTNode]):
        """
        Decorators.

        :param decorators: The decorators (in order) to be represented.
        """
        super().__init__(decorators)

    def __str__(self):
        return f"Multiple, consecutive decorators.\nChildren: {list(self.children.values())}"

    def __repr__(self):
        return f"ASTDecoratorsNode(children={self.children})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_decorators method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_decorators(self)


class ASTSwitchSectionsNode(ASTMultiplesNode):
    """
    Switch sections.

    Representation of multiple, consecutive switch sections.
    """

    def __init__(self, switch_sections: Sequence[ASTNode]):
        """
        Switch sections.

        :param switch_sections: The switch sections (in order) to be represented.
        """
        super().__init__(switch_sections)

    def __str__(self):
        return f"Multiple, consecutive switch sections.\nChildren: {list(self.children.values())}"

    def __repr__(self):
        return f"ASTSwitchSectionsNode(children={self.children})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_switch_sections method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_switch_sections(self)


class ASTSwitchLabelsNode(ASTMultiplesNode):
    """
        Switch labels.

        Representation of multiple, consecutive switch labels.
        """

    def __init__(self, switch_labels: Sequence[ASTNode]):
        """
        Switch labels.

        :param switch_labels: The switch labels (in order) to be represented.
        """
        super().__init__(switch_labels)

    def __str__(self):
        return f"Multiple, consecutive switch labels.\nChildren: {list(self.children.values())}"

    def __repr__(self):
        return f"ASTSwitchLabelsNode(children={self.children})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_switch_labels method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_switch_labels(self)


class ASTVariableDeclarationsNode(ASTMultiplesNode):
    """
    Variable declarations.

    Representation of multiple, consecutive variable declarations.
    """

    def __init__(self, variable_declarations: Sequence[ASTNode]):
        """
        Variable declarations.

        :param variable_declarations: The variable declarations (in order) to be represented.
        """
        super().__init__(variable_declarations)

    def __str__(self):
        return f"Multiple, consecutive variable declarations.\nChildren: {list(self.children.values())}"

    def __repr__(self):
        return f"ASTVariableDeclarationsNode(children={self.children})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_variable_declarations method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_variable_declarations(self)


class ASTConstantDeclarationsNode(ASTMultiplesNode):
    """
    Constant declarations.

    Representation of multiple, consecutive constant declarations.
    """

    def __init__(self, constant_declarations: Sequence[ASTNode]):
        """
        Constant declarations.

        :param constant_declarations: The constant declarations (in order) to be represented.
        """
        super().__init__(constant_declarations)

    def __str__(self):
        return f"Multiple, consecutive constant declarations.\nChildren: {list(self.children.values())}"

    def __repr__(self):
        return f"ASTConstantDeclarationsNode(children={self.children})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_constant_declarations method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_constant_declarations(self)


class ASTAttributesNode(ASTMultiplesNode):
    """
    Attributes.

    Representation of multiple, consecutive attributes.
    """

    def __init__(self, attributes: Sequence[ASTNode]):
        """
        Attributes.

        :param attributes: The attributes (in order) to be represented.
        """
        super().__init__(attributes)

    def __str__(self):
        return f"Multiple, consecutive attributes.\nChildren: {list(self.children.values())}"

    def __repr__(self):
        return f"ASTAttributesNode(children={self.children})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_attributes method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_attributes(self)


class ASTAttributeSectionsNode(ASTMultiplesNode):
    """
    Attribute sections.

    Representation of multiple, consecutive attribute sections.
    """

    def __init__(self, attribute_sections: Sequence[ASTNode]):
        """
        Attribute sections.

        :param attribute_sections: The attribute sections (in order) to be represented.
        """
        super().__init__(attribute_sections)

    def __str__(self):
        return f"Multiple, consecutive attribute sections.\nChildren: {list(self.children.values())}"

    def __repr__(self):
        return f"ASTAttributeSectionsNode(children={self.children})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_attribute_sections method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_attribute_sections(self)


class ASTConstraintsClausesNode(ASTMultiplesNode):
    """
    Constraints clauses.

    Representation of multiple, consecutive constraints clauses.
    """

    def __init__(self, constraints_clauses: Sequence[ASTNode]):
        """
        Constraints.

        :param constraints_clauses: The constraints clauses (in order) to be represented.
        """
        super().__init__(constraints_clauses)

    def __str__(self):
        return f"Multiple, consecutive constraints clauses.\nChildren: {list(self.children.values())}"

    def __repr__(self):
        return f"ASTConstraintsClausesNode(children={self.children})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_constraints_clauses method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_constraints_clauses(self)


class ASTConstraintsNode(ASTMultiplesNode):
    """
    Constraints.

    Representation of multiple, consecutive constraints.
    """

    def __init__(self, constraints: Sequence[ASTNode]):
        """
        Constraints.

        :param constraints: The constraints (in order) to be represented.
        """
        super().__init__(constraints)

    def __str__(self):
        return f"Multiple, consecutive constraints.\nChildren: {list(self.children.values())}"

    def __repr__(self):
        return f"ASTConstraintsNode(children={self.children})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_constraints method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_constraints(self)


# endregion

# region Statements

class ASTStatementNode(ASTNode):
    """
    Statement.

    Base class for representing a statement.
    """

    def __init__(self, children: Optional[Dict[Any, ASTNode]] = None):
        """
        Statement.

        :param children: The child nodes of the statement node.
        """
        super().__init__(children)

    def __str__(self):
        return f"Generic statement.\nChildren: {list(self.children.values())}"

    def __repr__(self):
        return f"ASTStatementNode(children={self.children})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_statement method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_statement(self)


class ASTDelStatementNode(ASTStatementNode):
    """
    Delete statement.
    """

    def __init__(self, target: ASTNode):
        """
        Delete statement.

        :param target: Expression(s) determining what is to be deleted.
        """
        super().__init__({"target": target})

    def __str__(self):
        return f"Delete statement.\nTarget: {self['target']}"

    def __repr__(self):
        return f"ASTDelStatementNode(target={self['target']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_del_statement method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_del_statement(self)


class ASTAssignmentStatementNode(ASTStatementNode):
    """
    Assignment statement.

    Standard variable assignment statement.
    """

    def __init__(self, variables: ASTNode, values: ASTNode):
        """
        Assignment statement.

        :param variables: The variable(s) to be assigned to.
        :param values: The value(s) to assign.
        """
        super().__init__({"variables": variables, "values": values})

    def __str__(self):
        return f"Standard variable assignment statement.\nVariable(s): {self['variables']}\nValue(s): {self['values']}"

    def __repr__(self):
        return f"ASTAssignmentStatementNode(variables={self['variables']}, values={self['values']}"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_assignment_statement method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_assignment_statement(self)


class ASTAugmentedAssignmentStatementNode(ASTStatementNode):
    """
    Augmented assignment statement.

    Augmented (in-place) assignment statement.
    """

    def __init__(self, operation: ASTInPlaceOperation, variables: ASTNode, values: ASTNode):
        """
        Augmented assignment statement.

        :param operation: The in-place operation being performed.
        :param variables: The variable(s) being assigned to.
        :param values: The value(s) being assigned.
        """
        self.operation = operation
        super().__init__({"variables": variables, "values": values})

    def __str__(self):
        return f"Augmented assignment statement.\nOperation: {self.operation}\nVariables: {self['variables']}" \
               f"\nValues: {self['values']}"

    def __repr__(self):
        return f"ASTAugmentedAssignmentStatementNode(operation={self.operation}, variables={self['variables']}, " \
               f"values={self['values']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_augmented_assignment_statement method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_augmented_assignment_statement(self)


class ASTAnnotatedAssignmentStatementNode(ASTStatementNode):
    """
    Annotated assignment statement.

    Python variable assignment with type hint annotation.
    """

    def __init__(self, annotation: ASTNode, variables: ASTNode, values: Optional[ASTNode] = None):
        """
        Annotated assignment statement.

        :param annotation: The annotation for the variable(s).
        :param variables: The variable(s) being assigned to.
        :param values: The value(s) being assigned.
        """
        super().__init__({"variables": variables, "annotation": annotation, "values": values})

    def __str__(self):
        return f"Annotated assignment statement.\nAnnotation: {self['annotation']}\nVariables: {self['variables']}" \
               f"\nValues: {self['values']}"

    def __repr__(self):
        return f"ASTAnnotatedAssignmentStatementNode(annotation={self['annotation']}, variables={self['variables']}, " \
               f"values={self['values']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_annotated_assignment_statement method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_annotated_assignment_statement(self)


class ASTYieldStatementNode(ASTStatementNode):
    """
    Yield statement.
    """

    def __init__(self, values: Optional[ASTNode] = None):
        """
        Yield statement.

        :param values: The value(s) being yielded.
        """
        super().__init__({"values": values})

    def __str__(self):
        return f"Yield statement.\nValues: {self['values']}"

    def __repr__(self):
        return f"ASTYieldStatementNode(values={self['values']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_yield_statement method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_yield_statement(self)


class ASTPassStatementNode(ASTStatementNode):
    """
    Pass statement.
    """

    def __init__(self):
        """
        Pass statement.
        """
        super().__init__()

    def __str__(self):
        return "Pass statement."

    def __repr__(self):
        return "ASTPassStatementNode()"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_pass_statement method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_pass_statement(self)


class ASTBreakStatementNode(ASTStatementNode):
    """
    Break statement.
    """

    def __init__(self):
        """
        Break statement.
        """
        super().__init__()

    def __str__(self):
        return "Break statement."

    def __repr__(self):
        return "ASTBreakStatementNode()"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_break_statement method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_break_statement(self)


class ASTContinueStatementNode(ASTStatementNode):
    """
    Continue statement.
    """

    def __init__(self):
        """
        Continue statement.
        """
        super().__init__()

    def __str__(self):
        return "Continue statement."

    def __repr__(self):
        return "ASTContinueStatementNode()"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_continue_statement method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_continue_statement(self)


class ASTReturnStatementNode(ASTStatementNode):
    """
    Return statement.
    """

    def __init__(self, values: Optional[ASTNode] = None):
        """
        Return statement.

        :param values: The value(s) being returned.
        """
        super().__init__({"values": values})

    def __str__(self):
        return f"Return statement.\nValues: {self['values']}"

    def __repr__(self):
        return f"ASTReturnStatementNode(values={self['values']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_return_statement method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_return_statement(self)


class ASTThrowStatementNode(ASTStatementNode):
    """
    Throw statement.
    """

    def __init__(self, exception: Optional[ASTNode] = None):
        """
        Throw statement.

        :param exception: The exception to be thrown.
        """
        super().__init__({"exception": exception})

    def __str__(self):
        return f"Throw statement.\nException: {self['exception']}"

    def __repr__(self):
        return f"ASTThrowStatementNode(exception={self['exception']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_throw_statement method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_throw_statement(self)


class ASTImportStatementNode(ASTStatementNode):
    """
    Import statement.
    """

    def __init__(self, libraries: ASTNode, modifiers: Optional[Sequence[ASTModifier]] = None):
        """
        Import statement.

        :param libraries: The libraries to be imported.
        """
        self.modifiers = modifiers
        super().__init__({"libraries": libraries})

    def __str__(self):
        return f"Import statement.\nLibraries: {self['libraries']}\nModifiers: {self.modifiers}"

    def __repr__(self):
        return f"ASTImportStatementNode(libraries={self['libraries']}, modifiers={self.modifiers})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_import_statement method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_import_statement(self)


class ASTGlobalStatementNode(ASTStatementNode):
    """
    Global statement.

    Global variable(s) declaration.
    """

    def __init__(self, variables: ASTNode):
        """
        Global statement.

        :param variables: The global variable(s) being declared.
        """
        super().__init__({"variables": variables})

    def __str__(self):
        return f"Global variable(s) declaration.\nVariables: {self['variables']}"

    def __repr__(self):
        return f"ASTGlobalStatementNode(variables={self['variables']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_global_statement method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_global_statement(self)


class ASTNonLocalStatementNode(ASTStatementNode):
    """
    Non-local statement.

    Non-local variable(s) declaration.
    """

    def __init__(self, variables: ASTNode):
        """
        Non-local statement.

        :param variables: The nonlocal variable(s) being declared.
        """
        super().__init__({"variables": variables})

    def __str__(self):
        return f"Non-local variable(s) declaration.\nVariables: {self['variables']}"

    def __repr__(self):
        return f"ASTNonLocalStatementNode(variable={self['variables']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_non_local_statement method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_non_local_statement(self)


class ASTAssertStatementNode(ASTStatementNode):
    """
    Assert statement.
    """

    def __init__(self, condition: ASTNode, message: Optional[ASTNode] = None):
        """
        Assert statement.

        :param condition: The condition to assert.
        :param message: The message for the error raised should the assertion fail.
        """
        super().__init__({"condition": condition, "message": message})

    def __str__(self):
        return f"Assert statement.\nCondition: {self['condition']}\nMessage: {self['message']}"

    def __repr__(self):
        return f"ASTAssertStatementNode(condition={self['condition']}, message={self['message']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_assert_statement method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_assert_statement(self)


class ASTIfStatementNode(ASTStatementNode):
    """
    If statement.
    """

    def __init__(self, condition: ASTNode, body: Optional[ASTNode] = None, else_body: Optional[ASTNode] = None):
        """
        If statement.

        :param condition: The condition to check.
        :param body: The code to execute if the condition is met.
        :param else_body: The code to execute if the condition is not met.
        """
        super().__init__({"condition": condition, "body": body, "else_body": else_body})

    def __str__(self):
        return f"If statement.\nCondition: {self['condition']}\nBody: {self['body']}, Else body: {self['else_body']}"

    def __repr__(self):
        return f"ASTIfStatementNode(condition={self['condition']}, body={self['body']}, else_body={self['else_body']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_if_statement method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_if_statement(self)


class ASTLoopStatementNode(ASTStatementNode):
    """
    Loop statement.
    """

    def __init__(self, condition: ASTNode, body: Optional[ASTNode] = None, else_body: Optional[ASTNode] = None):
        """
        Loop statement.

        :param condition: The condition to check.
        :param body: The code to execute while the condition is met.
        :param else_body: The code to execute when the condition is not met.
        """
        super().__init__({"condition": condition, "body": body, "else_body": else_body})

    def __str__(self):
        return f"Loop statement.\nCondition: {self['condition']}\nBody: {self['body']}\nElse body: {self['else_body']}"

    def __repr__(self):
        return f"ASTLoopStatementNode(condition={self['condition']}, body={self['body']}, " \
               f"else_body={self['else_body']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_loop_statement method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_loop_statement(self)


class ASTTryStatementNode(ASTStatementNode):
    """
    Try statement.
    """

    def __init__(self, body, catches: Optional[ASTNode] = None, else_body: Optional[ASTNode] = None,
                 finally_: Optional[ASTNode] = None):
        """
        Try statement.

        :param body: The code to try.
        :param catches: The catch clause(s).
        :param else_body: The code to execute if the control flow leaves the try block, no exception was raised, and no
        return, continue, or break statement was executed.
        :param finally_: The finally clause.
        """
        super().__init__({"body": body, "catches": catches, "else_body": else_body, "finally": finally_})

    def __str__(self):
        return f"Try statement.\nBody: {self['body']}\nCatches: {self['catches']}\nElse body: {self['else_body']}" \
               f"\nFinally: {self['finally']}"

    def __repr__(self):
        return f"ASTTryStatementNode(body={self['body']}, catches={self['catches']}, else_body={self['else_body']}, " \
               f"finally={self['finally']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_try_statement method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_try_statement(self)


class ASTWithStatementNode(ASTStatementNode):
    """
    With statement.
    """

    def __init__(self, expressions: ASTNode, body: ASTNode):
        """
        With statement.

        :param expressions: The expression(s) to evaluate to create a context manager.
        :param body: The code to execute within the established runtime context.
        """
        super().__init__({"expressions": expressions, "body": body})

    def __str__(self):
        return f"With statement.\nExpressions: {self['expressions']}\nBody: {self['body']}"

    def __repr__(self):
        return f"ASTWithStatementNode(expressions={self['expressions']}, body={self['body']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_with_statement method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_with_statement(self)


class ASTNamespaceDeclarationNode(ASTStatementNode):
    """
    Namespace declaration.
    """

    def __init__(self, name: ASTNode, body: Optional[ASTNode] = None):
        """
        Namespace declaration.
        
        :param name: The name of the namespace.
        :param body: The body of the namespace.
        """
        super().__init__({"name": name, "body": body})

    def __str__(self):
        return f"Namespace declaration.\nName: {self['name']}\nBody: {self['body']}"

    def __repr__(self):
        return f"ASTNamespaceDeclarationNode(name={self['name']}, body={self['body']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_namespace_declaration method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_namespace_declaration(self)


class ASTSwitchStatementNode(ASTStatementNode):
    """
    Switch statement.
    """

    def __init__(self, match_expression: ASTNode, sections: Optional[ASTNode] = None):
        """
        Switch statement.

        :param match_expression: The expression to match against the case label patterns.
        :param sections: The switch sections contained within the switch statement.
        """
        super().__init__({"match_expression": match_expression, "sections": sections})

    def __str__(self):
        return f"Switch statement.\nMatch expression: {self['match_expression']}\nSections: {self['sections']}"

    def __repr__(self):
        return f"ASTSwitchStatementNode(match_expression={self['match_expression']}, sections={self['sections']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_switch_statement method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_switch_statement(self)


class ASTJumpStatementNode(ASTStatementNode):
    """
    Jump.
    """

    def __init__(self, target: ASTNode):
        """
        Jump.
        
        :param target: The target of the jump.
        """
        super().__init__({"target": target})

    def __str__(self):
        return f"Jump.\nTarget: {self['target']}"

    def __repr__(self):
        return f"ASTJumpStatementNode(target={self['target']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_jump_statement method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_jump_statement(self)


class ASTLockStatementNode(ASTStatementNode):
    """
    Lock.
    """

    def __init__(self, lock_object: ASTNode, body: Optional[ASTNode] = None):
        """
        Lock.

        :param lock_object: The object to acquire a lock on.
        :param body: The code to be executed with the lock acquired.
        """
        super().__init__({"lock_object": lock_object, "body": body})

    def __str__(self):
        return f"Lock.\nLock object: {self['lock_object']}\nBody: {self['body']}"

    def __repr__(self):
        return f"ASTLockStatementNode(lock_object={self['lock_object']}, body={self['body']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_lock_statement method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_lock_statement(self)


class ASTExternAliasDirectiveNode(ASTStatementNode):
    """
    Extern alias directive.
    """

    def __init__(self, alias: ASTNode):
        """
        Extern alias directive.

        :param alias: The alias being referenced.
        """
        super().__init__({"alias": alias})

    def __str__(self):
        return f"Extern alias directive.\nAlias: {self['alias']}"

    def __repr__(self):
        return f"ASTExternAliasDirectiveNode(alias={self['alias']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_extern_alias_directive method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_extern_alias_directive(self)


class ASTVariableDeclarationNode(ASTStatementNode):
    """
    Variable declaration.
    """

    def __init__(self, name: ASTNode, type_: Optional[ASTNode] = None, initial_value: Optional[ASTNode] = None,
                 attributes: Optional[ASTNode] = None, modifiers: Optional[Sequence[ASTModifier]] = None):
        """
        Variable declaration.
        :param name: The variable being declared.
        :param type_: The type of the variable being declared.
        :param initial_value: The initial value assigned to the variable.
        :param attributes: The attribute(s) applied to the variable.
        :param modifiers: The modifier(s) applied to the variable.
        """
        self.modifiers = modifiers if modifiers is not None else []
        super().__init__({"name": name, "type": type_, "initial_value": initial_value, "attributes": attributes})

    def __str__(self):
        return f"Variable declaration.\nName: {self['name']}\nType: {self['type']}\n" \
               f"Initial value: {self['initial_value']}\nAttributes: {self['attributes']}\n" \
               f"Modifiers: {self.modifiers}"

    def __repr__(self):
        return f"ASTVariableDeclaration(name={self['name']}, type={self['type']}, " \
               f"initial_value={self['initial_value']}, attributes={self['attributes']}, " \
               f"modifiers={self.modifiers})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_variable_declaration method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_variable_declaration(self)


class ASTConstantDeclarationNode(ASTStatementNode):
    """
    Constant declaration.
    """

    def __init__(self, name: ASTNode, type_: ASTNode, initial_value: ASTNode,
                 modifiers: Optional[Sequence[ASTModifier]] = None):
        """
        Constant declaration.
        :param name: The constant being declared.
        :param type_: The type of the constant being declared.
        :param initial_value: The initial value assigned to the constant.
        :param modifiers: The modifier applied to the constant.
        """
        super().__init__({"name": name, "type": type_, "initial_value": initial_value})
        self.modifiers = modifiers if modifiers is not None else []

    def __str__(self):
        return f"Constant declaration.\nName: {self['name']}\nType: {self['type']}\n" \
               f"Initial value: {self['initial_value']}\nModifiers: {self.modifiers}"

    def __repr__(self):
        return f"ASTConstantDeclaration(name={self['name']}, type={self['type']}, " \
               f"initial_value={self['initial_value']}, modifiers={self.modifiers})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_constant_declaration method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_constant_declaration(self)


# region Definitions

class ASTDefinitionNode(ASTStatementNode):
    """
    Definition.

    Base class for different kinds of definitions.
    """

    def __init__(self, name: ASTNode, attributes: Optional[ASTNode] = None,
                 modifiers: Optional[Sequence[ASTModifier]] = None, children: Optional[Dict[Any, ASTNode]] = None):
        """
        Definition.

        :param name: The name of the definition.
        :param attributes: The attribute(s) being applied to the definition.
        :param modifiers: The modifier(s) being applied to the definition.
        :param children: The child nodes of the definition node.
        """
        super().__init__({"name": name, "attributes": attributes, **(children if children is not None else {})})
        self.modifiers = modifiers if modifiers is not None else []

    def __str__(self):
        return f"Definition.\nName: {self['name']}\nAttributes: {self['attributes']}\nModifiers: {self.modifiers}\n" \
               f"Children: {list(self.children.values())}"

    def __repr__(self):
        return f"ASTDefinitionNode(name={self['name']}, attributes={self['attributes']}, modifiers={self.modifiers}, " \
               f"children={self.children})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_definition method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """

        return visitor.visit_definition(self)


class ASTClassDefinitionNode(ASTDefinitionNode):
    """
    Class definition.
    """

    def __init__(self, name, body: Optional[ASTNode] = None, bases: Optional[ASTNode] = None,
                 constraints_clauses: Optional[ASTNode] = None, attributes=None, modifiers=None):
        """
        Class definition.

        :param name: The name of the class.
        :param body: The body of the class.
        :param bases: The base class(es) that the class inherits from and/or the interfaces that it implements.
        :param constraints_clauses: The constraints clause(s) being applied to the class' type parameters.
        :param attributes: The attribute(s) being applied to the class.
        :param modifiers: The modifier(s) being applied to the class.
        """
        super().__init__(name, attributes, modifiers,
                         {"body": body, "bases": bases, "constraints_clauses": constraints_clauses})

    def __str__(self):
        return f"Class definition.\nName: {self['name']}\nBody: {self['body']}\nBases: {self['bases']}\n" \
               f"Constraints clauses: {self['constraints_clauses']}\nAttributes: {self['attributes']}\n" \
               f"Modifiers: {self.modifiers}"

    def __repr__(self):
        return f"ASTClassDefinitionNode(name={self['name']}, body={self['body']}, bases={self['bases']}, " \
               f"constraints_clauses={self['constraints_clauses']}, attributes={self['attributes']}" \
               f"modifiers={self.modifiers})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_class_definition method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_class_definition(self)


class ASTFunctionDefinitionNode(ASTDefinitionNode):
    """
    Function definition.
    """

    def __init__(self, name, return_type: Optional[ASTNode] = None, parameters: Optional[ASTNode] = None,
                 constraints_clauses=None, body: Optional[ASTNode] = None, attributes=None, modifiers=None):
        """
        Function definition.

        :param name: The name of the function.
        :param return_type: The return type of the function.
        :param parameters: The parameter(s) of the function.
        :param constraints_clauses: The constraint(s) applied to the function's type parameters.
        :param body: The body of the function.
        :param attributes: The attribute(s) applied to the function.
        :param modifiers: The modifier(s) applied to the function.
        """
        super().__init__(name, attributes, modifiers, {"return_type": return_type, "parameters": parameters,
                                                       "constraints_clauses": constraints_clauses, "body": body})

    def __str__(self):
        return f"Function definition.\nName: {self['name']}\nParameters: {self['parameters']}\n" \
               f"Return type: {self['return_type']}\nBody: {self['body']}\nAttributes: {self['attributes']}\n" \
               f"Modifiers: {self.modifiers}"

    def __repr__(self):
        return f"ASTFunctionDefinitionNode(name={self['name']}, parameters={self['parameters']}, " \
               f"return_type={self['return_type']}, body={self['body']}, attributes={self['attributes']}, " \
               f"modifiers={self.modifiers})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_function_definition method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_function_definition(self)


class ASTEventDefinitionNode(ASTDefinitionNode):
    """
    Event definition.
    """

    def __init__(self, name, type_: ASTNode, body: Optional[ASTNode] = None, attributes=None, modifiers=None):
        """
        Event definition.
        :param name: The name of the event.
        :param type_: The type of delegates allowed to be invoked by the event.
        :param body: The body of the event.
        :param attributes: The attribute(s) being applied to the event.
        :param modifiers: The modifier(s) being applied to the event.
        """
        super().__init__(name, attributes, modifiers, {"type": type_, "body": body})

    def __str__(self):
        return f"Event definition.\nName: {self['name']}\nType: {self['type']}\nBody: {self['body']}\n" \
               f"Attributes: {self['attributes']}\nModifiers: {self.modifiers}"

    def __repr__(self):
        return f"ASTEventDefinitionNode(name={self['name']}, type={self['type']}, body={self['body']}, " \
               f"attributes={self['attributes']}, modifiers={self.modifiers})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_event_definition method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_event_definition(self)


class ASTConversionOperatorDefinitionNode(ASTDefinitionNode):
    """
    Conversion operator definition.
    """

    def __init__(self, target_type: ASTNode, conversion_type: ASTConversionType, parameter: ASTNode,
                 body: Optional[ASTNode] = None, attributes: Optional[ASTNode] = None,
                 modifiers: Optional[Sequence[ASTModifier]] = None):
        """
        Conversion operator definition.

        :param target_type: The type to convert to.
        :param conversion_type: The type of conversion (implicit or explicit).
        :param parameter: The parameter, the corresponding argument of which to convert.
        :param body: The body of the conversion operator.
        :param attributes: The attribute(s) being applied to the conversion operator.
        :param modifiers: The modifier(s) being applied to the conversion operator.
        """
        super().__init__(target_type, attributes, modifiers, {"parameter": parameter, "body": body})
        self.conversion_type = conversion_type

    def __str__(self):
        return f"Conversion operator definition.\nName (Target type): {self['name']}\n" \
               f"Conversion type: {self.conversion_type}\nParameter: {self['parameter']}\nBody: {self['body']}\n" \
               f"Attributes: {self['attributes']}\nModifiers: {self.modifiers}"

    def __repr__(self):
        return f"ASTConversionOperatorDefinitionNode(name={self['name']}, conversion_type={self.conversion_type}, " \
               f"parameter={self['parameter']}, body={self['body']}, attributes={self['attributes']}, " \
               f"modifiers={self.modifiers})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_conversion_operator_definition method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_conversion_operator_definition(self)


class ASTConstructorDefinitionNode(ASTDefinitionNode):
    """
    Constructor definition.
    """

    def __init__(self, name, parameters: Optional[ASTNode] = None, initializer: Optional[ASTNode] = None,
                 body: Optional[ASTNode] = None, attributes=None, modifiers=None):
        """
        Constructor definition.

        :param name: The name of the constructor.
        :param parameters: The parameter(s) of the constructor.
        :param initializer: The initializer of the constructor.
        :param body: The body of the constructor.
        :param attributes: The attribute(s) being applied to the constructor.
        :param modifiers: The modifier(s) being applied to the constructor.
        """
        super().__init__(name, attributes, modifiers,
                         {"parameters": parameters, "initializer": initializer, "body": body})

    def __str__(self):
        return f"Constructor definition.\nName: {self['name']}\nParameters: {self['parameters']}\n" \
               f"Initializer: {self['initializer']}\nBody: {self['body']}\nAttributes: {self['attributes']}\n" \
               f"Modifiers: {self.modifiers}"

    def __repr__(self):
        return f"ASTConstructorDefinitionNode(name={self['name']}, parameters={self['parameters']}, " \
               f"initializer={self['initializer']} body={self['body']}, attributes={self['attributes']}, " \
               f"modifiers={self.modifiers})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_constructor_definition method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_constructor_definition(self)


class ASTDestructorDefinitionNode(ASTDefinitionNode):
    """
    Destructor definition.
    """

    def __init__(self, name, body: Optional[ASTNode] = None, attributes=None, modifiers=None):
        """
        Destructor definition.

        :param name: The name of the destructor.
        :param body: The body of the destructor.
        :param attributes: The attribute(s) being applied to the destructor.
        :param modifiers: The modifier(s) being applied to the destructor.
        """
        super().__init__(name, attributes, modifiers, {"body": body})

    def __str__(self):
        return f"Destructor definition.\nName: {self['name']}\nBody: {self['body']}\n" \
               f"Attributes: {self['attributes']}\nModifiers: {self.modifiers}"

    def __repr__(self):
        return f"ASTDestructorDefinitionNode(name={self['name']}, body={self['body']}, " \
               f"attributes={self['attributes']}, modifiers={self.modifiers})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_destructor_definition method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_destructor_definition(self)


class ASTAccessorDefinitionNode(ASTDefinitionNode):
    """
    Accessor definition.
    """

    def __init__(self, name, body: Optional[ASTNode] = None, attributes=None, modifiers=None):
        """
        Accessor definition.

        :param name: The name of the accessor.
        :param body: The body of the accessor.
        :param attributes: The attribute(s) being applied to the accessor.
        :param modifiers: The modifier(s) being applied to the accessor.
        """
        super().__init__(name, attributes, modifiers, {"body": body})

    def __str__(self):
        return f"Accessor definition.\nName: {self['name']}\nBody: {self['body']}\n" \
               f"Attributes: {self['attributes']}\nModifiers: {self.modifiers}"

    def __repr__(self):
        return f"ASTAccessorDefinitionNode(name={self['name']}, body={self['body']}, " \
               f"attributes={self['attributes']}, modifiers={self.modifiers})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_accessor_definition method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_accessor_definition(self)


class ASTStructDefinitionNode(ASTDefinitionNode):
    """
    Struct definition.
    """

    def __init__(self, name, interfaces: Optional[ASTNode] = None, constraints_clauses: Optional[ASTNode] = None,
                 body: Optional[ASTNode] = None, attributes=None, modifiers=None):
        """
        Struct definition.
        
        :param name: The name of the struct.
        :param interfaces: The interfaces implemented by the struct.
        :param constraints_clauses: The constraint(s) being applied to the struct's type parameters.
        :param body: The body of the struct.
        :param attributes: The attribute(s) being applied to the struct.
        :param modifiers: The modifier(s) being applied to the struct.
        """
        super().__init__(name, attributes, modifiers,
                         {"interfaces": interfaces, "constraints_clauses": constraints_clauses, "body": body})

    def __str__(self):
        return f"Struct definition.\nName: {self['name']}\nInterfaces: {self['interfaces']}\n" \
               f"Constraints clauses: {self['constraints_clauses']}\nBody: {self['body']}\n" \
               f"Attributes: {self['attributes']}\nModifiers: {self.modifiers}"

    def __repr__(self):
        return f"ASTStructDefinitionNode(name={self['name']}, interfaces={self['interfaces']}, " \
               f"constraints_clauses={self['constraints_clauses']}, body={self['body']}, " \
               f"attributes={self['attributes']}, modifiers={self.modifiers})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_struct_definition method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_struct_definition(self)


class ASTInterfaceDefinitionNode(ASTDefinitionNode):
    """
    Interface definition.
    """

    def __init__(self, name, bases: Optional[ASTNode] = None, constraints_clauses: Optional[ASTNode] = None,
                 body: Optional[ASTNode] = None, attributes=None, modifiers=None):
        """
        Interface definition.
        
        :param name: The name of the interface.
        :param bases: The base interfaces inherited by the interface.
        :param constraints_clauses: The constraint(s) being applied to the interface's type parameters.
        :param body: The body of the interface.
        :param attributes: The attribute(s) being applied to the interface.
        :param modifiers: The modifier(s) being applied to the interface.
        """
        super().__init__(name, attributes, modifiers,
                         {"bases": bases, "constraints_clauses": constraints_clauses, "body": body})

    def __str__(self):
        return f"Interface definition.\nName: {self['name']}\nBases: {self['bases']}\n" \
               f"Constraints clauses: {self['constraints_clauses']}\nBody: {self['body']}\n" \
               f"Attributes: {self['attributes']}\nModifiers: {self.modifiers}"

    def __repr__(self):
        return f"ASTInterfaceDefinitionNode(name={self['name']}, bases={self['bases']}, " \
               f"constraints_clauses={self['constraints_clauses']}, body={self['body']}, " \
               f"attributes={self['attributes']}, modifiers={self.modifiers})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_interface_definition method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_interface_definition(self)


class ASTPropertyDefinitionNode(ASTDefinitionNode):
    """
    Property definition.
    """

    def __init__(self, name: ASTNode, type_: Optional[ASTNode] = None, body: Optional[ASTNode] = None,
                 initial_value: Optional[ASTNode] = None, attributes=None, modifiers=None):
        """
        Property definition.
        :param name: The name of the property.
        :param type_: The type of the property.
        :param body: The body of the property.
        :param initial_value: The initial value of the property.
        :param attributes: The attribute(s) being applied to the property.
        :param modifiers: The modifier(s) being applied to the property.
        """
        super().__init__(name, attributes, modifiers, {"type": type_, "body": body, "initial_value": initial_value})

    def __str__(self):
        return f"Property definition.\nName: {self['name']}\nType: {self['type']}\nBody: {self['body']}\n" \
               f"Initial value: {self['initial_value']}\nAttributes: {self['attributes']}\nModifiers: {self.modifiers}"

    def __repr__(self):
        return f"ASTPropertyDefinitionNode(name={self['name']}, type={self['type']}, body={self['body']}, " \
               f"initial_value={self['initial_value']}, attributes={self['attributes']}. modifiers={self.modifiers})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_property_definition method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
                """
        return visitor.visit_property_definition(self)


class ASTEnumDefinitionNode(ASTDefinitionNode):
    """
    Enum definition.
    """

    def __init__(self, name, underlying_type: Optional[ASTNode] = None, body: Optional[ASTNode] = None, attributes=None,
                 modifiers=None):
        """
        Enum definition.
        
        :param name: The name of the enum.
        :param underlying_type: The underlying type of the enum.
        :param body: The body of the enum.
        :param attributes: The attribute(s) being applied to the enum.
        :param modifiers: The modifier(s) being applied to the enum.
        """
        super().__init__(name, attributes, modifiers, {"underlying_type": underlying_type, "body": body})

    def __str__(self):
        return f"Enum definition.\nName: {self['name']}\nUnderlying type: {self['underlying_type']}\n" \
               f"Body: {self['body']}\nAttributes: {self['attributes']}\nModifiers: {self.modifiers}"

    def __repr__(self):
        return f"ASTEnumDefinitionNode(name={self['name']}, underlying_type={self['underlying_type']}, " \
               f"body={self['body']}, attributes={self['attributes']}, modifiers={self.modifiers})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_enum_definition method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_enum_definition(self)


class ASTDelegateDefinitionNode(ASTDefinitionNode):
    """
    Delegate definition.
    """

    def __init__(self, name, return_type: Optional[ASTNode] = None, constraints_clauses: Optional[ASTNode] = None,
                 parameters: Optional[ASTNode] = None, attributes=None, modifiers=None):
        """
        Delegate definition.
        
        :param name: The name of the delegate.
        :param return_type: The return type of the delegate.
        :param constraints_clauses: The constraint(s) being applied to the delegate's type parameters.
        :param parameters: The parameters of the delegate.
        :param attributes: The attribute(s) being applied to the delegate.
        :param modifiers: The modifier(s) being applied to the delegate.
        """
        super().__init__(name, attributes, modifiers,
                         {"return_type": return_type, "constraints_clauses": constraints_clauses,
                          "parameters": parameters})

    def __str__(self):
        return f"Delegate definition.\nName: {self['name']}\nReturn type: {self['return_type']}\n" \
               f"Constraints clauses: {self['constraints_clauses']}\nParameters: {self['parameters']}\n" \
               f"Attributes: {self['attributes']}\nModifiers: {self.modifiers}"

    def __repr__(self):
        return f"ASTDelegateDefinitionNode(name={self['name']}, return_type={self['return_type']}, " \
               f"constraints_clauses={self['constraints_clauses']}, parameters={self['parameters']}, " \
               f"attributes={self['attributes']}, modifiers={self.modifiers})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_delegate_definition method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_delegate_definition(self)


class ASTIndexerDefinitionNode(ASTDefinitionNode):
    """
    Indexer definition.
    """

    def __init__(self, name, return_type: Optional[ASTNode] = None, parameters: Optional[ASTNode] = None,
                 body: Optional[ASTNode] = None,
                 attributes=None, modifiers=None):
        """
        Indexer definition.
        
        :param name: The name of the indexer.
        :param return_type: The return type of the indexer.
        :param parameters: The parameter(s) of the indexer.
        :param body: The body of the indexer.
        :param attributes: The attribute(s) being applied to the indexer.
        :param modifiers: The modifier(s) being applied to the indexer.
        """
        super().__init__(name, attributes, modifiers,
                         {"return_type": return_type, "parameters": parameters, "body": body})

    def __str__(self):
        return f"Indexer definition.\nName: {self['name']}\nReturn type: {self['return_type']}\n" \
               f"Parameters: {self['parameters']}\nBody: {self['body']}\nAttributes: {self['attributes']}\n" \
               f"Modifiers: {self.modifiers}"

    def __repr__(self):
        return f"ASTIndexerDefinitionNode(name={self['name']}, return_type={self['return_type']}, " \
               f"parameters={self['parameters']}, body={self['body']}, attributes={self['attributes']}, " \
               f"modifiers={self.modifiers})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_indexer_definition method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_indexer_definition(self)


class ASTOperatorOverloadDefinitionNode(ASTDefinitionNode):
    """
    Operator overload definition.
    """

    def __init__(self, operator: ASTNode, return_type: Optional[ASTNode] = None, parameters: Optional[ASTNode] = None,
                 body: Optional[ASTNode] = None, attributes=None, modifiers=None):
        """
        Operator overload definition.
        
        :param operator: The operator being overloaded.
        :param return_type: The base operator_overloads inherited by the operator overload.
        :param parameters: The constraint(s) being applied to the operator overload's type parameters.
        :param body: The body of the operator overload.
        :param attributes: The attributes being applied to the operator overload.
        :param modifiers: The modifiers being applied to the operator overload.
        """
        super().__init__(operator, attributes, modifiers,
                         {"return_type": return_type, "parameters": parameters, "body": body})

    def __str__(self):
        return f"Operator overload definition.\nName (Operator): {self['name']}\nReturn type: {self['return_type']}\n" \
               f"Parameters: {self['parameters']}\nBody: {self['body']}\nAttributes: {self['attributes']}\n" \
               f"Modifiers: {self.modifiers}"

    def __repr__(self):
        return f"ASTOperatorOverloadDefinitionNode(name={self['name']}, return_type={self['return_type']}, " \
               f"parameters={self['parameters']}, body={self['body']}, attributes={self['attributes']}, " \
               f"modifiers={self.modifiers})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_operator_overload_definition method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_operator_overload_definition(self)


class ASTFixedSizeBufferDefinitionNode(ASTDefinitionNode):
    """
    Fixed size buffer definition.
    """

    def __init__(self, name: ASTNode, type_: Optional[ASTNode] = None, size: Optional[ASTNode] = None, attributes=None,
                 modifiers=None):
        """
        Fixed size buffer definition.
        
        :param name: The name of the buffer. 
        :param type_: The type of the members of the buffer.
        :param size: The size of the buffer.
        :param attributes: The attribute(s) being applied to the buffer.
        :param modifiers: The modifier(s) being applied to the buffer.
        """
        super().__init__(name, attributes, modifiers, {"type": type_, "size": size})

    def __str__(self):
        return f"Fixed size buffer definition.\nName: {self['name']}\nType: {self['type']}\nSize: {self['size']}\n" \
               f"Attributes: {self['attributes']}\nModifiers: {self.modifiers}"

    def __repr__(self):
        return f"ASTFixedSizeBufferDefinitionNode(name={self['name']}, type={self['type']}, size={self['size']}, " \
               f"attributes={self['attributes']}, modifiers={self.modifiers})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_fixed_size_buffer_definition method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_fixed_size_buffer_definition(self)


# endregion

# endregion

# region Expressions and Misc.


class ASTCatchNode(ASTNode):
    """
    Catch clause.
    """

    def __init__(self, exceptions: Optional[ASTNode] = None, condition: Optional[ASTNode] = None,
                 body: Optional[ASTNode] = None):
        """
        Catch clause.

        :param exceptions: The exception(s) to catch.
        :param condition: The exception filter condition that dictates whether or not to catch the exception.
        :param body: The code to execute if the specified exception(s) are thrown in the corresponding try block.
        """
        super().__init__({"exceptions": exceptions, "condition": condition, "body": body})

    def __str__(self):
        return f"Catch clause.\nExceptions: {self['exceptions']}\nCondition: {self['condition']}\nBody: {self['body']}"

    def __repr__(self):
        return f"ASTCatchNode(exceptions={self['exceptions']}, condition={self['condition']}, body={self['body']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_catch method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_catch(self)


class ASTFinallyNode(ASTNode):
    """
    Finally clause.
    """

    def __init__(self, body: Optional[ASTNode] = None):
        """
        Finally clause.

        :param body: The code to execute after all corresponding try, catch and else blocks,
        regardless of exceptions thrown.
        """
        super().__init__({"body": body})

    def __str__(self):
        return f"Finally clause.\nBody: {self['body']}"

    def __repr__(self):
        return f"ASTFinallyNode(body={self['body']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_finally method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_finally(self)


class ASTYieldExpressionNode(ASTNode):
    """
    Yield expression.
    """

    def __init__(self, values: Optional[ASTNode] = None):
        """
        Yield expression.

        :param values: The value(s) being yielded.
        """
        super().__init__({"values": values})

    def __str__(self):
        return f"Yield expression.\nValues: {self['values']}"

    def __repr__(self):
        return f"ASTYieldExpressionNode(values={self['values']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_yield_expression method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_yield_expression(self)


class ASTBinaryOperationNode(ASTNode):
    """
    Binary operation.
    """

    def __init__(self, operation: Union[ASTOperation], left_operand: ASTNode, right_operand: ASTNode):
        """
        Binary operation.

        :param operation: The operation being performed.
        :param left_operand: The left-hand operand of the operation.
        :param right_operand: The right-hand operand of the operation.
        """
        super().__init__({"left_operand": left_operand, "right_operand": right_operand})
        self.operation = operation

    def __str__(self):
        return f"Binary operation.\nOperation: {self.operation}\nLeft operand: {self['left_operand']}" \
               f"\nRight operand: {self['right_operand']}"

    def __repr__(self):
        return f"ASTBinaryOperationNode(operation={self.operation}, left_operand={self['left_operand']}, " \
               f"right_operand={self['right_operand']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_binary_operation method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_binary_operation(self)


class ASTUnaryOperationNode(ASTNode):
    """
    Unary operation.
    """

    def __init__(self, operation: ASTUnaryOperation, operand: ASTNode):
        """
        Unary operation.

        :param operation: The operation being performed.
        :param operand: The operand of the operation.
        """
        super().__init__({"operand": operand})
        self.operation = operation

    def __str__(self):
        return f"Unary operation.\nOperation: {self.operation}\nOperand: {self['operand']}"

    def __repr__(self):
        return f"ASTUnaryOperationNode(operation={self.operation}, operand={self['operand']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_unary_operation method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_unary_operation(self)


class ASTAliasNode(ASTNode):
    """
    Alias assignment.

    Assign an alias to a target expression.
    """

    def __init__(self, target: ASTNode, alias: ASTNode):
        """
        Alias assignment.

        :param target: The expression to assign the alias to.
        :param alias: The alias to be assigned
        """
        super().__init__({"target": target, "alias": alias})

    def __str__(self):
        return f"Alias assignment.\nTarget: {self['target']}\nAlias: {self['alias']}"

    def __repr__(self):
        return f"ASTAliasNode(target={self['target']}, alias={self['alias']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_alias method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_alias(self)


class ASTFromNode(ASTNode):
    """
    "From" expression.
    """

    def __init__(self, source: ASTNode, expressions: Optional[ASTNode] = None):
        """
        "From" expression.

        :param source: The source to take the expression(s) from.
        :param expressions: The expressions to take.
        """
        super().__init__({"source": source, "expressions": expressions})

    def __str__(self):
        return f"\"From\" expression.\nSource: {self['source']}\nExpressions: {self['expressions']}"

    def __repr__(self):
        return f"ASTFromNode(source={self['source']}, expressions={self['expressions']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_from method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_from(self)


class ASTAnonymousFunctionDefinitionNode(ASTNode):
    """
    Anonymous function definition.
    """

    def __init__(self, body: ASTNode, parameters: Optional[ASTNode] = None):
        """
        Anonymous function definition.

        :param body: The body of the anonymous function.
        :param parameters: The parameter(s) of the function.
        """
        super().__init__({"body": body, "parameters": parameters})

    def __str__(self):
        return f"Anonymous function definition.\nBody: {self['body']}\nParameters: {self['parameters']}"

    def __repr__(self):
        return f"ASTAnonymousFunctionDefinitionNode(body={self['body']}, parameters={self['parameters']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_anonymous_function_definition method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_anonymous_function_definition(self)


class ASTParameterNode(ASTNode):
    """
    Parameter.
    """

    def __init__(self, name: ASTNode, type_: Optional[ASTNode] = None, default: Optional[ASTNode] = None,
                 attributes: Optional[ASTNode] = None, modifiers: Optional[Sequence[ASTModifier]] = None):
        """
        Parameter.

        :param name: The name of the parameter.
        :param type_: The parameter's type.
        :param default: The default value of the parameter.
        :param attributes: The attribute(s) applied to the parameter.
        :param modifiers: The modifier(s) applied to the parameter.
        """
        super().__init__({"name": name, "type": type_, "default": default, "attributes": attributes})
        self.modifiers = modifiers if modifiers is not None else []

    def __str__(self):
        return f"Parameter.\nName: {self['name']}\nType: {self['type']}\nDefault: {self['default']}\n" \
               f"Attributes: {self['attributes']}\nModifiers: {self.modifiers}"

    def __repr__(self):
        return f"ASTParameterNode(name={self['name']}, type={self['type']}, default={self['default']}, " \
               f"attributes={self['attributes']}, modifiers={self.modifiers})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_parameter method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_parameter(self)


class ASTPositionalOnlyParameterNode(ASTParameterNode):
    """
    Positional-only parameter.

    A parameter that may only be fulfilled by a positional argument.
    """

    def __init__(self, name: ASTNode, type_: Optional[ASTNode] = None, default: Optional[ASTNode] = None,
                 attributes: Optional[ASTNode] = None, modifiers: Optional[Sequence[ASTModifier]] = None):
        """
        Positional-only parameter.

        :param name: The name of the parameter.
        :param type_: The parameter's type.
        :param default: The default value of the parameter.
        :param attributes: The attribute(s) applied to the parameter.
        :param modifiers: The modifier(s) applied to the class.
        """
        super().__init__(name, type_, default, attributes, modifiers)

    def __str__(self):
        return f"Positional-only parameter.\nName: {self['name']}\nType: {self['type']}\n" \
               f"Default: {self['default']}\nAttributes: {self['attributes']}\nModifiers: {self.modifiers}"

    def __repr__(self):
        return f"ASTPositionalOnlyParameterNode(name={self['name']}, type={self['type']}, " \
               f"default={self['default']}, attributes={self['attributes']}, modifiers={self.modifiers})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_positional_only_parameter method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_positional_only_parameter(self)


class ASTKeywordOnlyParameterNode(ASTParameterNode):
    """
    Keyword-only parameter.

    A parameter that may only be fulfilled by a keyword argument.
    """

    def __init__(self, name: ASTNode, type_: Optional[ASTNode] = None, default: Optional[ASTNode] = None,
                 attributes: Optional[ASTNode] = None, modifiers: Optional[Sequence[ASTModifier]] = None):
        """
        Keyword-only parameter.

        :param name: The name of the parameter.
        :param type_: The parameter's type.
        :param default: The default value of the parameter.
        :param attributes: The attribute(s) applied to the parameter.
        :param modifiers: The modifier(s) applied to the class.
        """
        super().__init__(name, type_, default, attributes, modifiers)

    def __str__(self):
        return f"Keyword-only parameter.\nName: {self['name']}\nType: {self['type']}\nDefault: {self['default']}\n" \
               f"Attributes: {self['attributes']}\nModifiers: {self.modifiers}"

    def __repr__(self):
        return f"ASTKeywordOnlyParameterNode(name={self['name']}, type={self['type']}, default={self['default']}, " \
               f"attributes={self['attributes']}, modifiers={self.modifiers})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_keyword_only_parameter method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_keyword_only_parameter(self)


class ASTPositionalArgumentsParameterNode(ASTNode):
    """
    Positional arguments parameter.
    """

    def __init__(self, name: ASTNode, type_: Optional[ASTNode] = None, attributes: Optional[ASTNode] = None):
        """
        Positional arguments parameter.

        :param name: The name of the parameter.
        :param type_: The type of all positional arguments supplied using the parameter.
        :param attributes: The attribute(s) applied to all positional arguments supplied using the parameter.
        """
        super().__init__({"name": name, "type": type_, "attributes": attributes})

    def __str__(self):
        return f"Positional arguments parameter.\nName: {self['name']}\nType: {self['type']}\n" \
               f"Attributes: {self['attributes']}"

    def __repr__(self):
        return f"ASTPositionalArgumentsParameterNode(name={self['name']}, type={self['type']}, " \
               f"attributes={self['attributes']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_positional_arguments_parameter method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_positional_arguments_parameter(self)


class ASTKeywordArgumentsParameterNode(ASTNode):
    """
    Keyword arguments parameter.
    """

    def __init__(self, name: ASTNode, type_: Optional[ASTNode] = None):
        """
        Keyword arguments parameter.

        :param name: The name of the parameter.
        :param type_: The type of all keyword arguments supplied using the parameter.
        """
        super().__init__({"name": name, "type": type_})

    def __str__(self):
        return f"Keyword arguments parameter.\nName: {self['name']}\n Type: {self['type']}"

    def __repr__(self):
        return f"ASTKeywordArgumentsParameterNode(name={self['name']}, type={self['type']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_keyword_arguments_parameter method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_keyword_arguments_parameter(self)


class ASTPositionalUnpackExpressionNode(ASTNode):
    """
    Positional unpack expression.
    """

    def __init__(self, expression: ASTNode):
        """
        Positional unpack expression.

        :param expression: The expression to positionally unpack.
        """
        super().__init__({"expression": expression})

    def __str__(self):
        return f"Positional unpack expression.\nExpression: {self['expression']}"

    def __repr__(self):
        return f"ASTPositionalUnpackExpressionNode(expressions={self['expression']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_positional_unpack_expression method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_positional_unpack_expression(self)


class ASTKeywordUnpackExpressionNode(ASTNode):
    """
    Keyword unpack expression.
    """

    def __init__(self, expression: ASTNode):
        """
        Keyword unpack expression.

        :param expression: The expression to keyword-wise unpack.
        """
        super().__init__({"expression": expression})

    def __str__(self):
        return f"Keyword unpack expression.\nExpression: {self['expression']}"

    def __repr__(self):
        return f"ASTKeywordUnpackExpressionNode(expressions={self['expression']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_keyword_unpack_expression method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_keyword_unpack_expression(self)


class ASTAsyncNode(ASTNode):
    """
    Async declaration.
    """

    def __init__(self, target: ASTNode):
        """
        Async declaration.

        :param target: The code to be declared as asynchronous.
        """
        super().__init__({"target": target})

    def __str__(self):
        return f"Async declaration.\nTarget: {self['target']}"

    def __repr__(self):
        return f"ASTAsyncNode(target={self['target']}"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_async method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_async(self)


class ASTAwaitNode(ASTNode):
    """
    Await expression.
    """

    def __init__(self, expression: ASTNode):
        """
        Await expression.

        :param expression: The expression to await.
        """
        super().__init__({"expression": expression})

    def __str__(self):
        return f"Await expression.\nExpression: {self['expression']}"

    def __repr__(self):
        return f"ASTAwaitNode(expression={self['expression']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_await method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_await(self)


class ASTMemberNode(ASTNode):
    """
    Member access.
    """

    def __init__(self, parent: ASTNode, member: ASTNode):
        """
        Member access.

        :param parent: The member's parent.
        :param member: The member to access.
        """
        super().__init__({"parent": parent, "member": member})

    def __str__(self):
        return f"Member access.\nParent: {self['parent']}\nMember: {self['member']}"

    def __repr__(self):
        return f"ASTMemberNode(parent={self['parent']}, member={self['member']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_member method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_member(self)


class ASTAccessNode(ASTNode):
    """
    Access.

    Sequence element(s) access.
    """

    def __init__(self, sequence: ASTNode, expressions: ASTNode):
        """
        Access.

        :param sequence: The sequence to access.
        :param expressions: The expression(s) defining which elements to access.
        """
        super().__init__({"sequence": sequence, "expressions": expressions})

    def __str__(self):
        return f"Sequence element(s) access.\nSequence: {self['sequence']}\nExpressions: {self['expressions']}"

    def __repr__(self):
        return f"ASTAccessNode(sequence={self['sequence']}, expressions={self['expressions']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_access method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_access(self)


class ASTIndexNode(ASTNode):
    """
    Index.

    Sequence single element access.
    """

    def __init__(self, index: ASTNode):
        """
        Index.

        :param index: The index of the element to access.
        """
        super().__init__({"index": index})

    def __str__(self):
        return f"Sequence single element access.\nIndex: {self['index']}"

    def __repr__(self):
        return f"ASTIndexNode(index={self['index']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_index method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_index(self)


class ASTSliceNode(ASTNode):
    """
    Slice.

    Sequence slice access.
    """

    def __init__(self, start: Optional[ASTNode] = None, stop: Optional[ASTNode] = None, step: Optional[ASTNode] = None):
        """
        Slice.

        :param start: The index of the first element in the slice.
        :param stop: The index to slice up to.
        :param step: The step of the slice.
        """
        super().__init__({"start": start, "stop": stop, "step": step})

    def __str__(self):
        return f"Sequence slice access.\nStart: {self['start']}\nStop: {self['stop']}\nStep: {self['step']}"

    def __repr__(self):
        return f"ASTSliceNode(start={self['start']}, stop={self['stop']}, step={self['step']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_slice method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_slice(self)


class ASTCallNode(ASTNode):
    """
    Method/function call.
    """

    def __init__(self, function: ASTNode, arguments: Optional[ASTNode] = None):
        """
        Method/function call.

        :param function: The function being called.
        :param arguments: The arguments being supplied to the function.
        """
        super().__init__({"function": function, "arguments": arguments})

    def __str__(self):
        return f"Method/function call.\nFunction: {self['function']}\nArguments: {self['arguments']}"

    def __repr__(self):
        return f"ASTCallNode(function={self['function']}, arguments={self['arguments']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_call method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_call(self)


class ASTArgumentNode(ASTNode):
    """
    Argument.
    """

    def __init__(self, value: ASTNode, modifiers: Optional[Sequence[ASTModifier]] = None):
        """
        Argument.

        :param value: The value being passed in as the argument.
        :param modifiers: The modifiers applied to the argument.
        """
        super().__init__({"value": value})
        self.modifiers = modifiers if modifiers is not None else []

    def __str__(self):
        return f"Argument.\nValue: {self['value']}\nModifiers: {self.modifiers}"

    def __repr__(self):
        return f"ASTArgumentNode(value={self['value']}, modifiers={self.modifiers})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_argument method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_argument(self)


class ASTKeywordArgumentNode(ASTNode):
    """
    Keyword argument.
    """

    def __init__(self, parameter: ASTNode, value: ASTNode, modifiers: Optional[Sequence[ASTModifier]] = None):
        """
        Keyword argument.

        :param parameter: The parameter to assign the value to.
        :param value: The value being passed in as the argument.
        :param modifiers: The modifiers applied to the argument.
        """
        super().__init__({"parameter": parameter, "value": value})
        self.modifiers = modifiers if modifiers is not None else []

    def __str__(self):
        return f"Keyword argument.\nParameter: {self['parameter']}\nValue: {self['value']}\nModifiers: {self.modifiers}"

    def __repr__(self):
        return f"ASTKeywordArgumentNode(parameter={self['parameter']}, value={self['value']}, " \
               f"modifiers={self.modifiers})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_keyword_argument method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_keyword_argument(self)


class ASTGeneratorExpressionNode(ASTNode):
    """
    Generator Expression.
    """

    def __init__(self, expression: ASTNode):
        """
        Generator expression.

        :param expression: The expression defining the generator.
        """
        super().__init__({"expression": expression})

    def __str__(self):
        return f"Generator expression.\nExpression: {self['expression']}"

    def __repr__(self):
        return f"ASTGeneratorExpressionNode(expression={self['expression']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_generator_expression method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_generator_expression(self)


class ASTComprehensionNode(ASTNode):
    """
    Comprehension expression.
    """

    def __init__(self, value: ASTNode, loop: ASTNode):
        """
        Comprehension expression.

        :param value: The value to return from the loop.
        :param loop: The loop represented in the comprehension.
        """
        super().__init__({"value": value, "loop": loop})

    def __str__(self):
        return f"Comprehension expression.\nValue: {self['value']}\nLoop: {self['loop']}"

    def __repr__(self):
        return f"ASTComprehensionNode(value={self['value']}, loop={self['loop']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_comprehension method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_comprehension(self)


class ASTListNode(ASTNode):
    """
    List declaration.
    """

    def __init__(self, elements: ASTNode):
        """
        List declaration.

        :param elements: The elements of the list.
        """
        super().__init__({"elements": elements})

    def __str__(self):
        return f"List declaration.\nElements: {self['elements']}"

    def __repr__(self):
        return f"ASTListNode(elements={self['elements']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_list method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_list(self)


class ASTTupleNode(ASTNode):
    """
    Tuple declaration.
    """

    def __init__(self, elements: ASTNode):
        """
        Tuple declaration.

        :param elements: The elements of the tuple.
        """
        super().__init__({"elements": elements})

    def __str__(self):
        return f"Tuple declaration.\nElements: {self['elements']}"

    def __repr__(self):
        return f"ASTTupleNode(elements={self['elements']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_tuple method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_tuple(self)


class ASTSetNode(ASTNode):
    """
    Set declaration.
    """

    def __init__(self, elements: ASTNode):
        """
        Set declaration.

        :param elements: The elements of the set.
        """
        super().__init__({"elements": elements})

    def __str__(self):
        return f"Set declaration.\nElements: {self['elements']}"

    def __repr__(self):
        return f"ASTSetNode(elements={self['elements']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_set method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_set(self)


class ASTMapNode(ASTNode):
    """
    Map declaration.
    """

    def __init__(self, elements: ASTNode):
        """
        Map declaration.

        :param elements: The elements of the map.
        """
        super().__init__({"elements": elements})

    def __str__(self):
        return f"Map declaration.\nElements: {self['elements']}"

    def __repr__(self):
        return f"ASTMapNode(elements={self['elements']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_map method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_map(self)


class ASTKeyValuePairNode(ASTNode):
    """
    Key-value pair.
    """

    def __init__(self, key: ASTNode, value: ASTNode):
        """
        Key-value pair.

        :param key: The key.
        :param value: The value.
        """
        super().__init__({"key": key, "value": value})

    def __str__(self):
        return f"Key-value pair.\nKey: {self['key']}\nValue: {self['value']}"

    def __repr__(self):
        return f"ASTKeyValuePairNode(key={self['key']}, value={self['value']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_key_value_pair method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_key_value_pair(self)


class ASTDecoratedNode(ASTNode):
    """
    Decorated statement.
    """

    def __init__(self, decorators: ASTNode, target: ASTNode):
        """
        Decorated statement.

        :param decorators: The decorators applied to the target.
        :param target: The target that is decorated.
        """
        super().__init__({"decorators": decorators, "target": target})

    def __str__(self):
        return f"Decorated statement.\nDecorators: {self['decorators']}\nTarget: {self['target']}"

    def __repr__(self):
        return f"ASTDecoratedNode(decorators={self['decorators']}, target={self['target']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_decorated method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_decorated(self)


class ASTDecoratorNode(ASTNode):
    """
    Decorator.
    """

    def __init__(self, name: ASTNode, arguments: Optional[ASTNode] = None):
        """
        Decorator.

        :param name: The name of the decorator.
        :param arguments: The arguments supplied to the decorator.
        """
        super().__init__({"name": name, "arguments": arguments})

    def __str__(self):
        return f"Decorator.\nName: {self['name']}\nArguments: {self['arguments']}"

    def __repr__(self):
        return f"ASTDecoratorNode(name={self['name']}, arguments={self['arguments']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_decorator method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_decorator(self)


class ASTConditionalExpressionNode(ASTNode):
    """
    Conditional expression.
    """

    def __init__(self, condition: ASTNode, consequent: ASTNode, alternative: ASTNode):
        """
        Conditional expression.

        :param condition: The condition to evaluate.
        :param consequent: The expression to evaluate if the condition is true.
        :param alternative: The expression to evaluate if the condition is false.
        """
        super().__init__({"condition": condition, "consequent": consequent, "alternative": alternative})

    def __str__(self):
        return f"Conditional expression.\nCondition: {self['condition']}\nConsequent: {self['consequent']}\n" \
               f"Alternative: {self['alternative']}"

    def __repr__(self):
        return f"ASTConditionalExpressionNode(condition={self['condition']}, consequent={self['consequent']}, " \
               f"alternative={self['alternative']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_conditional_expression method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_conditional_expression(self)


class ASTNullCoalescingExpressionNode(ASTNode):
    """
    Null-coalescing expression.
    """

    def __init__(self, expression: ASTNode, alternative: ASTNode):
        """
        Null-coalescing expression.

        :param expression: The expression to evaluate.
        :param alternative: The expression to evaluate if the expression is null.
        """
        super().__init__({"expression": expression, "alternative": alternative})

    def __str__(self):
        return f"Null-coalescing expression.\nExpression: {self['expression']}\nAlternative: {self['alternative']}"

    def __repr__(self):
        return f"ASTNullCoalescingExpressionNode(expression={self['expression']} alternative={self['alternative']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_null_coalescing_expression method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_null_coalescing_expression(self)


class ASTTypeCastNode(ASTNode):
    """
    Type cast.
    """

    def __init__(self, type_: ASTNode, expression: ASTNode):
        """
        Type cast.

        :param type_: The type to cast the expression to.
        :param expression: The expression to cast.
        """
        super().__init__({"type": type_, "expression": expression})

    def __str__(self):
        return f"Type cast.\nType: {self['type']}\nExpression: {self['expression']}"

    def __repr__(self):
        return f"ASTTypeCastNode(type={self['type']}, expression={self['expression']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_type_cast method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_type_cast(self)


class ASTTypeNode(ASTNode):
    """
    Type.
    """

    def __init__(self, name: ASTNode, arguments: ASTNode):
        """
        Type.
        
        :param name: The type's name. 
        :param arguments: The type's arguments. 
        """
        super().__init__({"name": name, "arguments": arguments})

    def __str__(self):
        return f"Type.\nName: {self['name']}\nArguments: {self['arguments']}"

    def __repr__(self):
        return f"ASTTypeNode(name={self['name']}, arguments={self['arguments']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_type method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_type(self)


class ASTObjectCreationNode(ASTNode):
    """
    Object creation.
    """

    def __init__(self, type_: Optional[ASTNode] = None, arguments: Optional[ASTNode] = None,
                 initializer: Optional[ASTNode] = None):
        """
        Object creation.

        :param type_: The type of the object being created.
        :param arguments: The arguments passed to the type's constructor.
        :param initializer: The initial values of the object.
        """
        super().__init__({"type": type_, "arguments": arguments, "initializer": initializer})

    def __str__(self):
        return f"Object creation.\nType: {self['type']}\nArguments: {self['arguments']}\n" \
               f"Initializer: {self['initializer']}"

    def __repr__(self):
        return f"ASTObjectCreationNode(type={self['type']}, arguments={self['arguments']}, " \
               f"initializer={self['initializer']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_object_creation method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_object_creation(self)


class ASTArrayCreationNode(ASTNode):
    """
    Array creation.
    """

    def __init__(self, type_: Optional[ASTNode] = None, dimensions: Optional[int] = 1, size: Optional[ASTNode] = None,
                 initializer: Optional[ASTNode] = None):
        """
        Array creation.

        :param type_: The type of the array being created.
        :param dimensions: The dimensions of the array.
        :param size: The size of the array.
        :param initializer: The initial values of the array.
        """
        super().__init__({"type": type_, "size": size, "initializer": initializer})
        self.dimensions = dimensions

    def __str__(self):
        return f"Array creation.\nType: {self['type']}\nSize: {self['size']}\nInitializer: {self['initializer']}"

    def __repr__(self):
        return f"ASTArrayCreationNode(type={self['type']}, size={self['size']}, initializer={self['initializer']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_array_creation method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_array_creation(self)


class ASTInitializerNode(ASTNode):
    """
    Initializer.
    """

    def __init__(self, expressions: Optional[ASTNode] = None):
        """
        Initializer.

        :param expressions: The expressions contained within the initializer.
        """
        super().__init__({"expressions": expressions})

    def __str__(self):
        return f"Initializer.\nExpressions: {self['expressions']}"

    def __repr__(self):
        return f"ASTInitializerNode(expressions={self['expressions']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_initializer method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_initializer(self)


class ASTQueryNode(ASTNode):
    """
    Query.
    """

    def __init__(self, clauses: ASTNode):
        """
        Query.

        :param clauses: The clauses that make up the query.
        """
        super().__init__({"clauses": clauses})

    def __str__(self):
        return f"Query.\nClauses: {self['clauses']}"

    def __repr__(self):
        return f"ASTQueryNode(clauses={self['clauses']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_query method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_query(self)


class ASTFromClauseNode(ASTNode):
    """
    From clause.
    """

    def __init__(self, range_variable: ASTNode, source: ASTNode):
        """
        From clause.
        
        :param range_variable: The variable representing each element in the source.
        :param source: The data source on which a query is being run.
        """
        super().__init__({"range_variable": range_variable, "source": source})

    def __str__(self):
        return f"From clause.\nRange variable: {self['range_variable']}\nSource: {self['source']}"

    def __repr__(self):
        return f"ASTFromClauseNode(range_variable={self['range_variable']}, source={self['source']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_from_clause method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_from_clause(self)


class ASTLetClauseNode(ASTNode):
    """
    Let clause.
    """

    def __init__(self, name: ASTNode, value: ASTNode):
        """
        Let clause.

        :param name: The variable to assign a value to.
        :param value: The value to be assigned..
        """
        super().__init__({"name": name, "value": value})

    def __str__(self):
        return f"Let clause.\nName: {self['name']}\nValue: {self['value']}"

    def __repr__(self):
        return f"ASTLetClauseNode(name={self['name']}, value={self['value']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_let_clause method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_let_clause(self)


class ASTWhereClauseNode(ASTNode):
    """
    Where clause.
    """

    def __init__(self, predicate: ASTNode):
        """
        Where clause.

        :param predicate: The boolean predicate to apply to each source element.
        """
        super().__init__({"predicate": predicate})

    def __str__(self):
        return f"Where clause.\nPredicate: {self['predicate']}"

    def __repr__(self):
        return f"ASTWhereClauseNode(predicate={self['predicate']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_where_clause method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_where_clause(self)


class ASTJoinClauseNode(ASTNode):
    """
    Join clause.
    """

    def __init__(self, target_range_variable: ASTNode, target_source: ASTNode, left_key: ASTNode, right_key: ASTNode):
        """
        Join clause.

        :param target_range_variable: The variable representing each element in the target source.
        :param target_source: The target data source on which the join is being performed.
        :param left_key: The left-hand key being checked for equality.
        :param right_key: The right-hand key being checked for equality.
        """
        super().__init__(
            {"target_range_variable": target_range_variable, "target_source": target_source, "left_key": left_key,
             "right_key": right_key})

    def __str__(self):
        return f"Join clause.\nTarget range variable: {self['target_range_variable']}\n" \
               f"Target source: {self['target_source']}\nLeft key: {self['left_key']}\n" \
               f"Right key: {self['right_key']}"

    def __repr__(self):
        return f"ASTJoinClauseNode(target_range_variable={self['target_range_variable']}, " \
               f"target_source={self['target_source']}, left_key={self['left_key']}, " \
               f"right_key={self['right_key']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_join_clause method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_join_clause(self)


class ASTOrderByClauseNode(ASTNode):
    """
    Order-by clause.
    """

    def __init__(self, orderings: ASTNode):
        """
        Order-by clause.

        :param orderings: The variable representing each element in the target source.
        """
        super().__init__({"orderings": orderings})

    def __str__(self):
        return f"Order-by clause.\nOrderings: {self['orderings']}"

    def __repr__(self):
        return f"ASTOrderByClauseNode(orderings={self['orderings']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_order_by_clause method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_order_by_clause(self)


class ASTOrderingNode(ASTNode):
    """
    Ordering.
    """

    def __init__(self, key: ASTNode, direction: ASTNode = None):
        """
        Ordering.

        :param key: The key specifying what to order by.
        :param direction: The direction in which to order.
        """
        super().__init__({"key": key, "direction": direction})

    def __str__(self):
        return f"Ordering.\nKey: {self['key']}\nDirection: {self['direction']}"

    def __repr__(self):
        return f"ASTOrderingNode(key={self['key']}, direction={self['direction']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_ordering method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_ordering(self)


class ASTSelectClauseNode(ASTNode):
    """
    Select clause.
    """

    def __init__(self, expression: ASTNode):
        """
        Select clause.

        :param expression: The expression specifying the type of values produced by the query.
        """
        super().__init__({"expression": expression})

    def __str__(self):
        return f"Select clause.\nExpression: {self['expression']}"

    def __repr__(self):
        return f"ASTSelectClauseNode(expression={self['expression']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_select_clause method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_select_clause(self)


class ASTGroupByClauseNode(ASTNode):
    """
    Group-by clause.
    """

    def __init__(self, range_variable: ASTNode, key: ASTNode):
        """
        Group-by clause.

        :param range_variable: The variable representing each element in the target source.
        :param key: The key specifying how values are to be grouped.
        """
        super().__init__({"range_variable": range_variable, "key": key})

    def __str__(self):
        return f"Group-by clause.\nRange variable: {self['range_variable']}\nKey: {self['key']}"

    def __repr__(self):
        return f"ASTGroupByClauseNode(range_variable={self['range_variable']}, key={self['key']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_group_by_clause method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_group_by_clause(self)


class ASTIntoClauseNode(ASTNode):
    """
    Into clause.
    """

    def __init__(self, identifier: ASTNode):
        """
        Into clause.

        :param identifier: The identifier to store the results of the previous clause against.
        """
        super().__init__({"identifier": identifier})

    def __str__(self):
        return f"Into clause.\nIdentifier: {self['identifier']}"

    def __repr__(self):
        return f"ASTIntoClauseNode(identifier={self['identifier']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_into_clause method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_into_clause(self)


class ASTLabelNode(ASTNode):
    """
    Label.
    """

    def __init__(self, name: ASTNode, target: ASTNode):
        """
        Label.
        
        :param name: The name of the label. 
        :param target: The target of the label.
        """
        super().__init__({"name": name, "target": target})

    def __str__(self):
        return f"Label.\nName: {self['name']}\nTarget: {self['target']}"

    def __repr__(self):
        return f"ASTLabelNode(name={self['name']}, target={self['target']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_label method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_label(self)


class ASTSwitchSectionNode(ASTNode):
    """
    Switch section.
    """

    def __init__(self, labels: ASTNode, body: ASTNode):
        """
        Switch section.

        :param labels: The labels contained within the switch section.
        :param body: The code to execute if the match expressions matches with one of the label patterns.
        """
        super().__init__({"labels": labels, "body": body})

    def __str__(self):
        return f"Switch section.\nLabels: {self['labels']}\nBody: {self['body']}"

    def __repr__(self):
        return f"ASTSwitchStatementNode(labels={self['labels']}, body={self['body']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_switch_statement method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_switch_section(self)


class ASTCaseLabelNode(ASTNode):
    """
    Case label.
    """

    def __init__(self, pattern: ASTNode):
        """
        Case label.

        :param pattern: The pattern for the case label.
        """
        super().__init__({"pattern": pattern})

    def __str__(self):
        return f"Case label.\nPattern: {self['pattern']}"

    def __repr__(self):
        return f"ASTCaseLabelNode(pattern={self['pattern']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_case_label method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_case_label(self)


class ASTDefaultLabelNode(ASTNode):
    """
    Default label.
    """

    def __init__(self):
        super().__init__()

    def __str__(self):
        return f"Default label."

    def __repr__(self):
        return f"ASTDefaultLabelNode()"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_default_label method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_default_label(self)


class ASTAttributeSectionNode(ASTNode):
    """
    Attribute section.
    """

    def __init__(self, attributes: ASTNode, target: Optional[ASTNode] = None):
        """
        Attribute section.

        :param attributes: The attributes being applied.
        :param target: The target for the the attributes.
        """
        super().__init__({"target": target, "attributes": attributes})

    def __str__(self):
        return f"Attribute section.\nAttributes: {self['attributes']}\nTarget: {self['target']}"

    def __repr__(self):
        return f"ASTAttributeSectionNode(attributes={self['attributes']}, target={self['target']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_attribute_section method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_attribute_section(self)


class ASTAttributeNode(ASTNode):
    """
    Attribute.
    """

    def __init__(self, name: ASTNode, arguments: Optional[ASTNode] = None):
        """
        Attribute.
        
        :param name: The name of the attribute. 
        :param arguments: The attribute's arguments.
        """
        super().__init__({"name": name, "arguments": arguments})

    def __str__(self):
        return f"Attribute.\nName: {self['name']}\nArguments: {self['arguments']}"

    def __repr__(self):
        return f"ASTAttributeNode(name={self['name']}, arguments={self['arguments']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_attribute method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_attribute(self)


class ASTPointerTypeNode(ASTNode):
    """
    Pointer type.
    """

    def __init__(self, type_: ASTNode):
        """
        Pointer type.

        :param type_: The type of the value that the pointer points to.
        """
        super().__init__({"type": type_})

    def __str__(self):
        return f"Pointer type.\nType: {self['type']}"

    def __repr__(self):
        return f"ASTPointerTypeNode(type={self['type']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_pointer_type method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_pointer_type(self)


class ASTNullableTypeNode(ASTNode):
    """
    Nullable type.
    """

    def __init__(self, type_: ASTNode):
        """
        Nullable type.

        :param type_: The type that may also be null.
        """
        super().__init__({"type": type_})

    def __str__(self):
        return f"Nullable type.\nType: {self['type']}"

    def __repr__(self):
        return f"ASTNullableTypeNode(type={self['type']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_nullable_type method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_nullable_type(self)


class ASTArrayTypeNode(ASTNode):
    """
    Array type.
    """

    def __init__(self, type_: ASTNode, dimensions: Optional[int] = 1):
        """
        Array type.

        :param type_: The type of the elements in the array.
        :param dimensions: The number of dimensions in the array.
        """
        super().__init__({"type": type_})
        self.dimensions = dimensions

    def __str__(self):
        return f"Array type.\nType: {self['type']}\nDimensions: {self.dimensions}"

    def __repr__(self):
        return f"ASTArrayTypeNode(type={self['type']}, dimensions={self.dimensions})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_array_type method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_array_type(self)


class ASTConstraintsClauseNode(ASTNode):
    """
    Constraints clause.
    """

    def __init__(self, type_parameter: ASTNode, constraints: ASTNode):
        """
        Constraints clause.
        
        :param type_parameter: The type parameter to apply the constraint(s) to. 
        :param constraints: The constraint(s) to apply.
        """
        super().__init__({"type_parameter": type_parameter, "constraints": constraints})

    def __str__(self):
        return f"Constraints clause.\nType parameter: {self['type_parameter']}\nConstraints: {self['constraints']}"

    def __repr__(self):
        return f"ASTConstraintsClauseNode(type_parameter={self['type_parameter']}, constraints={self['constraints']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_constraints_clause method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_constraints_clause(self)


class ASTStackAllocationNode(ASTNode):
    """
    Stack allocation.
    """

    def __init__(self, type_: ASTNode, length: ASTNode):
        super().__init__({"type": type_, "length": length})

    def __str__(self):
        return f"Stack allocation.\nType: {self['type']}\nLength: {self['length']}"

    def __repr__(self):
        return f"ASTStackAllocationNode(type={self['type']}, length={self['length']})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_stack_allocation method.
        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_stack_allocation(self)


# endregion

# region Enums

class ASTEnum(Enum):
    """
    Base class for enums.
    """

    def __repr__(self):
        return self.value


# Operation Enums

class ASTOperation(ASTEnum):
    """
    Base class for operation enums.
    """
    pass


class ASTArithmeticOperation(ASTOperation):
    """
    Arithmetic operations enum.
    """

    ADD = "Add"
    SUBTRACT = "Subtract"
    MULTIPLY = "Multiply"
    DIVIDE = "Divide"
    FLOOR_DIVIDE = "Floor Divide"
    MODULO = "Modulo"
    POWER = "Power"
    MATRIX_MULTIPLY = "Matrix Multiply"


class ASTBitwiseOperation(ASTOperation):
    """
    Bitwise operations enum.
    """

    AND = "Bitwise And"
    OR = "Bitwise Or"
    XOR = "Bitwise Xor"
    LEFT_SHIFT = "Bitwise Left Shift"
    RIGHT_SHIFT = "Bitwise Right Shift"


class ASTLogicalOperation(ASTOperation):
    """
    Logical operations enum.
    """
    AND = "Logical And"
    OR = "Logical Or"


class ASTComparisonOperation(ASTOperation):
    """
    Comparison operations enum.
    """

    EQUAL = "Equal"
    NOT_EQUAL = "Not Equal"
    LESS_THAN = "Less Than"
    GREATER_THAN = "Greater Than"
    LESS_THAN_OR_EQUAL = "Less Than Or Equal"
    GREATER_THAN_OR_EQUAL = "Greater Than Or Equal"
    IN = "In"
    IS = "Is"


class ASTUnaryOperation(ASTOperation):
    """
    Unary operations enum.
    """
    POSITIVE = "Positive"
    ARITHMETIC_NEGATION = "Negation (Arithmetic)"
    LOGICAL_NEGATION = "Negation (Logical)"
    BITWISE_INVERSION = "Bitwise Inversion"
    INCREMENT = "Increment"
    DECREMENT = "Decrement"
    POINTER_DEREFERENCE = "Pointer Dereference"
    ADDRESS = "Address"
    NULL_CONDITIONAL = "Null Conditional"


class ASTInPlaceOperation(ASTOperation):
    """
    In-place operations enum.
    """

    ADD = "In-Place Add"
    SUBTRACT = "In-Place Subtract"
    MULTIPLY = "In-Place Multiply"
    DIVIDE = "In-Place Divide"
    FLOOR_DIVIDE = "In-Place Floor Divide"
    MODULO = "In-Place Modulo"
    POWER = "In-Place Power"
    MATRIX_MULTIPLY = "In-Place Matrix Multiply"
    BITWISE_AND = "In-Place Bitwise And"
    BITWISE_OR = "In-Place Bitwise Or"
    BITWISE_XOR = "In-Place Bitwise Xor"
    LEFT_SHIFT = "In-Place Left Shift"
    RIGHT_SHIFT = "In-Place Right Shift"


class ASTSequenceOperation(ASTOperation):
    """
    Sequence operations enum.
    """

    CONCAT = "Concatenation"


# Modifier Enums

class ASTModifier(ASTEnum):
    """
    Base class for modifier enums.
    """
    pass


class ASTVisibilityModifier(ASTModifier):
    """
    Access modifiers enum.
    """

    PUBLIC = "Public"
    PROTECTED = "Protected"
    INTERNAL = "Internal"
    PRIVATE = "Private"
    PROTECTED_INTERNAL = "Protected Internal"
    PRIVATE_PROTECTED = "Private Protected"


class ASTConversionType(ASTModifier):
    """
    Conversion types enum.
    """
    IMPLICIT = "Implicit"
    EXPLICIT = "Explicit"


class ASTMiscModifier(ASTModifier):
    """
    Miscellaneous modifiers enum.
    """
    ABSTRACT = "Abstract"
    ASYNC = "Async"
    EVENT = "Event"
    CONST = "Const"
    EXTERN = "Extern"
    IN = "In"
    NEW = "New"
    OVERRIDE = "Override"
    OUT = "Out"
    PARTIAL = "Partial"
    READONLY = "Read-only"
    REF = "Ref"
    SEALED = "Sealed"
    STATIC = "Static"
    THIS = "This"
    UNSAFE = "Unsafe"
    VIRTUAL = "Virtual"
    VOLATILE = "Volatile"


# Literal Enums

class ASTLiteralType(ASTEnum):
    """
    Literal types enum.
    """

    NUMBER = "Number"
    CHAR = "Char"
    STRING = "String"
    BOOLEAN = "Boolean"
    NULL = "Null"
    ELLIPSIS = "Ellipsis"

# endregion
