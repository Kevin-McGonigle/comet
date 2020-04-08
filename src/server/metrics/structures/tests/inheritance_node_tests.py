import unittest

from server.metrics.structures.inheritance_tree import InheritanceNode
from server.metrics.structures.results import CometNodeResult


class InheritanceTreeTestCase(unittest.TestCase):
    CLASS_A_TOKENS = ['class', 'A', '(', ')', ':', '\n', 'def', 'test', '(', ')', ':', '\n', 'pass', '\n', '\n']
    CLASS_B_TOKENS = ['class', 'B', '(', 'A', ')', ':', '\n', 'def', 'test_two', '(', 'self', ',', 'x', ',', 'y', ')',
                      '->', CometNodeResult('int', None, None), ':', '\n', 'pass', '\n']
    CLASS_C_TOKENS = ['class', 'C', '(', 'A', ',', 'B', ')', ':', '\n', '    ', 'pass', '\n', '\n']

    def setUp(self):
        self.a_node = InheritanceNode(self.CLASS_A_TOKENS)
        self.b_node = InheritanceNode(self.CLASS_B_TOKENS)
        self.c_node = InheritanceNode(self.CLASS_C_TOKENS)

    def testCorrectParsingOfClassArguments(self):
        assert (self.a_node.class_name == "A" and self.a_node.parent == [])
        assert (self.a_node.methods == {"test": {"args": []}})

        assert (self.b_node.class_name == "B" and self.b_node.parent == ["A"])
        assert (self.b_node.methods == {"test_two": {"args": ["self", "x", "y"], "return": 'int'}})

        assert (self.c_node.class_name == "C" and self.c_node.parent == ["A", "B"])
        assert (self.c_node.methods == {})


if __name__ == "__main__":
    unittest.main()
