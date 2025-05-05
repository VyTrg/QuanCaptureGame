from treenode import TreeNode
from heuristic import heuristic

def minimax(node : TreeNode, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or node.is_leaf_node():
        return heuristic(node.data)
    
    if maximizingPlayer:
        maxEval = float('-inf')
        for child in node.children:
            eval = minimax (child, depth -1, False)
            maxEval = max(maxEval, eval)
        return maxEval
    else:
        minEval = float('inf')
        for child in node.children:
            eval = minimax (child, depth -1, True)
            minEval = min(minEval, eval)
        return minEval
