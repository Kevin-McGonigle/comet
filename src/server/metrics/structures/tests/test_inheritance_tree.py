from unittest import TestCase
from unittest.mock import patch, MagicMock

from metrics.structures.base.graph import Node
from metrics.structures.inheritance_tree import InheritanceTree, Class, KnownClass, UnknownClass


class TestInheritanceTree(TestCase):
    """
    Inheritance tree test case.
    """

    def test_base_getter(self) -> None:
        """
        Test getter for base property.
        """
        tree = InheritanceTree(Class())

        self.assertIs(tree.base, tree.root)

    def test_base_setter(self) -> None:
        """
        Test setter for base property.
        """
        tree = InheritanceTree(Class())

        tree.base = new_base = Class()

        self.assertIs(tree.root, new_base)

    def test_base_deleter(self) -> None:
        """
        Test deleter for base property.
        """
        tree = InheritanceTree(Class())

        del tree.base

        with self.assertRaises(AttributeError):
            print(tree.root)

    @patch("metrics.visitors.base.inheritance_tree_visitor.InheritanceTreeVisitor")
    @patch.object(Class, "accept")
    def test_accept(self, mock_accept: MagicMock, mock_visitor: MagicMock) -> None:
        """
        Test accept method.

        :param mock_accept: Mock of Class's accept method.
        :param mock_visitor: Mock of InheritanceTreeVisitor.
        """
        InheritanceTree(Class()).accept(mock_visitor)

        mock_accept.assert_called_with(mock_visitor)


class TestClass(TestCase):
    """
    Class test case.
    """

    def test_subclasses_getter(self) -> None:
        """
        Test getter for subclasses property.
        """
        class_ = Class(subclasses=[Class()])

        self.assertIs(class_.subclasses, class_.children)

    def test_subclasses_setter(self) -> None:
        """
        Test setter for subclasses property.
        """
        class_ = Class(subclasses=[])

        class_.subclasses = new_subclasses = [Class()]

        self.assertIs(class_.children, new_subclasses)

    def test_subclasses_deleter(self) -> None:
        """
        Test deleter for subclasses property.
        """
        class_ = Class(subclasses=[Class()])

        del class_.subclasses

        with self.assertRaises(AttributeError):
            print(class_.children)

    @patch("metrics.visitors.base.inheritance_tree_visitor.InheritanceTreeVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method.

        :param mock_visitor: Mock of InheritanceTreeVisitor.
        """
        class_ = Class()

        class_.accept(mock_visitor)

        mock_visitor.visit_class.assert_called_with(class_)

    @patch.object(Node, "add_child")
    def test_add_subclass(self, mock_add_child: MagicMock) -> None:
        """
        Test add_subclass method.
        
        :param mock_add_child: Mock of Node's add_child method.
        """
        subclass = Class()

        Class().add_subclass(subclass)

        mock_add_child.assert_called_with(subclass)

    @patch.object(Class, "add_subclass")
    def test_add_superclass(self, mock_add_subclass: MagicMock) -> None:
        """
        Test add_subclass method.

        :param mock_add_subclass: Mock of Class' add_subclass method.
        """
        class_ = Class()

        class_.add_superclass(Class())

        mock_add_subclass.assert_called_with(class_)


class TestKnownClass(TestCase):
    """
    Known class test case.
    """

    @patch("metrics.visitors.base.inheritance_tree_visitor.InheritanceTreeVisitor")
    def test_accept(self, mock_visitor) -> None:
        """
        Test accept method.

        :param mock_visitor: Mock of InheritanceTreeVisitor.
        """
        known_class = KnownClass("test")

        known_class.accept(mock_visitor)

        mock_visitor.visit_known_class.assert_called_with(known_class)


class TestUnknownClass(TestCase):
    """
    Unknown class test case.
    """

    @patch("metrics.visitors.base.inheritance_tree_visitor.InheritanceTreeVisitor")
    def test_accept(self, mock_visitor) -> None:
        """
        Test accept method.

        :param mock_visitor: Mock of InheritanceTreeVisitor.
        """
        unknown_class = UnknownClass()

        unknown_class.accept(mock_visitor)

        mock_visitor.visit_unknown_class.assert_called_with(unknown_class)


class TestMethod(TestCase):
    """
    Method test case.
    """

    pass


class TestParameter(TestCase):
    """
    Parameter test case.
    """

    pass


class TestPositionalArgumentsParameter(TestCase):
    """
    Positional arguments parameter test case.
    """

    pass


class TestKeywordArgumentsParameter(TestCase):
    """
    Keyword arguments parameter test case.
    """

    pass
