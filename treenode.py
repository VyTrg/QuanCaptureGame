# from bigtree import BaseNode
# from data import Data
#
# class TreeNode(BaseNode):
#     def __init__(self, name, Data, parent=None):
#         self.name = name
#         self.data = Data
#         self.parent = parent
#
#     def is_leaf_node(self):
#         len(self.children) == 0


from bigtree import BaseNode

class TreeNode(BaseNode):
    def __init__(self, name, data, parent=None):
        super().__init__(name=name, parent=parent)  # Để BaseNode xử lý parent
        self.data = data  # Lưu trữ dữ liệu bổ sung
        
    def is_leaf_node(self):
        return len(self.children) == 0