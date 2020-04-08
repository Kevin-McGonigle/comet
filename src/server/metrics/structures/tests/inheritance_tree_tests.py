import unittest

from server.metrics.structures.inheritance_tree import InheritanceTree, InheritanceNode
from server.metrics.structures.results import CometNodeResult


class InheritanceTreeTestCase(unittest.TestCase):
    CLASS_A_TOKENS = ['class', 'A', '(', ')', ':', '\n', 'def', 'test', '(', ')', ':', '\n', 'pass', '\n', '\n']
    CLASS_B_TOKENS = ['class', 'B', '(', CometNodeResult('A', None, None), ')', ':', '\n', 'def', 'test_two', '(', 'x',
                      ',', 'y', ')', ':', '\n', 'pass', '\n']
    CLASS_C_TOKENS = ['class', 'C', '(', CometNodeResult('A', None, None), ',', CometNodeResult('B', None, None), ')',
                      ':', '\n', '    ', 'pass', '\n', '\n']

    def setUp(self):
        self.inheritance_tree = InheritanceTree()
        self.a_node = InheritanceNode(self.CLASS_A_TOKENS)
        self.b_node = InheritanceNode(self.CLASS_B_TOKENS)
        self.c_node = InheritanceNode(self.CLASS_C_TOKENS)

    def testAddNode(self):
        self.assertEqual(len(self.inheritance_tree.root.values()), 0)
        self.inheritance_tree.add_node(self.a_node)
        self.assertEqual(len(self.inheritance_tree.root.values()), 1)
        self.assertNotEqual(self.inheritance_tree.root[self.a_node], None)

    def testGetParentNode(self):
        self.inheritance_tree.add_node(self.a_node)
        self.inheritance_tree.add_node(self.b_node)
        self.inheritance_tree.add_node(self.c_node)

        self.assertEqual(self.inheritance_tree.get_parent_node(self.a_node), [])
        self.assertEqual(self.inheritance_tree.get_parent_node(self.b_node), ['A'])
        self.assertEqual(self.inheritance_tree.get_parent_node(self.c_node), ['A', 'B'])

    def testGetChildren(self):
        self.inheritance_tree.add_node(self.a_node)
        self.inheritance_tree.add_node(self.b_node)
        self.inheritance_tree.add_node(self.c_node)

        self.assertEqual(self.inheritance_tree.get_children(self.a_node), ['B', 'C'])
        self.assertEqual(self.inheritance_tree.get_children(self.b_node), ['C'])
        self.assertEqual(self.inheritance_tree.get_children(self.c_node), [])


if __name__ == "__main__":
    unittest.main()
