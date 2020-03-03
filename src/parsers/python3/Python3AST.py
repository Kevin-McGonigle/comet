from sys import stdin

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker

from python3.Python3ASTVisitor import Python3ASTVisitor
from python3.Python3Lexer import Python3Lexer
from python3.Python3Parser import Python3Parser


def main():
    input_stream = InputStream(stdin.read())
    lexer = Python3Lexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = Python3Parser(tokens)
    tree = parser.file_input()
    visitor = Python3ASTVisitor()
    output = visitor.visit(tree)
    print(output)


if __name__ == "__main__":
    main()
