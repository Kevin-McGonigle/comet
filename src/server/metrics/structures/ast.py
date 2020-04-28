from typing import TYPE_CHECKING

from metrics.structures.base.graph import *

if TYPE_CHECKING:
    from metrics.visitors.base.ast_visitor import ASTVisitor


class AST(Graph):
    # Binary Operators
    ADD = "Add"
    SUBTRACT = "Subtract"
    MULTIPLY = "Multiply"
    DIVIDE = "Divide"
    FLOOR_DIVIDE = "Floor Divide"
    MODULO = "Modulo"
    POWER = "Power"
    BITWISE_AND = "Bitwise And"
    BITWISE_OR = "Bitwise Or"
    BITWISE_XOR = "Bitwise Xor"
    LEFT_SHIFT = "Left Shift"
    RIGHT_SHIFT = "Right Shift"
    MATRIX_MULTIPLY = "Matrix Multiply"

    # Unary Operators
    POSITIVE = "Positive"
    ARITH_NEGATION = "Negate (Arithmetic)"
    BITWISE_INVERSION = "Bitwise Inversion"

    # Logical Operators
    LOGICAL_AND = "Logical And"
    LOGICAL_OR = "Logical Or"
    LOGICAL_NEGATION = "Negate (Logical)"

    # Comparison Operators
    EQUAL = "Equal"
    NOT_EQUAL = "Not Equal"
    LESS_THAN = "Less Than"
    GREATER_THAN = "Greater Than"
    LESS_THAN_OR_EQUAL = "Less Than Or Equal"
    GREATER_THAN_OR_EQUAL = "Greater Than Or Equal"
    IN = "In"
    IS = "Is"

    # Augmented Assignment
    INPLACE_ADD = "In-Place Add"
    INPLACE_SUBTRACT = "In-Place Subtract"
    INPLACE_MULTIPLY = "In-Place Multiply"
    INPLACE_DIVIDE = "In-Place Divide"
    INPLACE_FLOOR_DIVIDE = "In-Place Floor Divide"
    INPLACE_MODULO = "In-Place Modulo"
    INPLACE_POWER = "In-Place Power"
    INPLACE_BITWISE_AND = "In-Place Bitwise And"
    INPLACE_BITWISE_OR = "In-Place Bitwise Or"
    INPLACE_BITWISE_XOR = "In-Place Bitwise Xor"
    INPLACE_LEFT_SHIFT = "In-Place Left Shift"
    INPLACE_RIGHT_SHIFT = "In_Place Right Shift"
    INPLACE_MATRIX_MULTIPLY = "In-Place Matrix Multiply"

    # Literal types
    NUMBER = "Number"
    STRING = "String"
    BOOLEAN = "Boolean"
    NULL = "Null"
    ELLIPSIS = "Ellipsis"

    def __init__(self, root=None):
        """
        Abstract syntax tree.
        :param root: The root node of the AST.
        :type root: ASTNode or None
        """
        super().__init__(root)

    def __str__(self):
        return f"Abstract syntax tree.\nRoot: {self.root}"

    def __repr__(self):
        return f"AST(root={self.root}"

    def accept(self, visitor):
        """
        Accept an AST visitor.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the accept.
        :rtype: Any
        """
        return super().accept(visitor)


class ASTNode(Node):
    def __init__(self, *children):
        """
        Generic abstract syntax tree node.
        :param children: The child nodes of the node.
        :type children: ASTNode or str
        """
        super().__init__(*children)

    def __str__(self):
        return f"Generic abstract syntax tree node.\nChildren: {self.children}"

    def __repr__(self):
        return f"ASTNode(children={self.children})"

    def accept(self, visitor):
        """
        Accept an AST visitor.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the accept.
        :rtype: Any
        """
        return super().accept(visitor)


