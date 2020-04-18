class Tree(object):
    def __init__(self, root=None):
        """
        Initialise a generic tree.
        :param root: The root node of the tree.
        :type root: Node
        """
        self.root = root
        super().__init__()

    def __str__(self):
        return str(self.root)


class Node(object):
    def __init__(self, name, *children):
        """
        Initialise a generic tree node.
        :param name: The name of the node.
        :type name: str
        :param children: The child nodes of the node.
        :type children: Node or str
        """
        self.name = name
        self.children = children
        super().__init__()

    def __str__(self):
        s = self.name
        if len(self.children) > 0:
            for child in self.children[:-1]:
                if child:
                    child_branches = str(child).splitlines()
                    s += f"\n|- {child_branches[0]}"
                    if len(child_branches) > 1:
                        for line in child_branches[1:]:
                            s += f"\n|  {line}"
            if self.children[-1]:
                final_child_branches = str(self.children[-1]).splitlines()
                s += f"\n`- {final_child_branches[0]}"
                if len(final_child_branches) > 1:
                    for line in final_child_branches[1:]:
                        s += f"\n   {line}"
        return s
