from abc import abstractmethod, ABCMeta

from antlr4 import Parser as AntlrParser, ParserRuleContext


class Parser(AntlrParser):
    __metaclass__ = ABCMeta

    @abstractmethod
    def parse(self) -> ParserRuleContext:
        """
        Generate a parse tree starting from the default entry parser rule.
        :return: The parse tree.
        """
        pass
