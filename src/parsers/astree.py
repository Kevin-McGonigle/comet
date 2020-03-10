from tree import Node, Tree


class AST(Tree):
    pass


class ASTNode(Node):
    pass


class ASTStatementsNode(ASTNode):
    def __init__(self, statements):
        self.first_statement = statements[0]
        if len(statements) > 1:
            self.next_statements = ASTStatementsNode(statements[1:])
        else:
            self.next_statements = None
        super().__init__("Statements")

    def __str__(self):
        return super().__str__(self.first_statement, self.next_statements)


class ASTDelStatementNode(ASTNode):
    def __init__(self, expressions):
        self.expressions = expressions
        super().__init__("Del")

    def __str__(self):
        return super().__str__(self.expressions)


class ASTExpressionsNode(ASTNode):
    def __init__(self, expressions):
        self.first_expression = expressions[0]
        if len(expressions) > 1:
            self.next_expressions = ASTExpressionsNode(expressions[1:])
        else:
            self.next_expressions = None
        super().__init__("Expressions")

    def __str__(self):
        return super().__str__(self.first_expression, self.next_expressions)


class ASTBinOpNode(ASTNode):
    def __init__(self, operation, left, right):
        self.left = left
        self.right = right
        super().__init__(operation)

    def __str__(self):
        return super().__str__(self.left, self.right)


class ASTUnOpNode(ASTNode):
    def __init__(self, operation, child):
        self.child = child
        super().__init__(operation)

    def __str__(self):
        return super().__str__(self.child)
