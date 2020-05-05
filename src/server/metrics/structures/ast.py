from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Optional, Sequence, Union

from metrics.structures.base.graph import *

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

    def accept(self, visitor: ASTVisitor):
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

    def __init__(self, *children: ASTNode):
        """
        Node.

        :param children: The child nodes of the node.
        """
        super().__init__(*children)

    def __str__(self):
        return f"Generic abstract syntax tree node.\nChildren: {self.children}"

    def __repr__(self):
        return f"ASTNode(children={self.children})"

    def accept(self, visitor: ASTVisitor):
        """
        Accept an AST visitor.

        :param visitor: The AST visitor to accept.
        :return: The result of the accept.
        """
        return super().accept(visitor)


# Terminals

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


# Multiples

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
        super().__init__(*children)

    def __str__(self):
        return f"Multiple, consecutive nodes (generic).\nChildren: {self.children}"

    def __repr__(self):
        return f"ASTMultiplesNode(children={self.children})"

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
        return f"Multiple, consecutive statements.\nChildren: {self.children}"

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
        return f"Multiple, consecutive expressions.\nChildren: {self.children}"

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
        return f"Multiple, consecutive variables.\nChildren: {self.children}"

    def __repr__(self):
        return f"ASTVariablesNode(children={self.children})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_variabes method.
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
        return f"Multiple, consecutive list, map or set elements.\nChildren: {self.children}"

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
        return f"Multiple, consecutive parameters.\nChildren: {self.children}"

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
        return f"Multiple, consecutive arguments.\nChildren: {self.children}"

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
        return f"Multiple, consecutive subscripts.\nChildren: {self.children}"

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
        return f"Multiple, consecutive catches.\nChildren: {self.children}"

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
        return f"Multiple, consecutive decorators.\nChildren: {self.children}"

    def __repr__(self):
        return f"ASTDecoratorsNode(children={self.children})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_decorators method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_decorators(self)


# Statements

class ASTStatementNode(ASTNode):
    """
    Statement.

    Base class for representing a statement.
    """

    def __init__(self, *children: ASTNode):
        """
        Statement.

        :param children: The child nodes of the statement node.
        """
        super().__init__(*children)

    def __str__(self):
        return f"Generic statement.\nChildren: {self.children}"

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
        self.target = target
        super().__init__(self.target)

    def __str__(self):
        return f"Delete statement.\nTarget: {self.target}"

    def __repr__(self):
        return f"ASTDelStatementNode(target={self.target})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_del_statement method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_del_statement(self)