# Terminals
class ASTTerminalNode(ASTNode):
    def __init__(self, *values):
        """
        Terminal node.
        :param values: The value(s) represented by the terminal node.
        :type values: str
        """
        super().__init__(*values)

    def __str__(self):
        return f"Terminal node.\nValues: {self.values}"

    def __repr__(self):
        return f"ASTTerminalNode(values={self.values})"

    @property
    def values(self):
        """
        Getter for values property.
        :return: The value(s) represented by the terminal node.
        :rtype: list[str]
        """
        return self.children

    @values.setter
    def values(self, new_values):
        """
        Setter for values property.
        :param new_values: The new value(s) to be represented by the terminal node.
        :type new_values: list[str]
        """
        self.children = new_values

    @values.deleter
    def values(self):
        """
        Deleter for values property.
        """
        del self.children

    def accept(self, visitor):
        """
        Accept an AST visitor and call its visit_terminal method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the accept.
        :rtype: Any
        """
        return visitor.visit_terminal(self)


class ASTIdentifierNode(ASTTerminalNode):
    def __init__(self, name):
        """
        Identifier.
        :param name: The name of the identifier.
        :type name: str
        """
        self.name = name
        super().__init__(self.name)

    def __str__(self):
        return f"Identifier.\nName: {self.name}"

    def __repr__(self):
        return f"ASTIdentifierNode(name={self.name})"

    def accept(self, visitor):
        """
        Accept an AST visitor and call its visit_identifier method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the accept.
        :rtype: Any
        """
        return visitor.visit_identifier(self)


class ASTLiteralNode(ASTTerminalNode):
    def __init__(self, type_, value=None):
        """
        Literal.
        :param type_: The type of literal.
        :type type_: str
        :param value: The value of the literal.
        :type value: str or None
        """
        self.type = type_
        self.value = value
        super().__init__(self.type, self.value)

    def __str__(self):
        return f"Literal.\nType: {self.type}\nValue: {self.value}"

    def __repr__(self):
        return f"ASTLiteralNode(type={self.type}, value={self.value})"

    def accept(self, visitor):
        """
        Accept an AST visitor and call its visit_literal method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the accept.
        :rtype: Any
        """
        return visitor.visit_literal(self)


# Multiples

class ASTMultiNode(ASTNode):
    def __init__(self, first, remaining):
        """
        Base class for representing a series of multiple, consecutive nodes.
        :param first: The first node in the series.
        :type first: ASTNode
        :param remaining: The remaining nodes in the series.
        :type remaining: ASTNode
        """
        self.first = first
        self.remaining = remaining
        super().__init__(self.first, self.remaining)

    def __str__(self):
        return f"Multiple, consecutive nodes (generic).\nFirst: {self.first}\nRemaining: {self.remaining}"

    def __repr__(self):
        return f"ASTMultiNode(first={self.first}, remaining={self.remaining})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_multi method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_multi(self)


class ASTStatementsNode(ASTMultiNode):
    def __init__(self, first, remaining):
        """
        Representation of multiple, consecutive statements.
        :param first: The first statement in the series of statements.
        :type first: ASTStatementNode
        :param remaining: The remaining statement(s) in the series of statements.
        :type remaining: ASTStatementsNode or ASTStatementNode
        """
        super().__init__(first, remaining)

    def __str__(self):
        return f"Multiple, consecutive statements.\nFirst: {self.first}\nRemaining: {self.remaining}"

    def __repr__(self):
        return f"ASTStatementsNode(first={self.first}, remaining={self.remaining})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_statements method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_statements(self)


class ASTExpressionsNode(ASTMultiNode):
    def __init__(self, first, remaining):
        """
        Representation of multiple, consecutive expressions.
        :param first: The first expression in the series of expressions.
        :type first: ASTNode
        :param remaining: The remaining expression(s) in the series of expressions.
        :type remaining: ASTNode
        """
        super().__init__(first, remaining)

    def __str__(self):
        return f"Multiple, consecutive expressions.\nFirst: {self.first}\nRemaining: {self.remaining}"

    def __repr__(self):
        return f"ASTExpressionsNode(first={self.first}, remaining={self.remaining})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_expressions method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_expressions(self)


