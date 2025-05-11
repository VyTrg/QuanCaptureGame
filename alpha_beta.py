from treenode import TreeNode
from heuristic import heuristic

def alpha_beta(node: TreeNode, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or node.is_leaf_node:
        
        return heuristic(node.data)
    node.sort_children(key=lambda x: heuristic(x.data), reverse=maximizingPlayer)  
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
    

def iterative_deepening_alpha_beta(root: TreeNode, max_depth: int, maximizingPlayer: bool = True):
    best_value = None
    # best_move = None

    for depth in range(1, max_depth + 1):
        value = alpha_beta(root, depth, float('-inf'), float('inf'), maximizingPlayer)
        best_value = value
        # print(f"Depth {depth}: Best value = {best_value}")

    return best_value