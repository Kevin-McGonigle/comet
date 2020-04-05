class CometResult(object):
    def __init__(self, ast, cfg, inheritance_tree):
        self.ast = ast
        self.cfg = cfg
        self.inheritance_tree = inheritance_tree


class CometNodeResult(object):
    def __init__(self, ast_node, cfg_node, inheritance_node):
        self.ast_node = ast_node
        self.cfg_node = cfg_node
        self.inheritance_node = inheritance_node

    def __eq__(self, other):
        return isinstance(other, CometNodeResult) and self.ast_node == other.ast_node and self.cfg_node == other.cfg_node
