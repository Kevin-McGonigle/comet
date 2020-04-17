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
        """
        self.name = name
        self.children = children
        super().__init__()

    def __str__(self):
        s = self.name
        if len(self.children) > 0:
            for arg in self.children[:-1]:
                arg_s = str(arg).splitlines()
                s += f"\n|- {arg_s[0]}"
                if len(arg_s) > 1:
                    for line in arg_s[1:]:
                        s += f"\n|  {line}"
            if self.children[-1] is not None:
                arg_s = str(self.children[-1]).splitlines()
                s += f"\n`- {arg_s[0]}"
                if len(arg_s) > 1:
                    for line in arg_s[1:]:
                        s += f"\n   {line}"
        return s
