class AST(object):
    def __init__(self, root=None) -> None:
        self.root = root
        super().__init__()

    def __str__(self):
        return str(self.root)


class Node(object):
    def __init__(self):
        super().__init__()

    def __str__(self, *args):
        s = self.__class__.__name__
        if len(args) > 0:
            for arg in args[:-1]:
                arg_s = str(arg).splitlines()
                s += f"\n|- {arg_s[0]}"
                if len(arg_s) > 1:
                    for line in arg_s[1:]:
                        s += f"\n|  {line}"
            if args[-1] is not None:
                arg_s = str(args[-1]).splitlines()
                s += f"\n`- {arg_s[0]}"
                if len(arg_s) > 1:
                    for line in arg_s[1:]:
                        s += f"\n   {line}"
        return s


class Statements(Node):
    def __init__(self, first_statement, next_statements=None) -> None:
        self.first_statement = first_statement
        self.next_statements = next_statements
        super().__init__()

    def __str__(self):
        return super().__str__(self.first_statement, self.next_statements)


if __name__ == "__main__":
    statements = Statements("This", Statements("is", Statements("a", Statements("test"))))
    ast = AST(statements)
    print(ast)
