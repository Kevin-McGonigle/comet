from typing import Any, Dict

from metrics.structures.base.graph import Graph, Node


class GraphVisitor(object):
    def visit(self, graph: Graph):
        """
        Visit a graph structure.

        :param graph: The graph to visit.
        :return: The output of the visiting process.
        """
        return graph.accept(self)

    def visit_children(self, node: Node) -> Dict[Node, Any]:
        """
        Visit each of a node's children.
        :param node: The parent node whose children to visit.
        :return: Mapping of each child to their visit result.
        """
        return {child: child.accept(self) for child in node.children}