class ASTElementsNode(ASTMultiNode):
    def __init__(self, first, remaining):
        """
        Representation of multiple, consecutive list, map or set elements.
        :param first: The first element in the series of elements.
        :type first: ASTNode
        :param remaining: The remaining element(s) in the series of elements.
        :type remaining: ASTNode
        """
        super().__init__(first, remaining)

    def __str__(self):
        return f"Multiple, consecutive list, map or set elements.\nFirst: {self.first}\nRemaining: {self.remaining}"

    def __repr__(self):
        return f"ASTElementsNode(first={self.first}, remaining={self.remaining})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_elements method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_elements(self)


class ASTParametersNode(ASTMultiNode):
    def __init__(self, first, remaining):
        """
        Representation of multiple, consecutive parameters.
        :param first: The first parameter in the series of parameters.
        :type first: ASTNode
        :param remaining: The remaining parameter(s) in the series of parameters.
        :type remaining: ASTNode
        """
        super().__init__(first, remaining)

    def __str__(self):
        return f"Multiple, consecutive parameters.\nFirst: {self.first}\nRemaining: {self.remaining}"

    def __repr__(self):
        return f"ASTParametersNode(first={self.first}, remaining={self.remaining})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_parameters method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_parameters(self)


class ASTArgumentsNode(ASTMultiNode):
    def __init__(self, first, remaining):
        """
        Representation of multiple, consecutive arguments.
        :param first: The first argument in the series of arguments.
        :type first: ASTNode
        :param remaining: The remaining argument(s) in the series of arguments.
        :type remaining: ASTNode
        """
        super().__init__(first, remaining)

    def __str__(self):
        return f"Multiple, consecutive arguments.\nFirst: {self.first}\nRemaining: {self.remaining}"

    def __repr__(self):
        return f"ASTArgumentsNode(first={self.first}, remaining={self.remaining})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_arguments method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_arguments(self)


class ASTSubscriptsNode(ASTMultiNode):
    def __init__(self, first, remaining):
        """
        Representation of multiple, consecutive subscripts.
        :param first: The first subscript in the series of subscripts.
        :type first: ASTNode
        :param remaining: The remaining subscript(s) in the series of subscripts.
        :type remaining: ASTNode
        """
        super().__init__(first, remaining)

    def __str__(self):
        return f"Multiple, consecutive subscripts.\nFirst: {self.first}\nRemaining: {self.remaining}"

    def __repr__(self):
        return f"ASTSubscriptsNode(first={self.first}, remaining={self.remaining})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_subscripts method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_subscripts(self)


class ASTCatchesNode(ASTMultiNode):
    def __init__(self, first, remaining):
        """
        Representation of multiple, consecutive catch statements.
        :param first: The first catch statement in the series of catch statements.
        :type first: ASTNode
        :param remaining: The remaining catch statement(s) in the series of catch statements.
        :type remaining: ASTNode
        """
        super().__init__(first, remaining)

    def __str__(self):
        return f"Multiple, consecutive catches.\nFirst: {self.first}\nRemaining: {self.remaining}"

    def __repr__(self):
        return f"ASTCatchesNode(first={self.first}, remaining={self.remaining})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_catches method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_catches(self)


class ASTDecoratorsNode(ASTMultiNode):
    def __init__(self, first, remaining):
        """
        Representation of multiple, consecutive decorators.
        :param first: The first decorator in the series of decorators.
        :type first: ASTNode
        :param remaining: The remaining decorator(s) in the series of decorators.
        :type remaining: ASTNode
        """
        super().__init__(first, remaining)

    def __str__(self):
        return f"Multiple, consecutive decorators.\nFirst: {self.first}\nRemaining: {self.remaining}"

    def __repr__(self):
        return f"ASTDecoratorsNode(first={self.first}, remaining={self.remaining})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_decorators method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_decorators(self)


