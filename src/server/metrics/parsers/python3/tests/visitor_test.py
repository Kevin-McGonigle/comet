from sys import stdin

from antlr4 import InputStream, CommonTokenStream

from server.metrics.parsers.python3.Python3CometVisitor import Python3CometVisitor
from server.metrics.parsers.python3.Python3Lexer import Python3Lexer
from server.metrics.parsers.python3.Python3Parser import Python3Parser


def main():
    content = stdin.read()
    input_stream = InputStream(content)
    lexer = Python3Lexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = Python3Parser(tokens)
    parse_tree = parser.file_input()
    visitor = Python3CometVisitor()
    output = visitor.visit(parse_tree)
    print(output)


if __name__ == "__main__":
    main()
