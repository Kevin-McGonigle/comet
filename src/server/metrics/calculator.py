from metrics.structures.ast import AST
from metrics.structures.cfg import CFG
from metrics.structures.inheritance_tree import InheritanceTree


class Calculator(object):
    def __init__(self, ast=None, cfg=None, inheritance_tree=None):
        """
        Metric/model calculator.
        :param ast: Abstract syntax tree.
        :type ast: AST
        :param cfg: Control flow graph.
        :type cfg: CFG or None
        :param inheritance_tree: Inheritance tree.
        :type inheritance_tree: InheritanceTree or None
        """
        self.ast = ast
        self.cfg = cfg
        self.it = inheritance_tree

    def abstract_syntax_tree(self):
        if self.ast:
            return self.ast

        # TODO: Generate AST

    def control_flow_graph(self):
        """
        Calculate control flow graph.
        :return: Control flow graph.
        :rtype: CFG
        """
        if self.cfg:
            return self.cfg

        # TODO: Generate CFG

        pass

    def inheritance_tree(self):
        """
        Calculate inheritance tree.
        :return: Inheritance tree.
        :rtype: InheritanceTree
        """
        if self.it:
            return self.it

        # TODO: Generate inheritance tree
        pass

    # TODO: Add calculation functions for all metrics and structures.
