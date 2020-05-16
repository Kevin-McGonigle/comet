from metrics.calculator import Calculator
from metrics.visitors.formatting.ast_formatting_visitor import ASTFormattingVisitor
from metrics.visitors.formatting.cfg_formatting_visitor import CFGFormattingVisitor
from metrics.visitors.formatting.inheritance_tree_formatting_visitor import InheritanceTreeFormattingVisitor

class Formatter(object):
    """
    Metric/model formatter.

    Class for formatting metrics & models for front-end use.
    """

    def __init__(self, Calculator: Calculator, file_name: str):
        self.calculator = Calculator
        self.metric_info = {
            "fileName": "test.py",
            "structures": {},
            "metrics": {}
        }

    def generate(self) -> dict:
        self.generate_structures()
        self.generate_metrics()
        return self.metric_info

    def generate_structures(self):
        self.generate_inheritance_tree()
        self.generate_dependency_graph()
        self.generate_ast()
        self.generate_control_flow_graph()
        self.generate_class_diagram()

    def generate_metrics(self):
        self.metric_info["metrics"]["logicalLinesOfCode"] = self.calculator.logical_lines_of_code()
        self.metric_info["metrics"]["cyclomaticComplexity"] = self.calculator.cyclomatic_complexity()
        self.metric_info["metrics"]["maximumInheritanceDepth"] = self.calculator.maximum_inheritance_depth()
        self.metric_info["metrics"]["maximumNestingDepth"] = self.calculator.maximum_nesting_depth()

        ac = self.calculator.afferent_coupling()
        ec = self.calculator.efferent_coupling()
        self.metric_info["metrics"]["afferentCoupling"] = [{"name": node.name, "value": ac[node]} for node in ac]
        self.metric_info["metrics"]["efferentCoupling"] = [{"name": node.name, "value": ec[node]} for node in ec]

    def generate_inheritance_tree(self):
        nodes, links = InheritanceTreeFormattingVisitor().visit(self.calculator.inheritance_tree())
        self.metric_info["structures"]["inheritanceTree"] = {
            "nodes": nodes,
            "links": links
        }

    def generate_dependency_graph(self):
        dependency_graph_graph_data = {
            "nodes": [],
            "links": [],
        }
        for node in self.calculator.dependency_graph().classes:
            dependency_graph_graph_data["nodes"].append({"id": node.name})

            for dependency in node.dependencies:
                dependency_graph_graph_data["links"].append({"source": dependency.name, "target": node.name})

        self.metric_info["structures"]["dependencyGraph"] = dependency_graph_graph_data

    def generate_control_flow_graph(self):
        nodes, links = CFGFormattingVisitor().visit(self.calculator.control_flow_graph())
        self.metric_info["structures"]["controlFlowGraph"] = {
            "nodes": nodes,
            "links": links
        }

    def generate_ast(self):
        self.metric_info["structures"]["abstractSyntaxTree"] = ASTFormattingVisitor().visit(self.calculator.ast)

    def generate_class_diagram(self):
        self.metric_info["structures"]["classDiagram"] = self.calculator.class_diagram()
