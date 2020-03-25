from sys import stdin

from antlr4 import InputStream, CommonTokenStream

from parsers.python3.Python3CometVisitor import Python3CometVisitor
from parsers.python3.Python3Lexer import Python3Lexer
from parsers.python3.Python3Parser import Python3Parser

with open('test.txt', 'r') as f:
    content = f.read()

def main():
    input_stream = InputStream(content)
    lexer = Python3Lexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = Python3Parser(tokens)
    parse_tree = parser.file_input()
    visitor = Python3CometVisitor()
    output = visitor.visit(parse_tree)

    inheritance_tree = visitor.inheritance_tree
    print(inheritance_tree)


if __name__ == "__main__":
    main()
