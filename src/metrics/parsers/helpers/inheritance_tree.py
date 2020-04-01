from .tree import Node, Tree
import itertools

class InheritanceTree(Tree):
    def __init__(self):
        super().__init__({})

    def add_node(self, node):
        self.root[node] = node.parent 
        
    def get_parent_node(self, node):
        return [node for node in self.root[node]]

    def get_children(self, parent_node):
        children = []
        for node in self.root:
            # Class -> [Inherits from mapping]
            if node == parent_node:
                continue
            if parent_node.name in [n for n in self.root[node]]:
                children.append(node.name)

        return children
    
    def __str__(self):
        return '\n'.join([f'Node: {node} Parent Node/s: {self.get_parent_node(node)} ' +
            f'Children: {self.get_children(node)} Methods & Args: {node.methods}' for node in self.root])
      

class InheritanceNode(Node):
    def __init__(self, statements):
        self.class_name = statements[1]
        self.parent =  self.parse_args(statements[3:])
        self.methods = self.generate_methods(statements)
        self.inherited_methods = {}
        super().__init__(self.class_name)            

    def generate_methods(self, statements):
        method_to_args = {}

        for i in range(len(statements)):
            if statements[i] == "def":
                method_name = statements[i + 1] # ['def', 'add', '(', 'x', ',', 'y', ')']
                method_args = self.parse_args(statements[i + 3:])
                method_to_args[method_name] = method_args
                # def method_name () = 4, method_args, removed commas
                i += 4 + len(method_args) + len(method_args) - 1
            i += 1
        return method_to_args

    def parse_args(self, arguments):
        # In line generator to avoid full population of list 
        return list(itertools.takewhile(lambda token: token != ")", (arg for arg in arguments if arg != ",")))