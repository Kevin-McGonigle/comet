from metrics.structures.base.graph import Graph, Node


class GraphVisitor(object):
    def visit(self, graph):
        """
        Visit a graph structure.
        :param graph: The graph to visit.
        :type graph: Graph
        :return: The output of the visiting process.
        :rtype: Any
        """
        return graph.accept(self)

    def visit_children(self, node):
        """
        Visit each of a node's children.
        :param node: The parent node whose children to visit.
        :type node: Node
        :return: Mapping of each child to their visit result.
        :rtype: dict[Node, Any]
        """
        return {child: child.accept(self) for child in node.children}