class ASTVariableDeclarationNode(ASTStatementNode):
    """
    Variable declaration.

    Declaring one or more variables.
    """

    def __init__(self, variables: ASTNode, type_: ASTNode = None, modifiers: Sequence[ASTModifier] = None):
        """
        Variable declaration.
        :param variables: The variable(s) being declared.
        :param type_: The type of the variable(s) being declared.
        :param modifiers: The modifier(s) applied to the variable(s).
        """
        self.variables = variables
        self.type = type_
        self.modifiers = modifiers if modifiers is not None else []
        super().__init__(self.variables, self.type)

    def __str__(self):
        return f"Variable declaration.\nVariable(s): {self.variables}\nType: {self.type}\nModifiers: {self.modifiers}"

    def __repr__(self):
        return f"ASTVariableDeclaration(variables={self.variables}, type={self.type}, modifiers={self.modifiers})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_variable_declaration method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_variable_declaration(self)


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
        self.variables = variables
        self.values = values
        super().__init__(self.variables, self.values)

    def __str__(self):
        return f"Standard variable assignment statement.\nVariable(s): {self.variables}\nValue(s): {self.values}"

    def __repr__(self):
        return f"ASTAssignmentStatementNode(variables={self.variables}, values={self.values}"

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
        self.variables = variables
        self.values = values
        super().__init__(self.variables, self.values)

    def __str__(self):
        return f"Augmented assignment statement.\nOperation: {self.operation}\nVariables: {self.variables}" \
               f"\nValues: {self.values}"

    def __repr__(self):
        return f"ASTAugmentedAssignmentStatementNode(operation={self.operation}, variables={self.variables}, " \
               f"values={self.values})"

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
        self.annotation = annotation
        self.variables = variables
        self.values = values
        super().__init__(self.variables, self.annotation, self.values)

    def __str__(self):
        return f"Annotated assignment statement.\nAnnotation: {self.annotation}\nVariables: {self.variables}" \
               f"\nValues: {self.values}"

    def __repr__(self):
        return f"ASTAnnotatedAssignmentStatementNode(annotation={self.annotation}, variables={self.variables}, " \
               f"values={self.values})"

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
        self.values = values
        super().__init__(self.values)

    def __str__(self):
        return f"Yield statement.\nValues: {self.values}"

    def __repr__(self):
        return f"ASTYieldStatementNode(values={self.values})"

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
        self.values = values
        super().__init__(self.values)

    def __str__(self):
        return f"Return statement.\nValues: {self.values}"

    def __repr__(self):
        return f"ASTReturnStatementNode(values={self.values})"

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
        self.exception = exception
        super().__init__(self.exception)

    def __str__(self):
        return f"Throw statement.\nException: {self.exception}"

    def __repr__(self):
        return f"ASTThrowStatementNode(exception={self.exception})"

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

    def __init__(self, libraries: ASTNode):
        """
        Import statement.
    
        :param libraries: The libraries to be imported.
        """
        self.libraries = libraries
        super().__init__(self.libraries)

    def __str__(self):
        return f"Import statement.\nLibraries: {self.libraries}"

    def __repr__(self):
        return f"ASTImportStatementNode(libraries={self.libraries})"

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
        self.variables = variables
        super().__init__(self.variables)

    def __str__(self):
        return f"Global variable(s) declaration.\nVariables: {self.variables}"

    def __repr__(self):
        return f"ASTGlobalStatementNode(variables={self.variables})"

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
        self.variables = variables
        super().__init__(self.variables)

    def __str__(self):
        return f"Non-local variable(s) declaration.\nVariables: {self.variables}"

    def __repr__(self):
        return f"ASTNonLocalStatementNode(variable={self.variables})"

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
        self.condition = condition
        self.message = message
        super().__init__(self.condition, self.message)

    def __str__(self):
        return f"Assert statement.\nCondition: {self.condition}\nMessage: {self.message}"

    def __repr__(self):
        return f"ASTAssertStatementNode(condition={self.condition}, message={self.message})"

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

    def __init__(self, condition: ASTNode, body: Optional[ASTNode] = None):
        """
        If statement.
        
        :param condition: The condition to check.
        :param body: The code to execute if the condition is met.
        """
        self.condition = condition
        self.body = body
        super().__init__(self.condition, self.body)

    def __str__(self):
        return f"If statement.\nCondition: {self.condition}\nBody: {self.body}"

    def __repr__(self):
        return f"ASTIfStatementNode(condition={self.condition}, body={self.body})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_if_statement method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_if_statement(self)


class ASTIfElseStatementNode(ASTStatementNode):
    """
    If-else statement.
    """

    def __init__(self, condition: ASTNode, body: ASTNode, else_body: ASTNode):
        """
        If-else statement.

        :param condition: The condition to check.
        :param body: The code to execute if the condition is met.
        :param else_body: The code to execute if the condition is not met.
        """
        self.condition = condition
        self.body = body
        self.else_body = else_body
        super().__init__(self.condition, self.body, self.else_body)

    def __str__(self):
        return f"If-else statement.\nCondition: {self.condition}\nBody: {self.body}, Else body: {self.else_body}"

    def __repr__(self):
        return f"ASTIfElseStatementNode(condition={self.condition}, body={self.body}, else_body={self.else_body})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_if_else_statement method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_if_else_statement(self)


class ASTLoopStatementNode(ASTStatementNode):
    """
    Loop statement.
    """

    def __init__(self, condition: ASTNode, body: Optional[ASTNode] = None):
        """
        Loop statement.

        :param condition: The condition to check.
        :param body: The code to execute while the condition is met.
        """
        self.condition = condition
        self.body = body
        super().__init__(self.condition, self.body)

    def __str__(self):
        return f"Loop statement.\nCondition: {self.condition}\nBody: {self.body}"

    def __repr__(self):
        return f"ASTLoopStatementNode(condition={self.condition}, body={self.body})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_loop_statement method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_loop_statement(self)