# Statements
class ASTStatementNode(ASTNode):
    def __init__(self, *children):
        """
        Base class for representing a statement.
        :param children: The child nodes of the statement node.
        :type children: ASTNode
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_statement(self)


class ASTDelStatementNode(ASTStatementNode):
    def __init__(self, expressions):
        """
        Delete statement.
        :param expressions: The expressions to be deleted.
        :type expressions: ASTNode
        """
        self.expressions = expressions
        super().__init__(self.expressions)

    def __str__(self):
        return f"Delete statement.\nExpressions: {self.expressions}"

    def __repr__(self):
        return f"ASTDelStatementNode(expressions={self.expressions})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_del_statement method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_del_statement(self)


class ASTAssignmentStatementNode(ASTStatementNode):
    def __init__(self, variables, values):
        """
        Standard variable assignment statement.
        :param variables: The variable(s) to be assigned to.
        :type variables: ASTNode
        :param values: The value(s) to assign.
        :type values: ASTNode
        """
        self.variables = variables
        self.values = values
        super().__init__(self.variables, self.values)

    def __str__(self):
        return f"Standard variable assignment statement.\nVariables: {self.variables}\nValues: {self.values}"

    def __repr__(self):
        return f"ASTAssignmentStatementNode(variables={self.variables}, values={self.values}"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_assignment_statement method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_assignment_statement(self)


class ASTAugmentedAssignmentStatementNode(ASTStatementNode):
    def __init__(self, operation, variables, values):
        """
        Augmented (in-place) assignment statement.
        :param operation: The in-place operation being performed.
        :type operation: str
        :param variables: The variable(s) being assigned to.
        :type variables: ASTNode
        :param values: The value(s) being assigned.
        :type values: ASTNode
        """
        self.operation = operation
        self.variables = variables
        self.values = values
        super().__init__(self.variables, self.values)

    def __str__(self):
        return f"Augmented (in-place) assignment statement.\nOperation: {self.operation}\nVariables: {self.variables}" \
               f"\nValues: {self.values}"

    def __repr__(self):
        return f"ASTAugmentedAssignmentStatementNode(operation={self.operation}, variables={self.variables}, " \
               f"values={self.values})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_augmented_assignment_statement method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_augmented_assignment_statement(self)


class ASTAnnotatedAssignmentStatementNode(ASTStatementNode):
    def __init__(self, annotation, variables, values=None):
        """
        Annotated assignment statement.
        :param annotation: The annotation for the variable(s).
        :type annotation: ASTNode
        :param variables: The variable(s) being assigned to.
        :type variables: ASTNode
        :param values: The value(s) being assigned
        :type values: ASTNode or None
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_annotated_assignment_statement(self)


class ASTYieldStatementNode(ASTStatementNode):
    def __init__(self, values=None):
        """
        Yield statement.
        :param values: The value(s) being yielded.
        :type values: ASTNode
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_yield_statement(self)


class ASTPassStatementNode(ASTStatementNode):
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_pass_statement(self)


class ASTBreakStatementNode(ASTStatementNode):
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_break_statement(self)


class ASTContinueStatementNode(ASTStatementNode):
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_continue_statement(self)


class ASTReturnStatementNode(ASTStatementNode):
    def __init__(self, values=None):
        """
        Return statement.
        :param values: The value(s) being returned.
        :type values: ASTNode
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_return_statement(self)


class ASTThrowStatementNode(ASTStatementNode):
    def __init__(self, exception=None):
        """
        Throw statement.
        :param exception: The exception to be thrown.
        :type exception: ASTNode or None
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_throw_statement(self)


class ASTImportStatementNode(ASTStatementNode):
    def __init__(self, libraries):
        """
        Import statement.
        :param libraries: The libraries to be imported.
        :type libraries: ASTNode
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_import_statement(self)


class ASTGlobalStatementNode(ASTStatementNode):
    def __init__(self, variables):
        """
        Global variable(s) declaration.
        :param variables: The global variable(s) being declared.
        :type variables: ASTNode
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_global_statement(self)


class ASTNonLocalStatementNode(ASTStatementNode):
    def __init__(self, variables):
        """
        Non-local variable(s) declaration.
        :param variables: The nonlocal variable(s) being declared.
        :type variables: ASTNode
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_non_local_statement(self)


