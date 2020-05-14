from unittest import TestCase
from unittest.mock import patch

from metrics.structures.base.graph import Node
from metrics.structures.dependency_graph import DependencyGraph, Class, KnownClass, UnknownClass
from metrics.visitors.base.dependency_graph_visitor import DependencyGraphVisitor


class TestDependencyGraph(TestCase):
    """
    Dependency graph test case.
    """

    def test_base_getter(self) -> None:
        """
        Test getter for base property.
        """
        dependency_graph = DependencyGraph(Class())

        self.assertIs(dependency_graph.base, dependency_graph.root)

    def test_base_setter(self) -> None:
        """
        Test setter for base property.
        """
        dependency_graph = DependencyGraph(Class())

        new_base = Class()

        dependency_graph.base = new_base

        self.assertIs(dependency_graph.root, new_base)

    def test_base_deleter(self) -> None:
        """
        Test deleter for base property.
        """
        dependency_graph = DependencyGraph(Class())

        del dependency_graph.base

        with self.assertRaises(AttributeError):
            print(dependency_graph.root)

    @patch.object(Class, "accept")
    def test_accept(self, mock_accept) -> None:
        """
        Test accept method.

        :param mock_accept: Mock of Class's accept method.
        """
        visitor = DependencyGraphVisitor()

        base = Class()

        dependency_graph = DependencyGraph(base, [base])

        dependency_graph.accept(visitor)

        mock_accept.assert_called_with(visitor)

        base.accept.assert_called_with(visitor)


class TestClass(TestCase):
    """
    Dependency graph class node test case.
    """

    def test_dependencies_getter(self) -> None:
        """
        Test getter for dependencies property.
        """
        class_ = Class(dependencies=[Class()])

        self.assertIs(class_.dependencies, class_.children)

    def test_dependencies_setter(self) -> None:
        """
        Test setter for dependencies property.
        """
        class_ = Class()

        dependencies = [Class()]

        class_.dependencies = dependencies

        self.assertIs(class_.children, dependencies)

    def test_dependencies_deleter(self) -> None:
        """
        Test deleter for dependencies property.
        """
        class_ = Class()

        del class_.dependencies

        with self.assertRaises(AttributeError):
            print(class_.children)

    @patch.object(DependencyGraphVisitor, "visit_class")
    def test_accept(self, mock_visit_class) -> None:
        """
        Test accept method.

        :param mock_visit_class: Mock of DependencyGraphVisitor's visit_class method.
        """
        visitor = DependencyGraphVisitor()

        class_ = Class()

        class_.accept(visitor)

        mock_visit_class.assert_called_with(class_)

        visitor.visit_class.assert_called_with(class_)

    @patch.object(Node, "add_child")
    def test_add_dependency(self, mock_add_child) -> None:
        """
        Test add_dependency method.

        :param mock_add_child: Mock of Node's add_child method.
        """
        class_ = Class()

        dependency = Class()

        class_.add_dependency(dependency)

        mock_add_child.assert_called_with(dependency)

        class_.add_child.assert_called_with(dependency)

    @patch.object(Class, "add_dependency")
    def test_add_dependent(self, mock_add_dependency) -> None:
        """
        Test add_dependent method.

        :param mock_add_dependency: Mock of Class' add_dependency method.
        """
        class_ = Class()

        dependent = Class()

        class_.add_dependent(dependent)

        mock_add_dependency.assert_called_with(class_)

        dependent.add_dependency.assert_called_with(class_)


class TestKnownClass(TestCase):
    """
    Dependency graph known class node test case.
    """

    @patch.object(DependencyGraphVisitor, "visit_known_class")
    def test_accept(self, mock_visit_known_class) -> None:
        """
        Test accept method.

        :param mock_visit_known_class: Mock of DependencyGraphVisitor's visit_known_class method.
        """
        visitor = DependencyGraphVisitor()

        known_class = KnownClass()

        known_class.accept(visitor)

        mock_visit_known_class.assert_called_with(known_class)

        visitor.visit_known_class.assert_called_with(known_class)


class TestUnknownClass(TestCase):
    """
    Dependency graph unknown class node test case.
    """

    @patch.object(DependencyGraphVisitor, "visit_unknown_class")
    def test_accept(self, mock_visit_unknown_class) -> None:
        """
        Test accept method.

        :param mock_visit_unknown_class: Mock of DependencyGraphVisitor's visit_unknown_class method.
        """
        visitor = DependencyGraphVisitor()

        unknown_class = UnknownClass()

        unknown_class.accept(visitor)

        mock_visit_unknown_class.assert_called_with(unknown_class)

        visitor.visit_unknown_class.assert_called_with(unknown_class)
