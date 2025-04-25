from bigtree import NodeMixin
from data import Data

class TreeNode(NodeMixin):
    def __init__(self, name, Data, parent=None):
        self.name = name
        self.data = Data
        self.parent = parent

    def is_leaf_node(self):
        len(self.children) == 0
