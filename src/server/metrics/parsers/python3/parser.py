from antlr4 import ParserRuleContext

from parsers.parser import Parser
from parsers.python3.base.Python3Parser import Python3Parser as AntlrParser


class Python3Parser(AntlrParser, Parser):
    def parse(self) -> ParserRuleContext:
        return self.file_input()
