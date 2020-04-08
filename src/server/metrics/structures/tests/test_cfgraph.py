from unittest import TestCase

from server.metrics.structures.cfgraph import CFG


class TestCFG(TestCase):
    def setUp(self):
        with self.assertRaises(Exception):
            # noinspection PyArgumentList
            self.cfg = CFG()
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_node_count(self):
        self.fail()

    def test_edge_count(self):
        self.fail()


class TestCFGNode(TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_add_child(self):
        self.fail()

    def test_node_count(self):
        self.fail()

    def test_edge_count(self):
        self.fail()


class TestCFGIfNode(TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_add_child(self):
        self.fail()


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
