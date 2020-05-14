from unittest import TestCase
from unittest.mock import patch, NonCallableMock

from metrics.structures.base.graph import Node
from metrics.structures.inheritance_tree import InheritanceTree, Class, KnownClass, UnknownClass
from metrics.visitors.base.inheritance_tree_visitor import InheritanceTreeVisitor


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

        new_base = Class()

        tree.base = new_base

        self.assertIs(tree.root, new_base)

    def test_base_deleter(self) -> None:
        """
        Test deleter for base property.
        """
        tree = InheritanceTree(Class())

        del tree.base

        with self.assertRaises(AttributeError):
            print(tree.root)

    @patch.object(Class, "accept")
    def test_accept(self, mock_accept: NonCallableMock) -> None:
        """
        Test accept method.

        :param mock_accept: Mock of Class's accept method.
        """
        base = Class()

        tree = InheritanceTree(base)

        visitor = InheritanceTreeVisitor()

        tree.accept(visitor)

        mock_accept.assert_called_with(visitor)

        base.accept.assert_called_with(visitor)


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

        new_subclasses = [Class()]

        class_.subclasses = new_subclasses

        self.assertIs(class_.children, new_subclasses)

    def test_subclasses_deleter(self) -> None:
        """
        Test deleter for subclasses property.
        """
        class_ = Class(subclasses=[Class()])

        del class_.subclasses

        with self.assertRaises(AttributeError):
            print(class_.children)

    @patch.object(InheritanceTreeVisitor, "visit_class")
    def test_accept(self, mock_visit_class: NonCallableMock) -> None:
        """
        Test accept method.

        :param mock_visit_class: Mock of InheritanceTreeVisitor's visit_class method.
        """
        class_ = Class()

        visitor = InheritanceTreeVisitor()

        class_.accept(visitor)

        mock_visit_class.assert_called_with(class_)

        visitor.visit_class.assert_called_with(class_)

    @patch.object(Node, "add_child")
    def test_add_subclass(self, mock_add_child: NonCallableMock) -> None:
        """
        Test add_subclass method.
        
        :param mock_add_child: Mock of Node's add_child method.
        """
        class_ = Class()

        subclass = Class()

        class_.add_subclass(subclass)

        mock_add_child.assert_called_with(subclass)

        class_.add_child.assert_called_with(subclass)

    @patch.object(Class, "add_subclass")
    def test_add_superclass(self, mock_add_subclass: NonCallableMock) -> None:
        """
        Test add_subclass method.

        :param mock_add_subclass: Mock of Class add_subclass method.
        """
        class_ = Class()

        superclass = Class()

        class_.add_superclass(class_)

        mock_add_subclass.assert_called_with(class_)

        superclass.add_subclass.assert_called_with(class_)


class TestKnownClass(TestCase):
    """
    Known class test case.
    """

    @patch.object(InheritanceTreeVisitor, "visit_known_class")
    def test_accept(self, mock_visit_known_class) -> None:
        """
        Test accept method.

        :param mock_visit_known_class: Mock of InheritanceTreeVisitor's visit_known_class method.
        """
        known_class = KnownClass("test")

        visitor = InheritanceTreeVisitor()

        known_class.accept(visitor)

        mock_visit_known_class.assert_called_with(known_class)

        visitor.visit_known_class.assert_called_with(known_class)


class TestUnknownClass(TestCase):
    @patch.object(InheritanceTreeVisitor, "visit_unknown_class")
    def test_accept(self, mock_visit_unknown_class) -> None:
        """
        Test accept method.

        :param mock_visit_unknown_class: Mock of InheritanceTreeVisitor's visit_unknown_class method.
        """
        unknown_class = UnknownClass()

        visitor = InheritanceTreeVisitor()

        unknown_class.accept(visitor)

        mock_visit_unknown_class.assert_called_with(unknown_class)

        visitor.visit_unknown_class.assert_called_with(unknown_class)


class TestMethod(TestCase):
    pass


class TestParameter(TestCase):
    pass


class TestPositionalArgumentsParameter(TestCase):
    pass


class TestKeywordArgumentsParameter(TestCase):
    pass