class ASTLoopElseStatementNode(ASTStatementNode):
    """
    Loop-else statement.
    """

    def __init__(self, condition: ASTNode, body: ASTNode, else_body: ASTNode):
        """
        Loop-else statement.

        :param condition: The condition to check.
        :param body: The code to execute while the condition is met.
        :param else_body: The code to execute when the condition is not met.
        """
        self.condition = condition
        self.body = body
        self.else_body = else_body
        super().__init__(self.condition, self.body, self.else_body)

    def __str__(self):
        return f"Loop-else statement.\nCondition: {self.condition}\nBody: {self.body}\nElse body: {self.else_body}"

    def __repr__(self):
        return f"ASTLoopElseStatementNode(condition={self.condition}, body={self.body}, else_body={self.else_body})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_loop_else_statement method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_loop_else_statement(self)


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
        self.body = body
        self.catches = catches
        self.else_body = else_body
        self.finally_ = finally_
        super().__init__(self.body, self.catches, self.else_body, self.finally_)

    def __str__(self):
        return f"Try statement.\nBody: {self.body}\nCatches: {self.catches}\nElse body: {self.else_body}" \
               f"\nFinally: {self.finally_}"

    def __repr__(self):
        return f"ASTTryStatementNode(body={self.body}, catches={self.catches}, else_body={self.else_body}, " \
               f"finally_={self.finally_})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_try_statement method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_try_statement(self)


class ASTCatchNode(ASTNode):
    """
    Catch clause.
    """

    def __init__(self, exceptions: Optional[ASTNode] = None, body: Optional[ASTNode] = None):
        """
        Catch clause.

        :param exceptions: The exception(s) to catch.
        :param body: The code to execute if the specified exception(s) are thrown in the corresponding try block.
        """
        self.exceptions = exceptions
        self.body = body
        super().__init__(self.exceptions, self.body)

    def __str__(self):
        return f"Catch clause.\nExceptions: {self.exceptions}\n Body: {self.body}"

    def __repr__(self):
        return f"ASTCatchNode(exceptions={self.exceptions}, body={self.body})"

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
        self.body = body
        super().__init__(self.body)

    def __str__(self):
        return f"Finally clause.\nBody: {self.body}"

    def __repr__(self):
        return f"ASTFinallyNode(body={self.body})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_finally method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_finally(self)


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
        self.expressions = expressions
        self.body = body
        super().__init__(self.expressions, self.body)

    def __str__(self):
        return f"With statement.\nExpressions: {self.expressions}\nBody: {self.body}"

    def __repr__(self):
        return f"ASTWithStatementNode(expressions={self.expressions}, body={self.body})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_with_statement method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_with_statement(self)


class ASTFunctionDefinitionNode(ASTStatementNode):
    """
    Function definition.
    """

    def __init__(self, name, parameters: Optional[ASTNode] = None, return_type: Optional[ASTNode] = None,
                 body: Optional[ASTNode] = None, modifiers: Optional[Sequence[ASTModifier]] = None):
        """
        Function definition.

        :param name: The name of the function.
        :param parameters: The parameter(s) of the function.
        :param return_type: The return type of the function.
        :param body: The body of the function.
        :param modifiers: The modifier(s) applied to the function.
        """
        self.name = name
        self.parameters = parameters
        self.return_type = return_type
        self.body = body
        self.modifiers = modifiers if modifiers is not None else []
        super().__init__(self.name, self.parameters, self.return_type, self.body)

    def __str__(self):
        return f"Function definition.\nName: {self.name}\nParameters: {self.parameters}\n" \
               f"Return type: {self.return_type}\nBody: {self.body}\nModifiers: {self.modifiers}"

    def __repr__(self):
        return f"ASTFunctionDefinitionNode(name={self.name}, parameters={self.parameters}, " \
               f"return_type={self.return_type}, body={self.body}, modifiers={self.modifiers})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_function_definition method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_function_definition(self)


class ASTClassDefinitionNode(ASTStatementNode):
    """
    Class definition.
    """

    def __init__(self, name: ASTNode, arguments: Optional[ASTNode] = None, body: Optional[ASTNode] = None,
                 modifiers: Optional[Sequence[ASTModifier]] = None):
        """
        Class definition.

        :param name: The name of the class.
        :param arguments: The argument(s) of the class.
        :param body: The body of the class.
        :param modifiers: The modifier(s) applied to the class.
        """
        self.name = name
        self.body = body
        self.arguments = arguments
        self.modifiers = modifiers if modifiers is not None else []
        super().__init__(self.name, self.arguments, self.body)

    def __str__(self):
        return f"Class definition\nName: {self.name}\nArguments: {self.arguments}\n" \
               f"Body: {self.body}\nModifiers: {self.modifiers}"

    def __repr__(self):
        return f"ASTClassDefinitionNode(name={self.name}, arguments={self.arguments}, " \
               f"body={self.body}, modifiers={self.modifiers})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_class_definition method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_class_definition(self)


