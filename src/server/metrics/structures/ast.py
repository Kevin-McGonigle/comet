from metrics.structures.base.tree import *


class AST(Tree):
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


class ASTNode(Node):
    def accept(self, visitor):
        """
        Accept AST visitor.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the accept.
        :rtype: Any
        """
        return super().accept(visitor)


# Terminal

class ASTTerminalNode(ASTNode):
    def __init__(self, text):
        """
        Terminal.
        :param text: The terminal's text.
        :type text: str
        """
        self.text = text
        super().__init__(self.text)

    def accept(self, visitor):
        return self.text


# Multiples

class ASTMultiNode(ASTNode):
    def __init__(self, _type, first, remaining):
        """
        Base class for representing multiples of certain components.
        :param _type: The type of each member of the series.
        :type _type: str
        :param first: The first member in the series.
        :type first: ASTNode or str
        :param remaining: The remaining members in the series.
        :type remaining: ASTNode or str
        """
        self.name = _type
        self.first = first
        self.remaining = remaining
        super().__init__(_type, self.first, self.remaining)


class ASTStatementsNode(ASTMultiNode):
    def __init__(self, first, remaining=None):
        """
        Representation of multiple, consecutive statements.
        :param first: The first statement in the series of statements.
        :type first: ASTStatementNode
        :param remaining: The remaining statement(s) in the series of statements.
        :type remaining: ASTStatementsNode or ASTStatementNode
        """
        super().__init__("Statements", first, remaining)

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
        :type first: ASTNode or str
        :param remaining: The remaining expression(s) in the series of expressions.
        :type remaining: ASTNode or str
        """
        super().__init__("Expressions", first, remaining)

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
        :type first: ASTNode or str
        :param remaining: The remaining element(s) in the series of elements.
        :type remaining: ASTNode or str
        """
        super().__init__("Elements", first, remaining)

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
        :type first: ASTNode or str
        :param remaining: The remaining parameter(s) in the series of parameters.
        :type remaining: ASTNode or str
        """
        super().__init__("Parameters", first, remaining)

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
        :type first: ASTNode or str
        :param remaining: The remaining argument(s) in the series of arguments.
        :type remaining: ASTNode or str
        """
        super().__init__("Arguments", first, remaining)

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
        :type first: ASTNode or str
        :param remaining: The remaining subscript(s) in the series of subscripts.
        :type remaining: ASTNode or str
        """
        super().__init__("Subscripts", first, remaining)

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
        :type first: ASTNode or str
        :param remaining: The remaining catch statement(s) in the series of catch statements.
        :type remaining: ASTNode or str
        """
        super().__init__("Catch Statements", first, remaining)

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
        :type first: ASTNode or str
        :param remaining: The remaining decorator(s) in the series of decorators.
        :type remaining: ASTNode or str
        """
        super().__init__("Decorators", first, remaining)

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
    pass


class ASTDelStatementNode(ASTStatementNode):
    def __init__(self, expressions):
        """
        Delete statement.
        :param expressions: The expressions to be deleted.
        :type expressions: ASTNode or str
        """
        self.expressions = expressions
        super().__init__("Del", self.expressions)

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
    def __init__(self, variables=None, values=None):
        """
        Standard variable assignment statement.
        :param variables: The variable(s) to be assigned to.
        :type variables: ASTNode or str
        :param values: The value(s) to assign.
        :type values: ASTNode or str
        """
        self.variables = variables
        self.values = values
        super().__init__("Assignment", self.variables, self.values)

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
        :type variables: ASTNode or str
        :param values: The value(s) being assigned.
        :type values: ASTNode or str
        """
        self.operation = operation
        self.variables = variables
        self.values = values
        super().__init__(self.operation, self.variables, self.values)

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
    def __init__(self, annotation, variables=None, values=None):
        """
        Annotated assignment statement.
        :param annotation: The annotation for the variable(s).
        :type annotation: ASTNode or str
        :param variables: The variable(s) being assigned to.
        :type variables: ASTNode or str
        :param values: The value(s) being assigned
        :type values:
        """
        self.annotation = annotation
        self.variables = variables
        self.values = values
        super().__init__("Annotation Assignment", self.variables, self.annotation, self.values)

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
        :type values: ASTNode or str
        """
        self.value = values
        super().__init__("Yield", self.value)

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
        super().__init__("Pass")

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
        super().__init__("Break")

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
        super().__init__("Continue")

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
        :type values: ASTNode or str
        """
        self.expression = values
        super().__init__("Return", self.expression)

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
        :type exception: ASTNode or str
        """
        self.exception = exception
        super().__init__("Throw", self.exception)

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
        :param libraries: The library to be imported.
        :type libraries: ASTNode or str
        """
        self.libraries = libraries
        super().__init__("Import", self.libraries)

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
        :type variables: ASTNode or str
        """
        self.variables = variables
        super().__init__("Global", self.variables)

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
        Non-local variable declaration.
        :param variables: The nonlocal variable(s) being declared.
        :type variables: ASTNode or str
        """
        self.variables = variables
        super().__init__("Non-Local", self.variables)

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
        :type condition: ASTNode or str
        :param message: The message for the error raised should the assertion fail.
        :type message: ASTNode or str
        """
        self.condition = condition
        self.message = message
        super().__init__("Assert", self.condition, self.message)

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
    def __init__(self, condition, body=None):
        """
        If statement.
        :param condition: The condition to check.
        :type condition: ASTNode or str
        :param body: The code to execute if the condition is met.
        :type body: ASTNode or str or None
        """
        self.condition = condition
        self.body = body
        super().__init__("If", self.condition, self.body)

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
        :type condition: ASTNode or str
        :param body: The code to execute if the condition is met.
        :type body: ASTNode or str
        :param else_body: The code to execute if the condition is not met.
        :type else_body: ASTNode or str
        """
        self.condition = condition
        self.body = body
        self.else_body = else_body
        super().__init__("If-Else", self.condition, self.body, self.else_body)

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
        :type condition: ASTNode or str
        :param body: The code to execute while the condition is met.
        :type body: ASTNode or str or None
        """
        self.condition = condition
        self.body = body
        super().__init__("While", self.condition, self.body)

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
        :type condition: ASTNode or str
        :param body: The code to execute while the condition is met.
        :type body: ASTNode or str
        :param else_body: The code to execute when the condition is not met.
        :type else_body: ASTNode or str
        """
        self.condition = condition
        self.body = body
        self.else_body = else_body
        super().__init__("While-Else", self.condition, self.body, self.else_body)

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
    def __init__(self, body, catches=None, else_body=None, _finally=None):
        """
        Try statement.
        :param body: The code to try.
        :type body: ASTNode or str
        :param catches: The catch clause(s).
        :type catches: ASTNode or str
        :param else_body: The code to execute if the control flow leaves the try block, no exception was raised, and no
        return, continue, or break statement was executed.
        :type else_body: ASTNode or str
        :param _finally: The finally clause.
        :type _finally: ASTNode or str
        """
        self.body = body
        self.catches = catches
        self._else = else_body
        self._finally = _finally
        super().__init__("Try", self.body, *self.catches, self._else, self._finally)

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
        :type expressions: ASTNode or str
        :param body: The code to execute within the established runtime context.
        :type body: ASTNode or str
        """
        self.expressions = expressions
        self.body = body
        super().__init__("With", self.expressions, self.body)

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
    def __init__(self, name, body, parameters=None, return_type=None):
        """
        Function definition.
        :param name: The name of the function.
        :type name: ASTNode or str
        :param body: The body of the function.
        :type body: ASTNode or str
        :param parameters: The parameter(s) of the function.
        :type parameters: ASTNode or str
        :param return_type: The return type of the function.
        :type return_type: ASTNode or str
        """
        self.name = name
        self.body = body
        self.parameters = parameters
        self.return_type = return_type
        super().__init__("Function Definition", self.name, self.parameters, self.return_type, self.body)

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
    def __init__(self, name, body, arguments=None):
        """
        Class definition.
        :param name: The name of the class.
        :type name: ASTNode or str
        :param body: The body of the class.
        :type body: ASTNode or str
        :param arguments: The argument(s) of the class.
        :type arguments: ASTNode or str
        """
        self.name = name
        self.body = body
        self.arguments = arguments
        super().__init__("Class Definition", self.name, self.arguments, self.body)

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
    def __init__(self, value=None):
        """
        Yield expression.
        :param value: The expression(s) to yield.
        :type value: ASTNode
        """
        self.value = value
        super().__init__("Yield", self.value)

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
        :type exceptions: ASTNode or str
        :param body: The code to execute if the specified exception(s) are thrown in the corresponding try block.
        :type body: ASTNode or str
        """
        self.exception = exceptions
        self.body = body
        super().__init__("Catch", self.exception, self.body)

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
    def __init__(self, body):
        """
        Finally clause.
        :param body: The code to execute after all corresponding try, catch and else blocks,
        regardless of exceptions thrown.
        :type body:
        """
        self.body = body
        super().__init__("Finally", self.body)

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
        :type left_operand: ASTNode or str
        :param right_operand: The right-hand operand of the operation.
        :type right_operand: ASTNode or str
        """
        self.left_operand = left_operand
        self.right_operand = right_operand
        super().__init__(operation, self.left_operand, self.right_operand)

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
        Initialise a unary operation node.
        :param operation: The operation being performed.
        :type operation: str
        :param operand: The operand of the operation.
        :type operand: ASTNode or str
        """
        self.operation = operation
        self.operand = operand
        super().__init__(self.operation, self.operand)

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
        :type expression: ASTNode or str
        :param alias: The alias to be assigned
        :type alias: ASTNode or str
        """
        self.expression = expression
        self.alias = alias
        super().__init__("As", self.expression, self.alias)

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
        :type target: ASTNode or str
        """
        self.child = target
        super().__init__("Async", self.child)

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
    def __init__(self, name, _type=None, default=None):
        """
        Function parameter.
        :param name: The name of the parameter.
        :type name: str
        :param _type: The parameter's type.
        :type _type: ASTNode or str
        :param default: The default value of the parameter.
        :type default: ASTNode or str
        """
        self.name = name
        self.type = _type
        self.default = default
        super().__init__("Parameter", self.name, self.type, self.default)

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
    def __init__(self, name, _type=None):
        """
        Positional arguments parameter.
        :param name: The name of the parameter.
        :type name: str
        :param _type: The type of all positional arguments supplied using the parameter.
        :type _type: ASTNode or str
        """
        self.name = name
        self.type = _type
        super().__init__("Positional Arguments Parameter", self.name, self.type)

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
    def __init__(self, name, _type=None):
        """
        Keyword arguments parameter.
        :param name: The name of the parameter.
        :type name: str
        :param _type: The type of all keyword arguments supplied using the parameter.
        :type _type: ASTNode or str
        """
        self.name = name
        self.type = _type
        super().__init__("Keyword Arguments Parameter", self.name, self.type)

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
        :type source: ASTNode or str
        :param expressions: The expressions to take.
        :type expressions: ASTNode or str or None
        """
        self.source = source
        self.expressions = expressions
        super().__init__("From", self.source, self.expressions)

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
        :type body: ASTNode or str
        :param parameters: The parameter(s) of the function.
        :type parameters: ASTNode or str
        """
        self.body = body
        self.parameters = parameters
        super().__init__("Anonymous Function Definition", self.parameters, self.body)

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_anonymous_function_definition method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_anonymous_function_definition(self)


