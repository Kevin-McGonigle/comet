from metrics.calculator import Calculator
from metrics.structures.ast import AST


class Formatter(object):
    """
    Metric/model formatter.

    Class for formatting metrics & models for front-end use.
    """

    def __init__(self, ast: AST):
        self.calculator = Calculator(ast)
        self.metric_info = {}

    def generate_info(self):
        self.metric_info["inheritance_tree"] = self.calculator.inheritance_tree()
        self.metric_info["control_flow_graph"] = self.calculator.control_flow_graph()
        self.metric_info["dependency_graph"] = self.calculator.dependency_graph()
        # TODO: class diagram

        print(self.metric_info)