class ASTAssertStatementNode(ASTStatementNode):
    def __init__(self, condition, message=None):
        """
        Assert statement.
        :param condition: The condition to assert.
        :type condition: ASTNode
        :param message: The message for the error raised should the assertion fail.
        :type message: ASTNode or None
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_assert_statement(self)


class ASTIfStatementNode(ASTStatementNode):
    def __init__(self, condition, body):
        """
        If statement.
        :param condition: The condition to check.
        :type condition: ASTNode
        :param body: The code to execute if the condition is met.
        :type body: ASTNode
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_if_statement(self)


class ASTIfElseStatementNode(ASTStatementNode):
    def __init__(self, condition, body, else_body):
        """
        If-else statement.
        :param condition: The condition to check.
        :type condition: ASTNode
        :param body: The code to execute if the condition is met.
        :type body: ASTNode
        :param else_body: The code to execute if the condition is not met.
        :type else_body: ASTNode
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_if_else_statement(self)


class ASTLoopStatementNode(ASTStatementNode):
    def __init__(self, condition, body=None):
        """
        Loop statement.
        :param condition: The condition to check.
        :type condition: ASTNode
        :param body: The code to execute while the condition is met.
        :type body: ASTNode or None
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_loop_statement(self)


class ASTLoopElseStatementNode(ASTStatementNode):
    def __init__(self, condition, body, else_body):
        """
        Loop-else statement.
        :param condition: The condition to check.
        :type condition: ASTNode
        :param body: The code to execute while the condition is met.
        :type body: ASTNode
        :param else_body: The code to execute when the condition is not met.
        :type else_body: ASTNode
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_loop_else_statement(self)


class ASTTryStatementNode(ASTStatementNode):
    def __init__(self, body, catches=None, else_body=None, finally_=None):
        """
        Try statement.
        :param body: The code to try.
        :type body: ASTNode
        :param catches: The catch clause(s).
        :type catches: ASTNode or None
        :param else_body: The code to execute if the control flow leaves the try block, no exception was raised, and no
        return, continue, or break statement was executed.
        :type else_body: ASTNode or None
        :param finally_: The finally clause.
        :type finally_: ASTNode or None
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_try_statement(self)


class ASTWithStatementNode(ASTStatementNode):
    def __init__(self, expressions, body):
        """
        With statement.
        :param expressions: The expression(s) to evaluate to create a context manager.
        :type expressions: ASTNode
        :param body: The code to execute within the established runtime context.
        :type body: ASTNode
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_with_statement(self)


class ASTFunctionDefinitionNode(ASTStatementNode):
    def __init__(self, name, parameters=None, body=None, return_type=None):
        """
        Function definition.
        :param name: The name of the function.
        :type name: ASTNode
        :param parameters: The parameter(s) of the function.
        :type parameters: ASTNode or None
        :param body: The body of the function.
        :type body: ASTNode or None
        :param return_type: The return type of the function.
        :type return_type: ASTNode or None
        """
        self.name = name
        self.body = body
        self.parameters = parameters
        self.return_type = return_type
        super().__init__(self.name, self.parameters, self.return_type, self.body)

    def __str__(self):
        return f"Function definition.\nName: {self.name}\nParameters: {self.parameters}\nBody: {self.body}" \
               f"\nReturn type: {self.return_type}"

    def __repr__(self):
        return f"ASTFunctionDefinitionNode(name={self.name}, parameters={self.parameters}, body={self.body}, " \
               f"return_type={self.return_type})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_function_definition method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_function_definition(self)


class ASTClassDefinitionNode(ASTStatementNode):
    def __init__(self, name, arguments=None, body=None):
        """
        Class definition.
        :param name: The name of the class.
        :type name: ASTNode
        :param arguments: The argument(s) of the class.
        :type arguments: ASTNode or None
        :param body: The body of the class.
        :type body: ASTNode or None
        """
        self.name = name
        self.body = body
        self.arguments = arguments
        super().__init__(self.name, self.arguments, self.body)

    def __str__(self):
        return f"Class definition\nName: {self.name}\nArguments: {self.arguments}\nBody: {self.body}"

    def __repr__(self):
        return f"ASTClassDefinitionNode(name={self.name}, arguments={self.arguments}, body={self.body})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_class_definition method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_class_definition(self)


class ASTYieldExpressionNode(ASTNode):
    def __init__(self, values=None):
        """
        Yield expression.
        :param values: The value(s) being yielded.
        :type values: ASTNode
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_yield_expression(self)