class ASTUnpackExpressionNode(ASTNode):
    def __init__(self, expression):
        """
        Unpack expression.
        :param expression: The expression to unpack.
        :type expression: ASTNode or str
        """
        self.expression = expression
        super().__init__("Unpack", self.expression)

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_unpack_expression method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_unpack_expression(self)


class ASTAwaitNode(ASTNode):
    def __init__(self, expression):
        """
        Await expression.
        :param expression: The expression to await.
        :type expression: ASTNode or str
        """
        self.expression = expression
        super().__init__("Await", self.expression)

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
        :type sequence: ASTNode or str
        :param subscripts: The subscript(s) defining which elements to access.
        :type subscripts: ASTNode or str
        """
        self.name = sequence
        self.subscript = subscripts
        super().__init__("Access", self.name, self.subscript)

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
        :type index: ASTNode or str
        """
        self.index = index
        super().__init__("Index", self.index)

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
        :type start: ASTNode or str
        :param stop: The index to slice up to.
        :type stop: ASTNode or str
        :param step: The step of the slice.
        :type step: ASTNode or str
        """
        self.start = start
        self.stop = stop
        self.step = step
        super().__init__("Slice", self.start, self.stop, self.step)

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
        Function call.
        :param function: The function being called.
        :type function: ASTNode or str
        :param arguments: The arguments being supplied to the function.
        :type arguments: ASTNode or str
        """
        self.name = function
        self.arguments = arguments
        super().__init__("Call", self.name, self.arguments)

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_call method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_call(self)


