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
        super().__init__("Statements", self.first_statement, self.next_statements)


class ASTDelStatementNode(ASTNode):
    def __init__(self, expressions):
        """
        Initialise a delete statement node.
        :param expressions: The expressions to delete.
        :type expressions: ASTExpressionsNode
        """
        self.expressions = expressions
        super().__init__("Del", self.expressions)


class ASTExpressionsNode(ASTNode):
    def __init__(self, first_expression=None, next_expressions=None):
        """
        Initialise an expressions node.
        :param first_expression:
        :type first_expression:
        :param next_expressions:
        :type next_expressions:
        """
        self.first_expression = first_expression
        self.next_expressions = next_expressions
        super().__init__("Expressions", self.first_expression, self.next_expressions)


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
        super().__init__(operation, self.left_operand, self.right_operand)


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
        super().__init__(self.operation, self.operand)


class ASTAssignmentNode(ASTNode):
    def __init__(self, variables=None, values=None):
        """
        Initialise an assignment node.
        :param variables: The variable(s) being assigned to.
        :type variables: ASTNode
        :param values: The values being assigned.
        :type values: ASTNode
        """
        self.variables = variables
        self.values = values
        super().__init__("Assignment", self.variables, self.values)


class ASTAugmentedAssignmentNode(ASTNode):
    def __init__(self, operation, variables=None, values=None):
        """
        Initialise an augmented assignment node.
        :param operation: The operation being performed.
        :type operation: str
        :param variables: The variable(s) being assigned to.
        :type variables: ASTNode
        :param values: The value(s) being assigned.
        :type values: ASTNode
        """
        self.operation = operation
        self.variables = variables
        self.values = values
        super().__init__(self.operation, self.variables, self.values)


class ASTAnnotationAssignmentNode(ASTNode):
    def __init__(self, annotation, variables=None, values=None):
        """
        Initialise an annotation assignment node.
        :param variables: The variable(s) being assigned to.
        :type variables: ASTNode
        :param annotation: The annotation being applied.
        :type annotation: ASTNode
        :param values: The value(s) being assigned.
        :type values: ASTNode
        """
        self.annotation = annotation
        self.variables = variables
        self.values = values
        super().__init__("Annotation Assignment", self.variables, self.annotation, self.values)


class ASTYieldNode(ASTNode):
    def __init__(self, value=None):
        """
        Initialise a yield statement node.
        :param value: The expression(s) to yield.
        :type value: ASTNode
        """
        self.value = value
        super().__init__("Yield", self.value)


class ASTPassStatementNode(ASTNode):
    def __init__(self):
        super().__init__("Pass")


class ASTBreakStatementNode(ASTNode):
    def __init__(self):
        super().__init__("Break")


class ASTContinueStatementNode(ASTNode):
    def __init__(self):
        super().__init__("Continue")


class ASTReturnStatementNode(ASTNode):
    def __init__(self, expressions=None):
        self.expression = expressions
        super().__init__("Return", self.expression)


class ASTThrowStatementNode(ASTNode):
    def __init__(self, exception=None):
        self.exception = exception
        super().__init__("Throw", self.exception)


class ASTImportStatementNode(ASTNode):
    def __init__(self, libraries):
        self.libraries = libraries
        super().__init__("Import", self.libraries)


class ASTGlobalStatementNode(ASTNode):
    def __init__(self, variables):
        self.variables = variables
        super().__init__("Global", self.variables)


class ASTNonLocalStatementNode(ASTNode):
    def __init__(self, variables):
        self.variables = variables
        super().__init__("Non-Local", self.variables)


class ASTAssertStatementNode(ASTNode):
    def __init__(self, condition, message=None):
        self.condition = condition
        self.message = message
        super().__init__("Assert", self.condition, self.message)


class ASTIfStatementNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
        super().__init__("If", self.condition, self.body)


class ASTIfElseStatementNode(ASTNode):
    def __init__(self, condition, body, else_body):
        self.condition = condition
        self.body = body
        self.else_body = else_body
        super().__init__("If-Else", self.condition, self.body, self.else_body)


class ASTLoopStatementNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
        super().__init__("While", self.condition, self.body)


class ASTLoopElseStatementNode(ASTNode):
    def __init__(self, condition, body, else_body):
        self.condition = condition
        self.body = body
        self.else_body = else_body
        super().__init__("While-Else", self.condition, self.body, self.else_body)


class ASTTryStatementNode(ASTNode):
    def __init__(self, body, catches=None, _else=None, _finally=None):
        self.body = body
        self.catches = catches
        self._else = _else
        self._finally = _finally
        super().__init__("Try", self.body, *self.catches, self._else, self._finally)


class ASTCatchStatementNode(ASTNode):
    def __init__(self, exception=None, body=None):
        self.exception = exception
        self.body = body
        super().__init__("Catch", self.exception, self.body)


class ASTFinallyStatementNode(ASTNode):
    def __init__(self, body):
        self.body = body
        super().__init__("Finally", self.body)


class ASTAsNode(ASTNode):
    def __init__(self, expression, alias):
        self.expression = expression
        self.alias = alias
        super().__init__("As", self.expression, self.alias)


class ASTWithStatementNode(ASTNode):
    def __init__(self, expressions, body):
        self.expressions = expressions
        self.body = body
        super().__init__("With", self.expressions, self.body)


