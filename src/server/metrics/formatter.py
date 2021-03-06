from metrics.calculator import Calculator
from metrics.visitors.formatting.ast_formatting_visitor import ASTFormattingVisitor
from metrics.visitors.formatting.cfg_formatting_visitor import CFGFormattingVisitor
from metrics.visitors.formatting.inheritance_tree_formatting_visitor import InheritanceTreeFormattingVisitor


class Formatter(object):
    """
    Metric/model formatter.

    Class for formatting metrics & models for front-end use.
    """

    def __init__(self, calculator: Calculator, file_name: str):
        self.calculator = calculator
        self.metric_info = {
            "fileName": file_name,
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
        for cls in self.calculator.dependency_graph().classes:
            for node in cls:
                dependency_graph_graph_data["nodes"].append({"id": node.name})

                for dependency in node.dependencies:
                    dependency_graph_graph_data["links"].append({"source": node.name, "target": dependency.name})

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
        formatted_class_diagram = {
            "nodes": [],
            "links": []
        }

        for cls in self.calculator.class_diagram().classes:
            attributes = {}
            methods = {}

            for attribute in cls.attributes:
                attributes[attribute.name] = attribute.type if attribute.type is not None else ""

            for method in cls.methods:
                parameters = {}
                for parameter in method.parameters if isinstance(method.parameters, list) else [method.parameters]:
                    parameters[parameter.name] = parameter.type if parameter.type is not None else ""

                methods[method.name] = {
                    "arguments": parameters,
                    "returnType": method.return_type
                }

            formatted_class_diagram["nodes"].append({"id": cls.name, "classArgs": attributes,
                                                     "classFunctions": methods})

            for relationship in cls.relationships:
                formatted_class_diagram["links"].append({"source": cls.name, "target": relationship.relation.name,
                                                         "label": relationship.type.value, "value": 1})

        self.metric_info["structures"]["classDiagram"] = formatted_class_diagram
