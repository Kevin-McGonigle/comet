from antlr4 import InputStream, CommonTokenStream

from ..parsers.python3.Python3CometVisitor import Python3CometVisitor
from ..parsers.python3.Python3Lexer import Python3Lexer
from ..parsers.python3.Python3Parser import Python3Parser


class Error(Exception):
    """Base class for other exceptions"""
    pass

class BaseParseTreeError(Error):
    """Raised when the base parse tree cannot be generated"""
    pass

class InheritanceTreeError(Error):
    """Raised when inheritance tree cannot be generated"""
    pass

class Manager:
    def __init__(self, data, comet_result=False):
        self.data = self.read_file_content(data)
        self.parse_tree = self.generate_base_parse_tree()
        
        if comet_result:
            self.comet_result = self.generate_comet_result()
        else:
            self.comet_result = None
    
    def read_file_content(self, file):
        f = file.open()
        data = f.read()
        f.close()
        return str(data, "utf-8")

    def generate_base_parse_tree(self):
        input_stream = InputStream(self.data)
        lexer = Python3Lexer(input_stream)
        tokens = CommonTokenStream(lexer)
        parser = Python3Parser(tokens)
        return parser.file_input()

    def generate_comet_result(self):
        visitor = Python3CometVisitor()
        return visitor.visit(self.parse_tree)