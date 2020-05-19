from antlr4 import ParserRuleContext

from metrics.parsers.parser import Parser
from metrics.parsers.csharp.base.CSharpParser import CSharpParser as AntlrParser


class CSharpParser(AntlrParser, Parser):
    def parse(self) -> ParserRuleContext:
        return self.compilation_unit()