class ASTYieldExpressionNode(ASTNode):
    """
    Yield expression.
    """

    def __init__(self, values: Optional[ASTNode] = None):
        """
        Yield expression.

        :param values: The value(s) being yielded.
        """
        self.values = values
        super().__init__(self.values)

    def __str__(self):
        return f"Yield expression.\nValues: {self.values}"

    def __repr__(self):
        return f"ASTYieldExpressionNode(values={self.values})"

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

    def __init__(self, operation: Union[
        ASTArithmeticOperation, ASTLogicalOperation, ASTComparisonOperation, ASTBitwiseOperation],
                 left_operand: ASTNode, right_operand: ASTNode):
        """
        Binary operation.

        :param operation: The operation being performed.
        :param left_operand: The left-hand operand of the operation.
        :param right_operand: The right-hand operand of the operation.
        """
        self.operation = operation
        self.left_operand = left_operand
        self.right_operand = right_operand
        super().__init__(self.left_operand, self.right_operand)

    def __str__(self):
        return f"Binary operation.\nOperation: {self.operation}\nLeft operand: {self.left_operand}" \
               f"\nRight operand: {self.right_operand}"

    def __repr__(self):
        return f"ASTBinaryOperationNode(operation={self.operation}, left_operand={self.left_operand}, " \
               f"right_operand={self.right_operand})"

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

    def __init__(self, operation: Union[ASTArithmeticOperation, ASTLogicalOperation, ASTBitwiseOperation],
                 operand: ASTNode):
        """
        Unary operation.

        :param operation: The operation being performed.
        :param operand: The operand of the operation.
        """
        self.operation = operation
        self.operand = operand
        super().__init__(self.operand)

    def __str__(self):
        return f"Unary operation.\nOperation: {self.operation}\nOperand: {self.operand}"

    def __repr__(self):
        return f"ASTUnaryOperationNode(operation={self.operation}, operand={self.operand})"

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
        self.target = target
        self.alias = alias
        super().__init__(self.target, self.alias)

    def __str__(self):
        return f"Alias assignment.\nTarget: {self.target}\nAlias: {self.alias}"

    def __repr__(self):
        return f"ASTAliasNode(target={self.target}, alias={self.alias})"

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
        self.source = source
        self.expressions = expressions
        super().__init__(self.source, self.expressions)

    def __str__(self):
        return f"\"From\" expression.\nSource: {self.source}\nExpressions: {self.expressions}"

    def __repr__(self):
        return f"ASTFromNode(source={self.source}, expressions={self.expressions})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_from method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_from(self)


class ASTParameterNode(ASTNode):
    """
    Parameter.
    """

    def __init__(self, name: ASTNode, type_: Optional[ASTNode] = None, default: Optional[ASTNode] = None):
        """
        Parameter.

        :param name: The name of the parameter.
        :param type_: The parameter's type.
        :param default: The default value of the parameter.
        """
        self.name = name
        self.type = type_
        self.default = default
        super().__init__(self.name, self.type, self.default)

    def __str__(self):
        return f"Parameter.\nName: {self.name}\nType: {self.type}\nDefault: {self.default}"

    def __repr__(self):
        return f"ASTParameterNode(name={self.name}, type={self.type}, default={self.default})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_parameter method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_parameter(self)


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
        self.body = body
        self.parameters = parameters
        super().__init__(self.parameters, self.body)

    def __str__(self):
        return f"Anonymous function definition.\nBody: {self.body}\nParameters: {self.parameters}"

    def __repr__(self):
        return f"ASTAnonymousFunctionDefinitionNode(body={self.body}, parameters={self.parameters})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_anonymous_function_definition method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_anonymous_function_definition(self)


