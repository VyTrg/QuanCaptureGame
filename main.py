from board import Board
from data import Data
from treenode import TreeNode
from alpha_beta import alpha_beta
from square import Square
from heuristic import heuristic, heuristic_with_lookahead

def create_game_tree(board, player, depth):
    squares = [square.value for square in board.squares]
    current_data = Data(player, board.squares[12].value, board.squares[13].value, squares)
    root = TreeNode("root", current_data)

    if player == 1:
        possible_moves = [(i, direction) for i in range(1, 6) for direction in ["left", "right"] if board.squares[i].value > 0]
    else:
        possible_moves = [(i, direction) for i in range(7, 12) for direction in ["left", "right"] if board.squares[i].value > 0]

    for move in possible_moves:
        pos, direction = move
        new_board = Board()
        for i in range(14):
            new_board.squares[i] = Square(i, board.squares[i].value, board.squares[i].is_mandarin)
            new_board.squares[i].is_eaten = board.squares[i].is_eaten
        if direction == "left":
            score = new_board.move(pos, -1, 0 if player == 1 else 1)
        else:
            score = new_board.move(pos, 1, 0 if player == 1 else 1)
        if player == 1:
            new_board.squares[12].value += score
        else:
            new_board.squares[13].value += score
        child_squares = [square.value for square in new_board.squares]
        child_data = Data(1 if player == 2 else 2, new_board.squares[12].value, new_board.squares[13].value, child_squares)
        child_node = TreeNode(f"{pos}-{direction}", child_data, parent=root)  # Gán parent để thêm vào cây

        if depth > 1:
            child_tree = create_game_tree(new_board, 1 if player == 2 else 2, depth - 1)
            for grandchild in child_tree.children:
                grandchild.parent = child_node  # Gán parent để thêm cháu vào node con

    return root

def ai_move(board, depth=2):
    tree = create_game_tree(board, 1, depth)
    best_value = float('-inf')
    best_move = None
    for child in tree.children:
        value = alpha_beta(child, depth, float('-inf'), float('inf'), False)
        if value > best_value:
            best_value = value
            best_move = child.name
    if best_move:
        pos, direction = best_move.split('-')
        pos = int(pos)
        print(f"AI chọn: ô {pos}, hướng {direction}")
        if direction == "left":
            score = board.move(pos, -1, 0, enable_log=True)
        else:
            score = board.move(pos, 1, 0, enable_log=True)
        board.squares[12].value += score
        return score
    return 0

def ai_move_with_lookahead(board, depth=2):
    """
    Sử dụng heuristic_with_lookahead để đánh giá trực tiếp các bước đi tiếp theo
    mà không cần xây dựng toàn bộ cây trò chơi.
    
    Parameters:
    - board: Đối tượng Board hiện tại
    - depth: Độ sâu xem trước (số bước đi tiếp theo cần xem xét)
    
    Returns:
    - Điểm đạt được sau nước đi
    """
    squares = [square.value for square in board.squares]
    current_data = Data(1, board.squares[12].value, board.squares[13].value, squares)
    
    # Tạo danh sách các nước đi khả thi của AI
    possible_moves = [(i, direction) for i in range(1, 6) 
                      for direction in ["left", "right"] 
                      if board.squares[i].value > 0]
    
    if not possible_moves:
        return 0
    
    best_value = float('-inf')
    best_move = None
    
    # Đánh giá mỗi nước đi bằng heuristic_with_lookahead
    for pos, direction_str in possible_moves:
        direction = -1 if direction_str == "left" else 1
        
        # Tạo bản sao của bàn cờ
        new_board = Board()
        for i in range(14):
            new_board.squares[i] = Square(i, board.squares[i].value, board.squares[i].is_mandarin)
            if hasattr(board.squares[i], 'is_eaten'):
                new_board.squares[i].is_eaten = board.squares[i].is_eaten
        
        # Thực hiện nước đi
        score = new_board.move(pos, direction, 0, enable_log=False)
        new_board.squares[12].value += score
        
        # Tạo dữ liệu mới và đánh giá bằng heuristic_with_lookahead
        new_squares = [square.value for square in new_board.squares]
        new_data = Data(2, new_board.squares[12].value, new_board.squares[13].value, new_squares)
        value = heuristic_with_lookahead(new_data, new_board, depth - 1)
        
        if value > best_value:
            best_value = value
            best_move = (pos, direction_str)
    
    if best_move:
        pos, direction = best_move
        print(f"AI chọn: ô {pos}, hướng {direction}")
        if direction == "left":
            score = board.move(pos, -1, 0, enable_log=True)
        else:
            score = board.move(pos, 1, 0, enable_log=True)
        board.squares[12].value += score
        return score
    return 0

def play_game(use_lookahead=False):
    board = Board()
    current_player = 1
    game_over = False

    print("\n" + "="*50)
    if use_lookahead:
        print("Sử dụng AI với heuristic đánh giá các bước đi tiếp theo!")
    else:
        print("Sử dụng AI với heuristic trạng thái tĩnh!")
    print("="*50 + "\n")

    while not game_over:
        board.display_board()
        if current_player == 1:
            print("Lượt của AI:")
            if use_lookahead:
                score = ai_move_with_lookahead(board, depth=2)
            else:
                score = ai_move(board)
            if score > 0:
                print(f"AI ăn được {score} điểm!")
            board.fill_if_empty(0)  # check và xin quân cho AI (người chơi 1)
            current_player = 2
        else:
            print("Lượt của bạn (người chơi 2, ô 7-11):")
            try:
                pos = input("Chọn ô (7-11): ")
                pos = int(pos)
                while pos < 7 or pos > 11 or board.squares[pos].value == 0:
                    print("Ô không hợp lệ hoặc không có quân! Chọn lại.")
                    pos = int(input("Chọn ô (7-11): "))
                direction = input("Chọn hướng (left/right): ").lower()
                while direction not in ["left", "right"]:
                    print("Hướng không hợp lệ! Chọn lại.")
                    direction = input("Chọn hướng (left/right): ")
                if direction == "left":
                    score = board.move(pos, -1, 1, enable_log=True)
                else:
                    score = board.move(pos, 1, 1, enable_log=True)
                board.squares[13].value += score
                if score > 0:
                    print(f"Bạn ăn được {score} điểm!")
                board.fill_if_empty(1)  #check và xin quân cho người chơi 2
                current_player = 1
            except ValueError:
                print("Vui lòng nhập số hợp lệ!")
                continue

        player1_stones = sum(board.squares[i].value for i in range(1, 6))
        player2_stones = sum(board.squares[i].value for i in range(7, 12))
        if board.finished() or (player1_stones == 0 and player2_stones == 0):
            game_over = True
            print("\nTrò chơi kết thúc!")
            board.display_board()
            print(f"Điểm AI: {board.squares[12].value}")
            print(f"Điểm người chơi: {board.squares[13].value}")
            if board.squares[12].value > board.squares[13].value:
                print("Kết quả: AI thắng!")
            elif board.squares[13].value > board.squares[12].value:
                print("Kết quả: Người chơi thắng!")
            else:
                print("Kết quả: Hòa!")

if __name__ == "__main__":
    print("\nChào mừng đến với trò chơi Ô Ăn Quan!")
    choice = input("Bạn có muốn bắt đầu trò chơi? (y/n): ").lower()
    if choice == 'y':
        ai_type = input("Chọn loại AI (1: Heuristic tĩnh, 2: Heuristic xét bước đi tiếp theo): ")
        use_lookahead = (ai_type == '2')
        play_game(use_lookahead)
    else:
        print("Tạm biệt!")