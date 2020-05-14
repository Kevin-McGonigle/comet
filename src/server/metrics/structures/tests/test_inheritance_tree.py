from unittest import TestCase


class TestInheritanceTree(TestCase):
    def test_base_getter(self):
        self.fail()

    def test_base_setter(self):
        self.fail()

    def test_base_deleter(self):
        self.fail()

    def test_accept(self):
        self.fail()


class TestClass(TestCase):
    def test_subclasses_getter(self):
        self.fail()

    def test_subclasses_setter(self):
        self.fail()

    def test_subclasses_deleter(self):
        self.fail()

    def test_accept(self):
        self.fail()

    def test_add_subclass(self):
        self.fail()

    def test_add_superclass(self):
        self.fail()


class TestKnownClass(TestCase):
    def test_accept(self):
        self.fail()


class TestUnknownClass(TestCase):
    def test_accept(self):
        self.fail()


class TestMethod(TestCase):
    pass


class TestParameter(TestCase):
    pass


class TestPositionalArgumentsParameter(TestCase):
    pass


class TestKeywordArgumentsParameter(TestCase):
    pass
