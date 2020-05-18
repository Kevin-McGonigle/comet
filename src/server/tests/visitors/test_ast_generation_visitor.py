from unittest import TestCase
from unittest.mock import patch, MagicMock

from metrics.structures.ast import AST, ASTMultiplesNode, ASTNode, ASTMemberNode
from metrics.visitors.structures.ast_generation_visitor import ASTGenerationVisitor, ParseTreeVisitor


class TestASTGenerationVisitor(TestCase):
    """
    Base AST generation visitor test case.
    """

    @patch.object(ParseTreeVisitor, "visit")
    @patch("antlr4.tree.Tree.ParseTree")
    def test_visit(self, mock_tree: MagicMock, mock_base_visit: MagicMock) -> None:
        """
        Test visit method.

        :param mock_tree: Mock of ParseTree.
        :param mock_base_visit: Mock of ParseTreeVisitor's visit method.
        """
        ast = ASTGenerationVisitor().visit(mock_tree)
        mock_base_visit.assert_called_with(mock_tree)

        self.assertIsInstance(ast, AST)

    def test_build_multi(self) -> None:
        """
        Test build_multi method.
        """
        visitor = ASTGenerationVisitor()

        # region sequence = Null

        self.assertEqual(visitor.build_multi(None, ASTMultiplesNode), visitor.defaultResult())

        # endregion

        # region sequence = []

        nodes = []

        self.assertEqual(visitor.build_multi(nodes, ASTMultiplesNode), visitor.defaultResult())

        # endregion

        # region sequence = [x]

        nodes = [ASTNode()]

        self.assertIs(visitor.build_multi(nodes, ASTMultiplesNode), nodes[0])

        # endregion

        # region sequence = [x, ..., y]

        nodes = [ASTNode(), ASTNode()]

        multi = visitor.build_multi(nodes, ASTMultiplesNode)

        self.assertIsInstance(multi, ASTMultiplesNode)

        self.assertIs(multi[0], nodes[0])
        self.assertIs(multi[1], nodes[1])

        # endregion

    def test_build_right_associated(self) -> None:
        """
        Test build_right_associated method.
        """
        visitor = ASTGenerationVisitor()

        # region sequence = Null

        self.assertEqual(visitor.build_right_associated(None, ASTMemberNode), visitor.defaultResult())

        # endregion

        # region sequence = []

        nodes = []

        self.assertEqual(visitor.build_right_associated(nodes, ASTMemberNode), visitor.defaultResult())

        # endregion

        # region sequence = [x]

        nodes = [ASTNode()]

        self.assertIs(visitor.build_right_associated(nodes, ASTMemberNode), nodes[0])

        # endregion

        # region sequence = [x, ..., y]

        nodes = [ASTNode(), ASTNode(), ASTNode()]

        member = visitor.build_right_associated(nodes, ASTMemberNode)

        self.assertIsInstance(member, ASTMemberNode)

        self.assertIs(member["parent"], nodes[0])

        self.assertIsInstance(member["member"], ASTMemberNode)

        self.assertIs(member["member"]["parent"], nodes[1])
        self.assertIs(member["member"]["member"], nodes[2])

        # endregion

    def test_build_left_associated(self) -> None:
        """
        Test build_left_associated method.
        """
        visitor = ASTGenerationVisitor()

        # region sequence = Null

        self.assertEqual(visitor.build_left_associated(None, ASTMemberNode), visitor.defaultResult())

        # endregion

        # region sequence = []

        nodes = []

        self.assertEqual(visitor.build_left_associated(nodes, ASTMemberNode), visitor.defaultResult())

        # endregion

        # region sequence = [x]

        nodes = [ASTNode()]

        self.assertIs(visitor.build_left_associated(nodes, ASTMemberNode), nodes[0])

        # endregion

        # region sequence = [x, ..., y]

        nodes = [ASTNode(), ASTNode(), ASTNode()]

        member = visitor.build_left_associated(nodes, ASTMemberNode)

        self.assertIsInstance(member, ASTMemberNode)

        self.assertIs(member["member"], nodes[2])

        self.assertIsInstance(member["parent"], ASTMemberNode)

        self.assertIs(member["parent"]["parent"], nodes[0])
        self.assertIs(member["parent"]["member"], nodes[1])

        # endregion
