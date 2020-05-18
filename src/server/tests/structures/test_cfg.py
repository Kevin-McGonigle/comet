from unittest import TestCase
from unittest.mock import patch, MagicMock

from metrics.structures.cfg import CFG, CFGBlock, CFGIfBlock, CFGSwitchBlock, CFGContinueBlock, CFGBreakBlock, \
    CFGLoopElseBlock, CFGLoopBlock, CFGIfElseBlock


class TestCFG(TestCase):
    """
    Control-flow graph test case.
    """

    def test_entry_block_getter(self) -> None:
        """
        Test getter for entry_block property.
        """
        cfg = CFG()

        self.assertIs(cfg.entry_block, cfg.root)

    def test_entry_block_setter(self) -> None:
        """
        Test setter for entry_block property.
        """
        cfg = CFG()

        cfg.entry_block = new_entry_block = CFGBlock()

        self.assertIs(cfg.root, new_entry_block)

    def test_entry_block_deleter(self) -> None:
        """
        Test deleter for entry_block property.
        """
        cfg = CFG()

        cfg.entry_block = CFGBlock()

        del cfg.entry_block

        with self.assertRaises(AttributeError):
            print(cfg.root)

    @patch("metrics.visitors.base.cfg_visitor.CFGVisitor")
    @patch.object(CFGBlock, "accept")
    def test_accept(self, mock_accept: MagicMock, mock_visitor: MagicMock) -> None:
        """
        Test accept method.

        :param mock_accept: Mock of CFGBlock's accept method.
        :param mock_visitor: Mock of CFGVisitor.
        """
        CFG().accept(mock_visitor)

        mock_accept.assert_not_called()

        CFG(CFGBlock()).accept(mock_visitor)

        mock_accept.assert_called_with(mock_visitor)


class TestCFGBlock(TestCase):
    """
    CFG basic block test case.
    """

    def test_values(self) -> None:
        """
        Test values method.
        """
        block = CFGBlock({"test": CFGBlock()})

        self.assertEqual(block.values(), list(block.children.values()))

    def test_append(self) -> None:
        """
        Test append method.
        """
        block = CFGBlock()

        appended_block = CFGBlock()
        block.append(appended_block)

        self.assertIs(block["exit_block"], appended_block)

        new_appended_block = CFGBlock()
        block.append(new_appended_block)
        self.assertIs(block["exit_block"]["exit_block"], new_appended_block)

    @patch("metrics.visitors.base.cfg_visitor.CFGVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method
        :param mock_visitor: Mock of CFGVisitor.
        """
        block = CFGBlock()

        block.accept(mock_visitor)

        mock_visitor.visit_block.assert_called_with(block)

    def test_add_child(self):
        with self.assertRaises(NotImplementedError):
            CFGBlock().add_child(CFGBlock())

    def test_remove_child(self):
        with self.assertRaises(NotImplementedError):
            CFGBlock().remove_child(CFGBlock())


class TestCFGIfBlock(TestCase):
    @patch("metrics.visitors.base.cfg_visitor.CFGVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method
        :param mock_visitor: Mock of CFGVisitor.
        """
        block = CFGIfBlock()

        block.accept(mock_visitor)

        mock_visitor.visit_if_block.assert_called_with(block)


class TestCFGIfElseBlock(TestCase):
    @patch("metrics.visitors.base.cfg_visitor.CFGVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method
        :param mock_visitor: Mock of CFGVisitor.
        """
        block = CFGIfElseBlock()

        block.accept(mock_visitor)

        mock_visitor.visit_if_else_block.assert_called_with(block)


class TestCFGLoopBlock(TestCase):
    @patch("metrics.visitors.base.cfg_visitor.CFGVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method
        :param mock_visitor: Mock of CFGVisitor.
        """
        block = CFGLoopBlock()

        block.accept(mock_visitor)

        mock_visitor.visit_loop_block.assert_called_with(block)


class TestCFGLoopElseBlock(TestCase):
    @patch("metrics.visitors.base.cfg_visitor.CFGVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method
        :param mock_visitor: Mock of CFGVisitor.
        """
        block = CFGLoopElseBlock()

        block.accept(mock_visitor)

        mock_visitor.visit_loop_else_block.assert_called_with(block)


class TestCFGSwitchBlock(TestCase):
    @patch("metrics.visitors.base.cfg_visitor.CFGVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method
        :param mock_visitor: Mock of CFGVisitor.
        """
        block = CFGSwitchBlock()

        block.accept(mock_visitor)

        mock_visitor.visit_switch_block.assert_called_with(block)


class TestCFGBreakBlock(TestCase):
    @patch("metrics.visitors.base.cfg_visitor.CFGVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method
        :param mock_visitor: Mock of CFGVisitor.
        """
        block = CFGBreakBlock()

        block.accept(mock_visitor)

        mock_visitor.visit_break_block.assert_called_with(block)


class TestCFGContinueBlock(TestCase):
    @patch("metrics.visitors.base.cfg_visitor.CFGVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method
        :param mock_visitor: Mock of CFGVisitor.
        """
        block = CFGContinueBlock()

        block.accept(mock_visitor)

        mock_visitor.visit_continue_block.assert_called_with(block)
