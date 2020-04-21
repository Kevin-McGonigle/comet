import itertools

from metrics.structures.tree import Node, Tree


class InheritanceTree(Tree):
    def __init__(self, tree=None):
        if tree is None:
            tree = {}
        super().__init__(tree)

    def add_node(self, node):
        self.root[node] = node.parent

    def get_parent_node(self, node):
        return [n.ast_node for n in self.root[node]]

    def get_children(self, parent_node):
        children = []
        for node in self.root:
            if parent_node.class_name in self.get_parent_node(node):
                children.append(node.class_name)
        return children

    def get_json(self):
        json_dict = {}
        for node in self.root:
            json_dict[node.class_name] = self.get_children(node)
        return json_dict

    def get_inheritance_depth(self):
        # Incorrect fix later
        return 1 + max([len(self.get_children(node)) for node in self.root])

    def __str__(self):
        return '\n'.join([f'Node: {node} Parent Node/s: {self.get_parent_node(node)} ' +
                          f'Children: {self.get_children(node)} Methods & Args: {node.methods}' for node in self.root])


class InheritanceNode(Node):
    def __init__(self, statements):
        self.class_name = statements[1]
        self.parent = parse_args(statements[3:])
        self.methods = generate_methods(statements)
        super().__init__(self.class_name)


def generate_methods(statements) -> dict:
    method_data = {}  # { method_name : { args: [], returns: []}}
    for i in range(len(statements)):
        if statements[i] == "def":
            method_name = statements[i + 1]  # ['def', 'add']
            method_args = parse_args(statements[i + 3:])  # ['def', 'add', '(', 'x', ',', 'y', ')']

            # def method_name () = 4, method_args, removed commas
            i += 4 + len(method_args) + len(method_args) - 1

            # Python 3.6: ['def', 'add', '(', 'x', ',', 'y', ')', '->', 'int']
            if statements[i] == "->":
                return_type = statements[i + 1]
                method_data[method_name] = {"args": method_args, "return": return_type.ast_node}
                i += 2
            else:
                method_data[method_name] = {"args": method_args}
        i += 1

    return method_data


def parse_args(arguments) -> list:
    """Parse method arguments.
    arguments:
    """
    # In line generator to avoid full population of list
    return list(itertools.takewhile(lambda token: token != ")", (arg for arg in arguments if arg != ",")))
