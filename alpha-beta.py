from treenode import TreeNode

def alpha_beta(node : TreeNode(), depth, alpha, beta, maximizingPlayer):
    if node.is_leaf_node or depth == 0:
        return node
    if maximizingPlayer:
        for child in node:
            alpha = max(alpha, alpha_beta(node, depth - 1, alpha, beta, False))
            if alpha >= beta:
                break
        return alpha
    else:
        for child in node:
            beta = max(beta,  alpha_beta(node, depth - 1, alpha, beta, False))
            if alpha >= beta:
                break
        return beta
