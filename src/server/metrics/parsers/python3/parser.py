from antlr4 import ParserRuleContext

from metrics.parsers.parser import Parser
from metrics.parsers.python3.base.Python3Parser import Python3Parser as AntlrParser


class Python3Parser(AntlrParser, Parser):
    def parse(self) -> ParserRuleContext:
        return self.file_input()
