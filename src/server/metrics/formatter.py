from metrics.calculator import CalculatorStub
from metrics.visitors.formatting.inheritance_tree_formatting_visitor import InheritanceTreeFormattingVisitor
from metrics.visitors.formatting.control_flow_graph_formatting_visitor import ControlFlowGraphFormattingVisitor


class Formatter(object):
    """
    Metric/model formatter.

    Class for formatting metrics & models for front-end use.
    """

    def __init__(self, file_name: str):
        self.calculator = CalculatorStub()
        self.metric_info = {
            "fileName": "_".join(file_name.split("_")[2:]),
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
        # self.generate_control_flow_graph()
        # self.generate_class_diagram()

    def generate_metrics(self):
        self.metric_info["metrics"]["logicalLinesOfCode"] = self.calculator.logical_lines_of_code(None)
        self.metric_info["metrics"]["cyclomaticComplexity"] = self.calculator.cyclomatic_complexity(None)
        self.metric_info["metrics"]["maximumInheritanceDepth"] = self.calculator.maximum_inheritance_depth(None)
        self.metric_info["metrics"]["maxmimumNestingDepth"] = self.calculator.maximum_nesting_depth(None)

        ac = self.calculator.afferent_coupling(None)
        ec = self.calculator.efferent_coupling(None)
        self.metric_info["metrics"]["afferentCoupling"] = [{"name": node.name, "value": ac[node]} for node in ac]
        self.metric_info["metrics"]["efferentCoupling"] = [{"name": node.name, "value": ec[node]} for node in ec]
 
    def generate_inheritance_tree(self):
        nodes, links = InheritanceTreeFormattingVisitor().visit(self.calculator.inheritance_tree(None))
        self.metric_info["structures"]["inheritanceTree"] = {
            "nodes": nodes,
            "links": links
        }

    def generate_dependency_graph(self):
        dependency_graph_graph_data = {
            "nodes": [],
            "links": [],
        }
        for node in self.calculator.dependency_graph(None).classes:
            dependency_graph_graph_data["nodes"].append({"id": node.name})

            for dependency in node.dependencies:
                dependency_graph_graph_data["links"].append({"source": dependency.name, "target": node.name})
        
        self.metric_info["structures"]["dependencyGraph"] = dependency_graph_graph_data

    def generate_control_flow_graph(self):
        nodes, links = ControlFlowGraphFormattingVisitor().visit(self.calculator.control_flow_graph(None))
        print("CFG", nodes, links)
        self.metric_info["structures"]["controlFlowGraph"] = self.calculator.control_flow_graph(None)

    def generate_class_diagram(self):
        self.metric_info["structures"]["classDiagram"] = self.calculator.class_diagram(None)