class ASTMemberNode(ASTNode):
    def __init__(self, parent, member):
        """
        Member access.
        :param parent: The member's parent.
        :type parent: ASTNode or str
        :param member: The member to access.
        :type member: ASTNode or  str
        """
        self.parent = parent
        self.child = member
        super().__init__("Member", self.parent, self.child)

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
        :type elements: ASTNode or str
        """
        self.elements = elements
        super().__init__("List", self.elements)

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
        :type elements: ASTNode or str
        """
        self.elements = elements
        super().__init__("Tuple", self.elements)

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
        :type expression: ASTNode or str
        """
        self.expression = expression
        super().__init__("Generator Expression", self.expression)

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
        :type value: ASTNode or str
        :param loop: The loop represented in the comprehension.
        :type loop: ASTNode or str
        """
        self.value = value
        self.loop = loop
        super().__init__("Comprehension", self.value, self.loop)

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
        :type elements: ASTNode or str
        """
        self.elements = elements
        super().__init__("Map", self.elements)

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
        :type elements: ASTNode or str
        """
        self.elements = elements
        super().__init__("Set", self.elements)

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
        :type key: ASTNode or str
        :param value: The value.
        :type value: ASTNode or str
        """
        self.key = key
        self.value = value
        super().__init__("Key-Value Pair", self.key, self.value)

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
        :type decorators: ASTNode or str
        :param target: The target that is decorated.
        :type target: ASTNode or str
        """
        self.decorators = decorators
        self.target = target
        super().__init__("Decorated", self.decorators, self.target)

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
        :type name: ASTNode or str
        :param arguments: The arguments supplied to the decorator.
        :type arguments: ASTNode or str
        """
        self.name = name
        self.arguments = arguments
        super().__init__("Decorator", self.name, self.arguments)

    def accept(self, visitor):
        """
        Accept AST visitor and call its visit_decorator method.
        :param visitor: The AST visitor to accept.
        :type visitor: ASTVisitor
        :return: The result of the visit.
        :rtype: Any
        """
        return visitor.visit_decorator(self)