class ASTFunctionDefinitionNode(ASTNode):
    def __init__(self, name, body, parameters=None, return_type=None):
        self.name = name
        self.body = body
        self.parameters = parameters
        self.return_type = return_type
        super().__init__("Function Definition", self.name, self.parameters, self.return_type, self.body)


class ASTClassDefinitionNode(ASTNode):
    def __init__(self, name, body, arguments=None):
        self.name = name
        self.body = body
        self.arguments = arguments
        super().__init__("Class Definition", self.name, self.arguments, self.body)


class ASTAsyncNode(ASTNode):
    def __init__(self, child):
        self.child = child
        super().__init__("Async", self.child)


class ASTParametersNode(ASTNode):
    def __init__(self, first_parameter, next_parameters=None):
        self.first_parameter = first_parameter
        self.next_parameters = next_parameters
        super().__init__("Parameters", self.first_parameter, self.next_parameters)


class ASTParameterNode(ASTNode):
    def __init__(self, name, _type=None, default=None):
        self.name = name
        self.type = _type
        self.default = default
        super().__init__("Parameter", self.name, self.type, self.default)


class ASTPositionalArgumentsParameter(ASTNode):
    def __init__(self, name, _type=None):
        self.name = name
        self.type = _type
        super().__init__("Positional Arguments Parameter", self.name, self.type)


class ASTKeywordArgumentsParameter(ASTNode):
    def __init__(self, name, _type=None):
        self.name = name
        self.type = _type
        super().__init__("Keyword Arguments Parameter", self.name, self.type)


class ASTFromNode(ASTNode):
    def __init__(self, source, expressions):
        self.source = source
        self.expressions = expressions
        super().__init__("From", self.source, self.expressions)


class ASTAnonymousFunctionDefinitionNode(ASTNode):
    def __init__(self, body, parameters=None):
        self.body = body
        self.parameters = parameters
        super().__init__("Anonymous Function Definition", self.parameters, self.body)


class ASTUnpackExpressionNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression
        super().__init__("Unpack", self.expression)


class ASTAwaitNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression
        super().__init__("Await", self.expression)


class ASTAccessNode(ASTNode):
    def __init__(self, name, subscript):
        self.name = name
        self.subscript = subscript
        super().__init__("Access", self.name, self.subscript)


class ASTSubscriptsNode(ASTNode):
    def __init__(self, first_subscript, next_subscripts):
        self.first_subscript = first_subscript
        self.next_subscripts = next_subscripts
        super().__init__("Subscripts", self.first_subscript, self.next_subscripts)


class ASTIndexNode(ASTNode):
    def __init__(self, index):
        self.index = index
        super().__init__("Index", self.index)


class ASTSliceNode(ASTNode):
    def __init__(self, start, stop, step):
        self.start = start
        self.stop = stop
        self.step = step
        super().__init__("Slice", self.start, self.stop, self.step)


class ASTCallNode(ASTNode):
    def __init__(self, name, arguments=None):
        self.name = name
        self.arguments = arguments
        super().__init__("Call", self.name, self.arguments)


class ASTArgumentsNode(ASTNode):
    def __init__(self, first_argument, next_arguments):
        self.first_argument = first_argument
        self.next_arguments = next_arguments
        super().__init__("Arguments", self.first_argument, self.next_arguments)

    def __str__(self):
        return super().__str__()


class ASTMemberNode(ASTNode):
    def __init__(self, parent, child):
        self.parent = parent
        self.child = child
        super().__init__("Member", self.parent, self.child)


class ASTItemsNode(ASTNode):
    def __init__(self, first_item, next_items):
        self.first_item = first_item
        self.next_items = next_items
        super().__init__("Items", self.first_item, self.next_items)


class ASTListNode(ASTNode):
    def __init__(self, items):
        self.items = items
        super().__init__("List", self.items)


class ASTTupleNode(ASTNode):
    def __init__(self, items):
        self.items = items
        super().__init__("Tuple", self.items)


class ASTGeneratorExpressionNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression
        super().__init__("Generator Expression", self.expression)


class ASTComprehensionNode(ASTNode):
    def __init__(self, value, loop):
        self.value = value
        self.loop = loop
        super().__init__("Comprehension", self.value, self.loop)


class ASTMapNode(ASTNode):
    def __init__(self, items):
        self.items = items
        super().__init__("Map", self.items)


class ASTSetNode(ASTNode):
    def __init__(self, items):
        self.items = items
        super().__init__("Set", self.items)


class ASTKeyValuePairNode(ASTNode):
    def __init__(self, key, value):
        self.key = key
        self.value = value
        super().__init__("Key-Value Pair", self.key, self.value)


class ASTDecoratedNode(ASTNode):
    def __init__(self, decorators, target):
        self.decorators = decorators
        self.target = target
        super().__init__("Decorated", self.decorators, self.target)


class ASTDecoratorsNode(ASTNode):
    def __init__(self, first_decorator, next_decorators):
        self.first_decorator = first_decorator
        self.next_decorators = next_decorators
        super(ASTDecoratorsNode, self).__init__("Decorators", self.first_decorator, self.next_decorators)


class ASTDecoratorNode(ASTNode):
    def __init__(self, name, arguments=None):
        self.name = name
        self.arguments = arguments
        super().__init__("Decorator", self.name, self.arguments)


class ASTCatchStatementsNode(ASTNode):
    def __init__(self, first_catch, next_catches):
        self.first_catch = first_catch
        self.next_catches = next_catches
        super().__init__("Catch Statements", self.first_catch, self.next_catches)
