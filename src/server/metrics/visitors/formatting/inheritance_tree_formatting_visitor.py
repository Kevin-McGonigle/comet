from typing import List, Dict, Tuple

from metrics.visitors.base.inheritance_tree_visitor import InheritanceTreeVisitor


class InheritanceTreeFormattingVisitor(InheritanceTreeVisitor):
    """
    Inheritance tree formatting visitor.

    Provides functionality for visiting an inheritance tree and producing a list of classes and a list of links,
    both formatted for front-end request response.
    """

    def __init__(self):
        """
        Inheritance tree formatting visitor.
        """
        super().__init__()
        self._classes: List[Dict[str, str]] = []
        self._links: List[Dict[str, str]] = []

    def visit(self, tree) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
        """
        Visit an inheritance tree structure and return a list of classes and a list of links, formatted for front-end
        request response.

        :param tree: The inheritance tree to visit.
        :return: Formatted lists of classes and links respectively.
        """
        self._visited = []
        self._classes = []
        self._links = []

        tree.accept(self)

        return self._classes, self._links

    def visit_children(self, cls) -> None:
        """
        Visit each of a class' subclasses.

        :param cls: The parent class whose subclasses to visit.
        """
        if cls.subclasses:
            for subclass in cls.subclasses:
                subclass.accept(self)

    def visit_class(self, cls) -> None:
        """
        Visit a class.

        If the class has not yet been visited, add it to visited, add it to classes and add its subclass links.

        :param cls: The class to visit.
        """
        if cls not in self._visited:
            self._visited.append(cls)

            self._classes.append({"id": cls.name})

            if cls.subclasses:
                for subclass in cls.subclasses:
                    self._links.append({"source": cls.name, "target": subclass.name})

            self.visit_children(cls)
