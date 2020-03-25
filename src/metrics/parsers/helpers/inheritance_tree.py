from .tree import Node, Tree
import itertools

class InheritanceTree(Tree):
    def __init__(self):
        super().__init__({})

    def add_node(self, node):
        self.root[node] = node.parent

    def get_parent_node(self, node):
        return [node.ast_node for node in self.root[node]]

    def get_children(self, parent_node):
        children = []
        for node in self.root:
            # Class -> [Inherits from mapping]
            if node == parent_node:
                continue
            if parent_node.name in [n.ast_node for n in self.root[node]]:
                children.append(node.name)

        return children
    
    def __str__(self):
        return '\n'.join([f'Node: {node} Parent Node/s: {self.get_parent_node(node)} ' +
            f'Children: {self.get_children(node)}' for node in self.root])
      

class InheritanceNode(Node):
    def __init__(self, statements):
        self.class_name = statements[1]
        # Don't like this: itertools O(X) + list comprehension O(N)
        self.parent =  list(itertools.takewhile(lambda token: token != ")", [statement for statement in statements[3:] if statement != ","]))
        super().__init__(self.class_name)
    
    