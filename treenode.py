class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []

    def is_leaf_node(self):
        if self.children == []:
            return True
        return False