class ASTCatchNode(ASTNode):
    def __init__(self, exceptions=None, body=None):
        """
        Catch clause.
        :param exceptions: The exception(s) to catch.
        :type exceptions: ASTNode or None
        :param body: The code to execute if the specified exception(s) are thrown in the corresponding try block.
        :type body: ASTNode or None
        """
        self.exceptions = exceptions
        self.body = body
        super().__init__("Catch", self.exceptions, self.body)

    def __str__(self):
        return f"Catch clause.\nExceptions: {self.exceptions}\n Body: {self.body}"

    def __repr__(self):
        return f"ASTCatchNode(exceptions={self.exceptions}, body={self.body})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_catch method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_catch(self)


class ASTFinallyNode(ASTNode):
    def __init__(self, body=None):
        """
        Finally clause.
        :param body: The code to execute after all corresponding try, catch and else blocks,
        regardless of exceptions thrown.
        :type body: ASTNode or  None
        """
        self.body = body
        super().__init__("Finally", self.body)

    def __str__(self):
        return f"Finally clause.\nBody: {self.body}"

    def __repr__(self):
        return f"ASTFinallyNode(body={self.body})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_finally method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_finally(self)


class ASTBinaryOperationNode(ASTNode):
    def __init__(self, operation, left_operand, right_operand):
        """
        Binary operation.
        :param operation: The operation being performed.
        :type operation: str
        :param left_operand: The left-hand operand of the operation.
        :type left_operand: ASTNode
        :param right_operand: The right-hand operand of the operation.
        :type right_operand: ASTNode
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_binary_operation(self)


class ASTUnaryOperationNode(ASTNode):
    def __init__(self, operation, operand):
        """
        Unary operation.
        :param operation: The operation being performed.
        :type operation: str
        :param operand: The operand of the operation.
        :type operand: ASTNode
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_unary_operation(self)


class ASTAsNode(ASTNode):
    def __init__(self, expression, alias):
        """
        "As" expression.
        :param expression: The expression to assign the alias to.
        :type expression: ASTNode
        :param alias: The alias to be assigned
        :type alias: ASTNode
        """
        self.expression = expression
        self.alias = alias
        super().__init__(self.expression, self.alias)

    def __str__(self):
        return f"\"As\" expression.\nExpression: {self.expression}\nAlias: {self.alias}"

    def __repr__(self):
        return f"ASTAsNode(expression={self.expression}, alias={self.alias})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_as method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_as(self)


class ASTAsyncNode(ASTNode):
    def __init__(self, target):
        """
        Async declaration.
        :param target: The code to be declared as asynchronous.
        :type target: ASTNode
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_async(self)


class ASTParameterNode(ASTNode):
    def __init__(self, name, type_=None, default=None):
        """
        Parameter.
        :param name: The name of the parameter.
        :type name: ASTTerminalNode
        :param type_: The parameter's type.
        :type type_: ASTNode or None
        :param default: The default value of the parameter.
        :type default: ASTNode or None
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_parameter(self)


class ASTPositionalArgumentsParameter(ASTNode):
    def __init__(self, name, type_=None):
        """
        Positional arguments parameter.
        :param name: The name of the parameter.
        :type name: ASTTerminalNode
        :param type_: The type of all positional arguments supplied using the parameter.
        :type type_: ASTNode
        """
        self.name = name
        self.type = type_
        super().__init__(self.name, self.type)

    def __str__(self):
        return f"Positional arguments parameter.\nName: {self.name}\nType: {self.type}"

    def __repr__(self):
        return f"ASTPositionalArgumentsParameter(name={self.name}, type={self.type})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_positional_arguments_parameter method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_positional_arguments_parameter(self)


