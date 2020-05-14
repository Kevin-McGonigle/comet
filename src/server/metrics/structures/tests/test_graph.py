from unittest import TestCase
from unittest.mock import patch, NonCallableMock

from metrics.structures.base.graph import Graph, Node
from metrics.visitors.base.graph_visitor import GraphVisitor


class TestGraph(TestCase):
    """
    Graph test case.
    """

    @patch.object(Node, "accept")
    def test_accept(self, mock_accept: NonCallableMock) -> None:
        """
        Test accept method.

        :param mock_accept: Mock of Node's accept method.
        """
        # Check for root = None
        graph = Graph()

        visitor = GraphVisitor()

        graph.accept(visitor)

        mock_accept.assert_not_called()

        # Check for root != None
        root = Node()

        graph = Graph(root)

        graph.accept(visitor)

        mock_accept.assert_called_with(visitor)

        root.accept.assert_called_with(visitor)


class TestNode(TestCase):
    """
    Node test case.
    """

    @patch.object(GraphVisitor, "visit_children")
    def test_accept(self, mock_visit_children: NonCallableMock) -> None:
        """
        Test accept method.

        :param mock_visit_children: Mock of GraphVisitor's visit_children method.
        """
        node = Node()

        visitor = GraphVisitor()

        node.accept(visitor)

        mock_visit_children.assert_called_with(node)

        visitor.visit_children.assert_called_with(node)

    def test_add_child(self) -> None:
        """
        Test add_child method.
        """
        # Valid child, not in node's children
        node = Node()

        child = Node()

        node.add_child(child)

        self.assertIn(child, node.children)

        # Valid child, in node's children
        with self.assertRaises(ValueError):
            node.add_child(child)

        # Invalid child
        invalid_child = "invalid"
        with self.assertRaises(TypeError):
            node.add_child(invalid_child)

        self.assertNotIn(invalid_child, node.children)

    def test_remove_child(self) -> None:
        """
        Test remove_child method.
        """
        # Valid child, in node's children
        child = Node()

        node = Node(child)

        node.remove_child(child)

        self.assertNotIn(child, node.children)

        # Valid child, not in node's children
        with self.assertRaises(ValueError):
            node.remove_child(child)

        # Invalid child
        invalid_child = "invalid"
        with self.assertRaises(TypeError):
            node.remove_child(invalid_child)
