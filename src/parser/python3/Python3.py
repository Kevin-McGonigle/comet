from sys import argv
from antlr4 import *
from Python3Lexer import Python3Lexer
from Python3Listener import Python3Listener
from Python3Parser import Python3Parser
from Python3Visitor import Python3Visitor


def main():
    input_stream = FileStream(argv[1])
    lexer = Python3Lexer(input_stream)
    parser = Python3Parser(CommonTokenStream(lexer))
    tree = parser.file_input()
    print(tree.toStringTree(recog=parser))


if __name__ == "__main__":
    main()