class ASTKeywordArgumentsParameter(ASTNode):
    def __init__(self, name, type_=None):
        """
        Keyword arguments parameter.
        :param name: The name of the parameter.
        :type name: ASTTerminalNode
        :param type_: The type of all keyword arguments supplied using the parameter.
        :type type_: ASTNode
        """
        self.name = name
        self.type = type_
        super().__init__(self.name, self.type)

    def __str__(self):
        return f"Keyword arguments parameter.\nName: {self.name}\n Type: {self.type}"

    def __repr__(self):
        return f"ASTKeywordArgumentsParameter(name={self.name}, type={self.type})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_keyword_arguments_parameter method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_keyword_arguments_parameter(self)


class ASTFromNode(ASTNode):
    def __init__(self, source, expressions=None):
        """
        "From" expression.
        :param source: The source to take the expression(s) from.
        :type source: ASTNode
        :param expressions: The expressions to take.
        :type expressions: ASTNode or None
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_from(self)


class ASTAnonymousFunctionDefinitionNode(ASTNode):
    def __init__(self, body, parameters=None):
        """
        Anonymous function definition.
        :param body: The body of the anonymous function.
        :type body: ASTNode
        :param parameters: The parameter(s) of the function.
        :type parameters: ASTNode
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_anonymous_function_definition(self)


class ASTPositionalUnpackExpressionNode(ASTNode):
    def __init__(self, expression):
        """
        Positional unpack expression.
        :param expression: The expression to positionally unpack.
        :type expression: ASTNode
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_positional_unpack_expression(self)


class ASTKeywordUnpackExpressionNode(ASTNode):
    def __init__(self, expression):
        """
        Keyword unpack expression.
        :param expression: The expression to keyword-wise unpack.
        :type expression: ASTNode
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_keyword_unpack_expression(self)


class ASTAwaitNode(ASTNode):
    def __init__(self, expression):
        """
        Await expression.
        :param expression: The expression to await.
        :type expression: ASTNode
        """
        self.expression = expression
        super().__init__(self.expression)

    def __str__(self):
        return f"Await expression.\nExpression: {self.expression}"

    def __repr__(self):
        return f"ASTAwaitNode(expressions={self.expression})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_await method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_await(self)


class ASTAccessNode(ASTNode):
    def __init__(self, sequence, subscripts):
        """
        Sequence element(s) access.
        :param sequence: The sequence to access.
        :type sequence: ASTNode
        :param subscripts: The subscript(s) defining which elements to access.
        :type subscripts: ASTNode
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_access(self)


class ASTIndexNode(ASTNode):
    def __init__(self, index):
        """
        Sequence single element access.
        :param index: The index of the element to access.
        :type index: ASTNode
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_index(self)


class ASTSliceNode(ASTNode):
    def __init__(self, start, stop, step):
        """
        Sequence slice access.
        :param start: The index of the first element in the slice.
        :type start: ASTNode
        :param stop: The index to slice up to.
        :type stop: ASTNode
        :param step: The step of the slice.
        :type step: ASTNode
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_slice(self)


class ASTCallNode(ASTNode):
    def __init__(self, function, arguments=None):
        """
        Method/function call.
        :param function: The function being called.
        :type function: ASTNode
        :param arguments: The arguments being supplied to the function.
        :type arguments: ASTNode
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_call(self)


class ASTArgumentNode(ASTNode):
    def __init__(self, value):
        """
        Argument.
        :param value: The value being passed in as the argument.
        :type value: ASTNode
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_argument(self)


class ASTKeywordArgumentNode(ASTNode):
    def __init__(self, parameter, value):
        """
        Keyword argument.
        :param parameter: The parameter to assign the value to.
        :type parameter: ASTNode
        :param value: The value being passed in as the argument.
        :type value: ASTNode
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_keyword_argument(self)


class ASTMemberNode(ASTNode):
    def __init__(self, parent, member):
        """
        Member access.
        :param parent: The member's parent.
        :type parent: ASTNode
        :param member: The member to access.
        :type member: ASTNode
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_member(self)


class ASTListNode(ASTNode):
    def __init__(self, elements):
        """
        List declaration.
        :param elements: The elements of the list.
        :type elements: ASTNode
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
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_list(self)


