from treenode import TreeNode
from heuristic import heuristic

def alpha_beta(node: TreeNode, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or node.is_leaf_node:
        
        return heuristic(node.data)

    if maximizingPlayer:
        maxEval = float('-inf')
        for child in node.children:
            eval = alpha_beta(child, depth - 1, alpha, beta, False)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if alpha >= beta:
                break  # cut beta
        return maxEval
    else:
        minEval = float('inf')
        for child in node.children:
            eval = alpha_beta(child, depth - 1, alpha, beta, True)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if alpha >= beta:
                break  # alpha cut
        return minEval