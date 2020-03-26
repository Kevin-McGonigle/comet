import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import unittest
from inheritance_tree import InheritanceTree, InheritanceNode

class InheritanceTreeTestCase(unittest.TestCase):
    CLASS_A_TOKENS = ['class', 'A', '(', ')', ':', '\n', '    ', 'pass', '\n', '\n']
    CLASS_B_TOKENS = ['class', 'B', '(', 'A', ')', ':', '\n', '    ', 'pass', '\n', '\n']
    CLASS_C_TOKENS = ['class', 'C', '(','A', ',' ,'B', ')', ':', '\n', '    ', 'pass', '\n', '\n']

    def setUp(self):
        self.inheritance_tree = InheritanceTree()
        self.a_node = InheritanceNode(self.CLASS_A_TOKENS)     
        self.b_node = InheritanceNode(self.CLASS_B_TOKENS)     
        self.c_node = InheritanceNode(self.CLASS_C_TOKENS)

    def testCorrectParsingOfClassArguments(self):
        assert(self.a_node.class_name == "A" and self.a_node.parent == [])
        assert(self.b_node.class_name == "B" and self.b_node.parent == ["A"])
        assert(self.c_node.class_name == "C" and self.c_node.parent == ["A", "B"])

    def testAddNode(self):
        assert(len(self.inheritance_tree.root.values()) == 0)
        self.inheritance_tree.add_node(self.a_node)
        assert(len(self.inheritance_tree.root.values()) > 0)
        assert(self.inheritance_tree.root[self.a_node] != None)

    def testGenerateCorrectInheritanceTree(self):
        self.inheritance_tree.add_node(self.a_node)
        self.inheritance_tree.add_node(self.b_node)
        self.inheritance_tree.add_node(self.c_node)

        assert(self.inheritance_tree.root[self.a_node] == [])
        assert(self.inheritance_tree.root[self.b_node] == ['A'])
        assert(self.inheritance_tree.root[self.c_node] == ['A', 'B'])

    def testGetChidren(self):
        self.inheritance_tree.add_node(self.a_node)
        self.inheritance_tree.add_node(self.b_node)

        a_children = self.inheritance_tree.get_children(self.a_node) 
        b_children = self.inheritance_tree.get_children(self.b_node)

        assert(a_children == ['B'])
        assert(b_children == [])

    def testGetParentNode(self):
        self.inheritance_tree.add_node(self.a_node)
        self.inheritance_tree.add_node(self.b_node)
        self.inheritance_tree.add_node(self.c_node)

        a_parent = self.inheritance_tree.get_parent_node(self.a_node)
        b_parent = self.inheritance_tree.get_parent_node(self.b_node)
        c_parent = self.inheritance_tree.get_parent_node(self.c_node)

        assert(a_parent == [])
        assert(b_parent == ['A'])
        assert(c_parent == ['A', 'B'])


if __name__ == "__main__":
    unittest.main()