class ASTPositionalArgumentsParameterNode(ASTNode):
    """
    Positional arguments parameter.
    """

    def __init__(self, name: ASTNode, type_: Optional[ASTNode] = None):
        """
        Positional arguments parameter.

        :param name: The name of the parameter.
        :param type_: The type of all positional arguments supplied using the parameter.
        """
        self.name = name
        self.type = type_
        super().__init__(self.name, self.type)

    def __str__(self):
        return f"Positional arguments parameter.\nName: {self.name}\nType: {self.type}"

    def __repr__(self):
        return f"ASTPositionalArgumentsParameterNode(name={self.name}, type={self.type})"

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
        self.name = name
        self.type = type_
        super().__init__(self.name, self.type)

    def __str__(self):
        return f"Keyword arguments parameter.\nName: {self.name}\n Type: {self.type}"

    def __repr__(self):
        return f"ASTKeywordArgumentsParameterNode(name={self.name}, type={self.type})"

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
        self.expression = expression
        super().__init__(self.expression)

    def __str__(self):
        return f"Positional unpack expression.\nExpression: {self.expression}"

    def __repr__(self):
        return f"ASTPositionalUnpackExpressionNode(expressions={self.expression})"

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
        self.expression = expression
        super().__init__(self.expression)

    def __str__(self):
        return f"Keyword unpack expression.\nExpression: {self.expression}"

    def __repr__(self):
        return f"ASTKeywordUnpackExpressionNode(expressions={self.expression})"

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
        self.target = target
        super().__init__(self.target)

    def __str__(self):
        return f"Async declaration.\nTarget: {self.target}"

    def __repr__(self):
        return f"ASTAsyncNode(target={self.target}"

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
        self.expression = expression
        super().__init__(self.expression)

    def __str__(self):
        return f"Await expression.\nExpression: {self.expression}"

    def __repr__(self):
        return f"ASTAwaitNode(expression={self.expression})"

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
        self.parent = parent
        self.member = member
        super().__init__(self.parent, self.member)

    def __str__(self):
        return f"Member access.\nParent: {self.parent}\nMember: {self.member}"

    def __repr__(self):
        return f"ASTMemberNode(parent={self.parent}, member={self.member})"

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

    def __init__(self, sequence: ASTNode, subscripts: ASTNode):
        """
        Access.

        :param sequence: The sequence to access.
        :param subscripts: The subscript(s) defining which elements to access.
        """
        self.sequence = sequence
        self.subscripts = subscripts
        super().__init__(self.sequence, self.subscripts)

    def __str__(self):
        return f"Sequence element(s) access.\nSequence: {self.sequence}\nSubscripts: {self.subscripts}"

    def __repr__(self):
        return f"ASTAccessNode(sequence={self.sequence}, subscripts={self.subscripts})"

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
        self.index = index
        super().__init__(self.index)

    def __str__(self):
        return f"Sequence single element access.\nIndex: {self.index}"

    def __repr__(self):
        return f"ASTIndexNode(index={self.index})"

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
        self.start = start
        self.stop = stop
        self.step = step
        super().__init__(self.start, self.stop, self.step)

    def __str__(self):
        return f"Sequence slice access.\nStart: {self.start}\nStop: {self.stop}\nStep: {self.step}"

    def __repr__(self):
        return f"ASTSliceNode(start={self.start}, stop={self.stop}, step={self.step})"

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
        self.function = function
        self.arguments = arguments
        super().__init__(self.function, self.arguments)

    def __str__(self):
        return f"Method/function call.\nFunction: {self.function}\nArguments: {self.arguments}"

    def __repr__(self):
        return f"ASTCallNode(function={self.function}, arguments={self.arguments})"

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

    def __init__(self, value: ASTNode):
        """
        Argument.

        :param value: The value being passed in as the argument.
        """
        self.value = value
        super().__init__(self.value)

    def __str__(self):
        return f"Argument.\nValue: {self.value}"

    def __repr__(self):
        return f"ASTArgumentNode(value={self.value})"

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

    def __init__(self, parameter: ASTNode, value: ASTNode):
        """
        Keyword argument.

        :param parameter: The parameter to assign the value to.
        :param value: The value being passed in as the argument.
        """
        self.parameter = parameter
        self.value = value
        super().__init__(self.parameter, self.value)

    def __str__(self):
        return f"Keyword argument.\nParameter: {self.parameter}\nValue: {self.value}"

    def __repr__(self):
        return f"ASTKeywordArgumentNode(parameter={self.parameter}, value={self.value})"

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
        self.expression = expression
        super().__init__(self.expression)

    def __str__(self):
        return f"Generator expression.\nExpression: {self.expression}"

    def __repr__(self):
        return f"ASTGeneratorExpressionNode(expression={self.expression})"

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
        self.value = value
        self.loop = loop
        super().__init__(self.value, self.loop)

    def __str__(self):
        return f"Comprehension expression.\nValue: {self.value}\nLoop: {self.loop}"

    def __repr__(self):
        return f"ASTComprehensionNode(value={self.value}, loop={self.loop})"

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
        self.elements = elements
        super().__init__(self.elements)

    def __str__(self):
        return f"List declaration.\nElements: {self.elements}"

    def __repr__(self):
        return f"ASTListNode(elements={self.elements})"

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
        self.elements = elements
        super().__init__(self.elements)

    def __str__(self):
        return f"Tuple declaration.\nElements: {self.elements}"

    def __repr__(self):
        return f"ASTTupleNode(elements={self.elements})"

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
        self.elements = elements
        super().__init__(self.elements)

    def __str__(self):
        return f"Set declaration.\nElements: {self.elements}"

    def __repr__(self):
        return f"ASTSetNode(elements={self.elements})"

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
        self.elements = elements
        super().__init__(self.elements)

    def __str__(self):
        return f"Map declaration.\nElements: {self.elements}"

    def __repr__(self):
        return f"ASTMapNode(elements={self.elements})"

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
        self.key = key
        self.value = value
        super().__init__(self.key, self.value)

    def __str__(self):
        return f"Key-value pair.\nKey: {self.key}\nValue: {self.value}"

    def __repr__(self):
        return f"ASTKeyValuePairNode(key={self.key}, value={self.value})"

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
        self.decorators = decorators
        self.target = target
        super().__init__(self.decorators, self.target)

    def __str__(self):
        return f"Decorated statement.\nDecorators: {self.decorators}\nTarget: {self.target}"

    def __repr__(self):
        return f"ASTDecoratedNode(decorators={self.decorators}, target={self.target})"

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
        self.name = name
        self.arguments = arguments
        super().__init__(self.name, self.arguments)

    def __str__(self):
        return f"Decorator.\nName: {self.name}\nArguments: {self.arguments}"

    def __repr__(self):
        return f"ASTDecoratorNode(name={self.name}, arguments={self.arguments})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_decorator method.

        :param visitor: The AST visitor to accept.
        :return: The result of the visit.
        """
        return visitor.visit_decorator(self)


# Enums

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
    POSITIVE = "Positive"
    NEGATION = "Negation (Arithmetic)"


class ASTBitwiseOperation(ASTOperation):
    """
    Bitwise operations enum.
    """

    AND = "Bitwise And"
    BITWISE_OR = "Bitwise Or"
    BITWISE_XOR = "Bitwise Xor"
    LEFT_SHIFT = "Bitwise Left Shift"
    RIGHT_SHIFT = "Bitwise Right Shift"
    INVERSION = "Bitwise Inversion"


class ASTLogicalOperation(ASTOperation):
    """
    Logical operations enum.
    """
    AND = "Logical And"
    OR = "Logical Or"
    NOT = "Negation (Logical)"


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


class ASTAccessModifier(ASTModifier):
    """
    Access modifiers enum.
    """

    PRIVATE = "Private"
    INTERNAL = "Internal"
    PROTECTED = "Protected"
    PUBLIC = "Public"


class ASTMiscModifier(ASTModifier):
    """
    Miscellaneous modifiers enum.
    """
    ABSTRACT = "Abstract"
    ASYNC = "Async"
    EVENT = "Event"
    CONST = "Const"
    EXTERN = "Extern"
    NEW = "New"
    OVERRIDE = "Override"
    PARTIAL = "Partial"
    READONLY = "Read-only"
    SEALED = "Sealed"
    STATIC = "Static"
    UNSAFE = "Unsafe"
    VIRTUAL = "Virtual"
    VOLATIOLE = "Volatile"


# Literal Enums

class ASTLiteralType(ASTEnum):
    """
    Literal types enum.
    """

    NUMBER = "Number"
    STRING = "String"
    BOOLEAN = "Boolean"
    NULL = "Null"
    ELLIPSIS = "Ellipsis"
