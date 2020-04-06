from unittest import TestCase

from metrics.structures.cfgraph import *


class TestCFG(TestCase):
    def setUp(self):
        super().setUp()
        with self.assertRaises(Exception):
            # noinspection PyArgumentList
            self.cfg = CFG()

    def tearDown(self):
        super().tearDown()

    def test_node_count(self):
        self.fail()

    def test_edge_count(self):
        self.fail()


class TestCFGNode(TestCase):
    def setUp(self):
        super().setUp()
        self.cfg_node = CFGNode()

    def tearDown(self):
        super().tearDown()

    def test_add_child(self):
        self.assertEqual(len(self.cfg_node.children), 0)

        child_node = CFGNode()
        self.cfg_node.add_child(child_node)

        self.assertEqual(len(self.cfg_node.children), 1)
        self.assertIn(child_node, self.cfg_node.children)

        with self.assertRaises(ValueError):
            self.cfg_node.add_child(child_node)

        self.assertEqual(self.cfg_node.children.count(child_node), 1)

    def test_node_count(self):
        self.assertEqual(self.cfg_node.node_count(), 1)

        child_node = CFGNode()
        self.cfg_node.add_child(child_node)

        self.assertEqual(self.cfg_node.node_count(), 2)

        self.cfg_node.children[0].add_child(self.cfg_node)

        self.assertEqual(self.cfg_node.node_count(), 2)

    def test_edge_count(self):
        self.assertEqual(self.cfg_node.edge_count(), 0)

        child_node1 = CFGNode()
        child_node2 = CFGNode()

        self.cfg_node.add_child(child_node1)
        self.cfg_node.add_child(child_node2)

        self.assertEqual(self.cfg_node.edge_count(), 2)

        child_node1.add_child(self.cfg_node)

        self.assertEqual(self.cfg_node.edge_count(), 3)


class TestCFGIfNode(TestCase):
    def setUp(self):
        super().setUp()

        success_block = CFGNode()
        exit_block = CFGNode()

        self.if_node = CFGIfNode(success_block, exit_block)

        self.assertEqual(self.if_node.edge_count(), 3)
        self.assertEqual(self.if_node.node_count(), 3)

        self.assertEqual(self.if_node.success_block, success_block)
        self.assertEqual(self.if_node.exit_block, exit_block)

        self.assertIn(success_block, self.if_node.children)
        self.assertIn(exit_block, self.if_node.children)
        self.assertIn(exit_block, success_block.children)

    def tearDown(self):
        super().tearDown()

    def test_add_child(self):
        child_node = CFGNode()
        self.if_node.add_child(child_node)

        self.assertEqual(self.if_node.node_count(), 4)
        self.assertEqual(self.if_node.edge_count(), 4)

        self.assertIn(child_node, self.if_node.exit_block.children)


class TestCFGIfElseNode(TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()


class TestCFGWhileNode(TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_add_child(self):
        self.fail()


class TestCFGWhileElseNode(TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()


class TestCFGBreakNode(TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()
