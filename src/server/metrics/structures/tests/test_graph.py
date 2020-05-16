from unittest import TestCase
from unittest.mock import patch, MagicMock

from metrics.structures.base.graph import Graph, Node


class TestGraph(TestCase):
    """
    Graph test case.
    """

    @patch("metrics.visitors.base.graph_visitor.GraphVisitor")
    @patch.object(Node, "accept")
    def test_accept(self, mock_accept: MagicMock, mock_visitor: MagicMock) -> None:
        """
        Test accept method.

        :param mock_accept: Mock of Node's accept method.
        :param mock_visitor: Mock of GraphVisitor.
        """
        # Check for root = None
        Graph().accept(mock_visitor)

        mock_accept.assert_not_called()

        # Check for root != None
        Graph(Node()).accept(mock_visitor)

        mock_accept.assert_called_with(mock_visitor)


class TestNode(TestCase):
    """
    Node test case.
    """

    @patch("metrics.visitors.base.graph_visitor.GraphVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method.

        :param mock_visitor: Mock of GraphVisitor.
        """
        node = Node()

        node.accept(mock_visitor)

        mock_visitor.visit_children.assert_called_with(node)

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
            # noinspection PyTypeChecker
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
            # noinspection PyTypeChecker
            node.remove_child(invalid_child)