class ASTTupleNode(ASTNode):
    def __init__(self, elements):
        """
        Tuple declaration.
        :param elements: The elements of the tuple.
        :type elements: ASTNode
        """
        self.elements = elements
        super().__init__("Tuple", self.elements)

    def __str__(self):
        return f"Tuple declaration.\nElements: {self.elements}"

    def __repr__(self):
        return f"ASTTupleNode(elements={self.elements})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_tuple method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_tuple(self)


class ASTGeneratorExpressionNode(ASTNode):
    def __init__(self, expression):
        """
        Generator expression.
        :param expression: The expression defining the generator.
        :type expression: ASTNode
        """
        self.expression = expression
        super().__init__("Generator Expression", self.expression)

    def __str__(self):
        return f"Generator expression.\nExpression: {self.expression}"

    def __repr__(self):
        return f"ASTGeneratorExpressionNode(expression={self.expression})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_generator_expression method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_generator_expression(self)


class ASTComprehensionNode(ASTNode):
    def __init__(self, value, loop):
        """
        Comprehension expression.
        :param value: The value to return from the loop.
        :type value: ASTNode
        :param loop: The loop represented in the comprehension.
        :type loop: ASTNode
        """
        self.value = value
        self.loop = loop
        super().__init__("Comprehension", self.value, self.loop)

    def __str__(self):
        return f"Comprehension expression.\nValue: {self.value}\nLoop: {self.loop}"

    def __repr__(self):
        return f"ASTComprehensionNode(value={self.value}, loop={self.loop})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_comprehension method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_comprehension(self)


class ASTMapNode(ASTNode):
    def __init__(self, elements):
        """
        Map declaration.
        :param elements: The elements of the map.
        :type elements: ASTNode
        """
        self.elements = elements
        super().__init__("Map", self.elements)

    def __str__(self):
        return f"Map declaration.\nElements: {self.elements}"

    def __repr__(self):
        return f"ASTMapNode(elements={self.elements})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_map method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_map(self)


class ASTSetNode(ASTNode):
    def __init__(self, elements):
        """
        Set declaration.
        :param elements: The elements of the set.
        :type elements: ASTNode
        """
        self.elements = elements
        super().__init__("Set", self.elements)

    def __str__(self):
        return f"Set declaration.\nElements: {self.elements}"

    def __repr__(self):
        return f"ASTSetNode(elements={self.elements})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_set method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_set(self)


class ASTKeyValuePairNode(ASTNode):
    def __init__(self, key, value):
        """
        Key-value pair.
        :param key: The key.
        :type key: ASTNode
        :param value: The value.
        :type value: ASTNode
        """
        self.key = key
        self.value = value
        super().__init__("Key-Value Pair", self.key, self.value)

    def __str__(self):
        return f"Key-value pair.\nKey: {self.key}\nValue: {self.value}"

    def __repr__(self):
        return f"ASTKeyValuePairNode(key={self.key}, value={self.value})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_key_value_pair method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_key_value_pair(self)


class ASTDecoratedNode(ASTNode):
    def __init__(self, decorators, target):
        """
        Decorated statement.
        :param decorators: The decorators applied to the target.
        :type decorators: ASTNode
        :param target: The target that is decorated.
        :type target: ASTNode
        """
        self.decorators = decorators
        self.target = target
        super().__init__("Decorated", self.decorators, self.target)

    def __str__(self):
        return f"Decorated statement.\nDecorators: {self.decorators}\nTarget: {self.target}"

    def __repr__(self):
        return f"ASTDecoratedNode(decorators={self.decorators}, target={self.target})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_decorated method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_decorated(self)


class ASTDecoratorNode(ASTNode):
    def __init__(self, name, arguments=None):
        """
        Decorator.
        :param name: The name of the decorator.
        :type name: ASTNode
        :param arguments: The arguments supplied to the decorator.
        :type arguments: ASTNode
        """
        self.name = name
        self.arguments = arguments
        super().__init__("Decorator", self.name, self.arguments)

    def __str__(self):
        return f"Decorator.\nName: {self.name}\nArguments: {self.arguments}"

    def __repr__(self):
        return f"ASTDecoratorNode(name={self.name}, arguments={self.arguments})"

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_decorator method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_decorator(self)
