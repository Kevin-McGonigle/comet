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
    pass


class ASTStatementsNode(ASTNode):
    def __init__(self, first_statement, next_statements=None):
        """
        Initialise a statements node.
        :param first_statement: The first statement in the series of statements.
        :type first_statement: ASTNode
        :param next_statements: The next statements node in the series.
        :type next_statements: ASTStatementsNode
        """
        self.first_statement = first_statement
        self.next_statements = next_statements
        super().__init__("Statements")

    def __str__(self):
        return super().__str__(self.first_statement, self.next_statements)


class ASTDelStatementNode(ASTNode):
    def __init__(self, expressions):
        """
        Initialise a delete statement node.
        :param expressions: The expressions to delete.
        :type expressions: ASTExpressionsNode
        """
        self.expressions = expressions
        super().__init__("Del")

    def __str__(self):
        return super().__str__(self.expressions)


class ASTExpressionsNode(ASTNode):
    def __init__(self, first_expression, next_expressions=None):
        """
        Initialise an expressions node.
        :param first_expression:
        :type first_expression:
        :param next_expressions:
        :type next_expressions:
        """
        self.first_expression = first_expression
        self.next_expressions = next_expressions
        super().__init__("Expressions")

    def __str__(self):
        return super().__str__(self.first_expression, self.next_expressions)


class ASTBinOpNode(ASTNode):
    def __init__(self, operation, left_operand, right_operand):
        """
        Initialise a binary operation node.
        :param operation: The operation being performed.
        :type operation: str
        :param left_operand: The left-hand operand of the operation.
        :type left_operand: ASTNode
        :param right_operand: The right-hand operand of the operation.
        :type right_operand: ASTNode
        """
        self.left_operand = left_operand
        self.right_operand = right_operand
        super().__init__(operation)

    def __str__(self):
        return super().__str__(self.left_operand, self.right_operand)


class ASTUnOpNode(ASTNode):
    def __init__(self, operation, operand):
        """
        Initialise a unary operation node.
        :param operation: The operation being performed.
        :type operation: str
        :param operand: The operand of the operation.
        :type operand: ASTNode
        """
        self.operation = operation
        self.operand = operand
        super().__init__(self.operation)

    def __str__(self):
        return super().__str__(self.operand)


class ASTAssignmentNode(ASTNode):
    def __init__(self, variable, value):
        """
        Initialise an assignment node.
        :param variable: The variable(s) being assigned to.
        :type variable: ASTNode
        :param value: The values being assigned.
        :type value: ASTNode
        """
        self.variable = variable
        self.value = value
        super().__init__("Assignment")

    def __str__(self):
        return super().__str__(self.variable, self.value)


class ASTAugmentedAssignmentNode(ASTNode):
    def __init__(self, operation, variable, value):
        """
        Initialise an augmented assignment node.
        :param operation: The operation being performed.
        :type operation: str
        :param variable: The variable(s) being assigned to.
        :type variable: ASTNode
        :param value: The value(s) being assigned.
        :type value: ASTNode
        """
        self.operation = operation
        self.variable = variable
        self.value = value
        super().__init__(self.operation)

    def __str__(self):
        return super().__str__(self.variable, self.value)


class ASTAnnotationAssignmentNode(ASTNode):
    def __init__(self, variable, annotation, value=None):
        """
        Initialise an annotation assignment node.
        :param variable: The variable(s) being assigned to.
        :type variable: ASTNode
        :param annotation: The annotation being applied.
        :type annotation: ASTNode
        :param value: The value(s) being assigned.
        :type value: ASTNode
        """
        self.variable = variable
        self.annotation = annotation
        self.value = value
        super().__init__("Annotation Assignment")

    def __str__(self):
        return super().__str__(self.variable, self.annotation, self.variable)


class ASTYieldStatementNode(ASTNode):
    def __init__(self, _from=False, arg=None):
        """
        Initialise a yield statement node.
        :param arg: Optional yield argument.
        :type arg: ASTNode
        """
        self._from = _from
        self.arg = arg

        super().__init__("Yield From" if self._from else "Yield")

    def __str__(self):
        return super().__str__(self.arg)


class ASTPassStatementNode(ASTNode):
    def __init__(self):
        super().__init__("Pass")

    def __str__(self):
        return super().__str__()


class ASTBreakStatementNode(ASTNode):
    def __init__(self):
        super().__init__("Break")

    def __str__(self):
        return super().__str__()


