from tree import Node, Tree


class AST(Tree):
    pass


class ASTNode(Node):
    pass


class StatementsNode(ASTNode):
    def __init__(self, statements):
        self.first_statement = statements[0]
        if len(statements) > 1:
            self.next_statements = StatementsNode(statements[1:])
        else:
            self.next_statements = None
        super(StatementsNode, self).__init__("Statements")

    def __str__(self):
        return super(StatementsNode, self).__str__(self.first_statement, self.next_statements)


class DelStatementNode(ASTNode):
    def __init__(self, expressions):
        self.expressions = expressions
        super(DelStatementNode, self).__init__("Del")

    def __str__(self):
        return super(DelStatementNode, self).__str__(self.expressions)


class ExpressionsNode(ASTNode):
    def __init__(self, expressions):
        self.first_expression = expressions[0]
        if len(expressions) > 1:
            self.next_expressions = ExpressionsNode(expressions[1:])
        else:
            self.next_expressions = None
        super(ExpressionsNode, self).__init__("Expressions")

    def __str__(self):
        return super(ExpressionsNode, self).__str__(self.first_expression, self.next_expressions)


class BinOpNode(ASTNode):
    def __init__(self, operation, left, right):
        self.left = left
        self.right = right
        super(BinOpNode, self).__init__(operation)

    def __str__(self):
        return super(BinOpNode, self).__str__(self.left, self.right)


if __name__ == "__main__":
    stmts = StatementsNode(["This", "is", "a", "test"])
    ast = Tree(stmts)
    print(ast)
