from unittest import TestCase
from unittest.mock import patch, MagicMock

from metrics.structures.cfg import CFGBlock, CFG


class TestCFG(TestCase):
    """
    Control-flow graph test case.
    """

    def test_entry_block_getter(self) -> None:
        """
        Test getter for entry_block property.
        """
        cfg = CFG(CFGBlock())

        self.assertIs(cfg.entry_block, cfg.root)

    def test_entry_block_setter(self) -> None:
        """
        Test setter for entry_block property.
        """
        cfg = CFG(CFGBlock())

        cfg.entry_block = new_entry_block = CFGBlock()

        self.assertIs(cfg.root, new_entry_block)

    def test_entry_block_deleter(self):
        """
        Test deleter for entry_block property.
        """
        cfg = CFG(CFGBlock())

        del cfg.entry_block

        with self.assertRaises(AttributeError):
            print(cfg.entry_block)

    @patch("metrics.visitors.base.cfg_visitor.CFGVisitor")
    @patch.object(CFGBlock, "accept")
    def test_accept(self, mock_accept: MagicMock, mock_visitor: MagicMock):
        cfg = CFG()

        cfg.accept(mock_visitor)

        self.fail()


class TestCFGBlock(TestCase):
    def test_exit_block_getter(self):
        self.fail()

    def test_exit_block_setter(self):
        self.fail()

    def test_exit_block_deleter(self):
        self.fail()

    def test_accept(self):
        self.fail()


class TestCFGIfBlock(TestCase):
    def test_success_block_getter(self):
        self.fail()

    def test_success_block_setter(self):
        self.fail()

    def test_success_block_deleter(self):
        self.fail()

    def test_exit_block_getter(self):
        self.fail()

    def test_exit_block_setter(self):
        self.fail()

    def test_exit_block_deleter(self):
        self.fail()

    def test_accept(self):
        self.fail()

    def test_add_child(self):
        self.fail()

    def test_remove_child(self):
        self.fail()


class TestCFGIfElseBlock(TestCase):
    def test_success_block_getter(self):
        self.fail()

    def test_success_block_setter(self):
        self.fail()

    def test_success_block_deleter(self):
        self.fail()

    def test_fail_block_getter(self):
        self.fail()

    def test_fail_block_setter(self):
        self.fail()

    def test_fail_block_deleter(self):
        self.fail()

    def test_exit_block_getter(self):
        self.fail()

    def test_exit_block_setter(self):
        self.fail()

    def test_exit_block_deleter(self):
        self.fail()

    def test_accept(self):
        self.fail()

    def test_add_child(self):
        self.fail()

    def test_remove_child(self):
        self.fail()


class TestCFGLoopBlock(TestCase):
    def test_success_block_getter(self):
        self.fail()

    def test_success_block_setter(self):
        self.fail()

    def test_success_block_deleter(self):
        self.fail()

    def test_accept(self):
        self.fail()

    def test_add_child(self):
        self.fail()

    def test_remove_child(self):
        self.fail()


class TestCFGLoopElseBlock(TestCase):
    def test_success_block_getter(self):
        self.fail()

    def test_success_block_setter(self):
        self.fail()

    def test_success_block_deleter(self):
        self.fail()

    def test_fail_block_getter(self):
        self.fail()

    def test_fail_block_setter(self):
        self.fail()

    def test_fail_block_deleter(self):
        self.fail()

    def test_exit_block_getter(self):
        self.fail()

    def test_exit_block_setter(self):
        self.fail()

    def test_exit_block_deleter(self):
        self.fail()

    def test_accept(self):
        self.fail()

    def test_add_child(self):
        self.fail()

    def test_remove_child(self):
        self.fail()


class TestCFGSwitchBlock(TestCase):
    def test_case_blocks_getter(self):
        self.fail()

    def test_case_blocks_setter(self):
        self.fail()

    def test_case_blocks_deleter(self):
        self.fail()

    def test_exit_block_getter(self):
        self.fail()

    def test_exit_block_setter(self):
        self.fail()

    def test_exit_block_deleter(self):
        self.fail()

    def test_accept(self):
        self.fail()

    def test_add_child(self):
        self.fail()

    def test_remove_child(self):
        self.fail()


class TestCFGBreakBlock(TestCase):
    def test_accept(self):
        self.fail()

    def test_add_child(self):
        self.fail()

    def test_remove_child(self):
        self.fail()


class TestCFGContinueBlock(TestCase):
    def test_accept(self):
        self.fail()

    def test_add_child(self):
        self.fail()

    def test_remove_child(self):
        self.fail()