class ASTContinueStatementNode(ASTNode):
    def __init__(self):
        super().__init__("Continue")

    def __str__(self):
        return super().__str__()


class ASTReturnStatementNode(ASTNode):
    def __init__(self, expressions=None):
        self.expression = expressions
        super().__init__("Return")

    def __str__(self):
        return super().__str__(self.expression)


class ASTThrowStatementNode(ASTNode):
    def __init__(self, exception=None):
        self.exception = exception
        super().__init__("Throw")

    def __str__(self):
        return super().__str__(self.exception)


class ASTImportStatementNode(ASTNode):
    def __init__(self, libraries):
        self.libraries = libraries
        super().__init__("Import")

    def __str__(self):
        return super().__str__(*self.libraries)


class ASTImportFromStatementNode(ASTNode):
    def __init__(self, _from, libraries):
        self._from = _from
        self.libraries = libraries
        super().__init__("Import From")

    def __str__(self):
        return super().__str__(self._from, *self.libraries)


class ASTGlobalStatementNode(ASTNode):
    def __init__(self, variables):
        self.variables = variables
        super().__init__("Global")

    def __str__(self):
        return super().__str__(*self.variables)


class ASTNonLocalStatementNode(ASTNode):
    def __init__(self, variables):
        self.variables = variables
        super().__init__("Non-Local")

    def __str__(self):
        return super().__str__(*self.variables)


class ASTAssertStatementNode(ASTNode):
    def __init__(self, condition, message=None):
        self.condition = condition
        self.message = message
        super().__init__("Assert")

    def __str__(self):
        return super().__str__(self.condition, self.message)


class ASTIfStatementNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
        super().__init__("If")

    def __str__(self):
        return super().__str__(self.condition, self.body)


class ASTIfElseStatementNode(ASTNode):
    def __init__(self, condition, body, else_body):
        self.condition = condition
        self.body = body
        self.else_body = else_body
        super().__init__("If-Else")

    def __str__(self):
        return super().__str__(self.condition, self.body, self.else_body)


class ASTLoopStatementNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
        super().__init__("While")

    def __str__(self):
        return super().__str__(self.condition, self.body)


class ASTLoopElseStatementNode(ASTNode):
    def __init__(self, condition, body, else_body):
        self.condition = condition
        self.body = body
        self.else_body = else_body
        super().__init__("While-Else")

    def __str__(self):
        return super().__str__(self.condition, self.body, self.else_body)


class ASTTryStatementNode(ASTNode):
    def __init__(self, body, catches=None, _finally=None):
        if not (catches or _finally):
            raise ValueError

        self.body = body
        self.catches = catches
        self._finally = _finally
        super().__init__("Try")

    def __str__(self):
        return super().__str__(self.body, *self.catches, self._finally)


class ASTCatchStatementNode(ASTNode):
    def __init__(self, exceptions, body):
        self.exceptions = exceptions
        self.body = body
        super().__init__("Catch")

    def __str__(self):
        return super().__str__(self.exceptions, self.body)


class ASTFinallyStatementNode(ASTNode):
    def __init__(self, body):
        self.body = body
        super().__init__("Finally")

    def __str__(self):
        return super().__str__(self.body)


class ASTAsStatementNode(ASTNode):
    def __init__(self, expression, alias):
        self.expression = expression
        self.alias = alias
        super().__init__("As")

    def __str__(self):
        return super().__str__(self.expression, self.alias)


class ASTWithStatementNode(ASTNode):
    def __init__(self, expressions, body):
        self.expressions = expressions
        self.body = body
        super().__init__("With")

    def __str__(self):
        return super().__str__(*self.expressions, self.body)


class ASTFunctionDefinitionNode(ASTNode):
    def __init__(self, name, body, arguments=None):
        self.name = name
        self.body = body
        self.arguments = arguments
        super().__init__("Function Definition")

    def __str__(self):
        return super().__str__(self.name, self.arguments, self.body)


class ASTClassDefinitionNode(ASTNode):
    def __init__(self, name, body, arguments=None):
        self.name = name
        self.body = body
        self.arguments = arguments
        super().__init__("Class Definition")

    def __str__(self):
        return super().__str__(self.name, self.arguments, self.body)


class ASTAsyncNode(ASTNode):
    def __init__(self, child):
        self.child = child
        super().__init__("Async")

    def __str__(self):
        return super().__str__(self.child)
