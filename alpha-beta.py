import math
import random

def generate_tree(depth, branching_factor):
    #tạo cây ngẫu nhiên với độ sâu và số nhánh con mỗi nút
    if depth == 0:
        return random.randint(-10, 10)  # Giá trị lá từ -10 đến 10
    
    return [generate_tree(depth - 1, branching_factor) for _ in range(branching_factor)]

def alpha_beta(node, depth, alpha, beta, maximizing_player):
    """Thuật toán Alpha-Beta Cắt Tỉa Nhánh."""
    if depth == 0 or isinstance(node, int):  # nếu đạt đến độ sâu tối đa hoặc là lá
        return node
    
    if maximizing_player:  # Người chơi MAX(AI)
        max_eval = -math.inf
        for child in node:  # Duyệt qua các nút con
            eval = alpha_beta(child, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:  # Cắt tỉa
                break
        return max_eval
    else:  # Người chơi MIN(người chơi)
        min_eval = math.inf
        for child in node:
            eval = alpha_beta(child, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:  # Cắt tỉa
                break
        return min_eval

# Tạo cây tìm kiếm ngẫu nhiên với độ sâu 3, mỗi nút có 3 nhánh con
random_tree = generate_tree(depth=3, branching_factor=3)

# Gọi thuật toán Alpha-Beta với độ sâu 3
best_value = alpha_beta(random_tree, 3, -math.inf, math.inf, True)

print("Cây trạng thái ngẫu nhiên:", random_tree)
print("Giá trị tốt nhất cho AI:", best_value)
