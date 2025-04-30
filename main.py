from board import Board
from data import Data
from treenode import TreeNode
from alpha_beta import alpha_beta
from square import Square

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
        # Copy state
        for i in range(14):
            new_board.squares[i].value = board.squares[i].value
            if hasattr(board.squares[i], 'is_eaten'):
                new_board.squares[i].is_eaten = board.squares[i].is_eaten
        # Thực hiện nước đi
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
        child_node = TreeNode(f"{pos}-{direction}", child_data)  
        child_node.parent = root

        if depth > 1:
            child_tree = create_game_tree(new_board, 1 if player == 2 else 2, depth - 1)
            for grandchild in child_tree.children:
                grandchild.parent = child_node

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
    return board

def play_game():
    board = Board()
    current_player = 1
    game_over = False

    while not game_over:
        board.display_board()

        if current_player == 1:
            print("Lượt của AI:")
            board = ai_move(board)
            current_player = 2
        else:
            print("Lượt của bạn (người chơi 2, ô 7-11):")
            pos = int(input("Chọn ô (7-11): "))
            while pos < 7 or pos > 11 or board.squares[pos].value == 0:
                print("Ô không hợp lệ hoặc không có quân! Chọn lại.")
                pos = int(input("Chọn ô (7-11): "))

            direction = input("Chọn hướng (left/right): ").lower()
            while direction not in ["left", "right"]:
                print("Hướng không hợp lệ! Chọn lại.")
                direction = input("Chọn hướng (left/right): ").lower()

            if direction == "left":
                score = board.move(pos, -1, 1)
            else:
                score = board.move(pos, 1, 1)
            board.squares[13].value += score
            current_player = 1

        player1_stones = sum(board.squares[i].value for i in range(1, 6))
        player2_stones = sum(board.squares[i].value for i in range(7, 12))
        if player1_stones == 0 and player2_stones == 0:
            game_over = True
            board.display_board()
            print("Trò chơi kết thúc!")
            print(f"Điểm AI: {board.squares[12].value}")
            print(f"Điểm người chơi: {board.squares[13].value}")
            if board.squares[12].value > board.squares[13].value:
                winner = "AI"
            elif board.squares[13].value > board.squares[12].value:
                winner = "Người chơi"
            else:
                winner = "Hòa"
            print(f"Kết quả: {winner} thắng!")

def test_het_quan():
    from board import Board
    board = Board()
    for i in range(7, 12):
        board.squares[i].value = 0
    print("\n[TEST] Trường hợp hết quân ở dãy dân người chơi 2:")
    board.display_board()


def test_xin_quan():
    from board import Board
    board = Board()
    for i in range(7, 12):
        board.squares[i].value = 0
    board.squares[13].value = 3  # Điểm người chơi 2 chỉ còn 3
    print("\n[TEST] Trường hợp xin quân:")
    board.display_board()


def test_an_lien_tiep():
    from board import Board
    board = Board()
    for i in range(7, 12):
        board.squares[i].value = 0
    board.squares[8].value = 5
    board.squares[10].value = 5
    board.squares[7].value = 1  # Người chơi 2 đi từ ô 7
    print("\n[TEST] Trường hợp ăn liên tiếp nhiều ô:")
    score = board.move(7, 1, 1)
    print("Điểm ăn được:", score)
    board.display_board()


def test_ket_thuc_game():
    from board import Board
    board = Board()
    for i in range(1, 6):
        board.squares[i].value = 0
    for i in range(7, 12):
        board.squares[i].value = 0
    board.squares[12].value = 10
    board.squares[13].value = 15
    print("\n[TEST] Trường hợp kết thúc game:")
    board.display_board()


if __name__ == "__main__":
    choice = input("Do u want start? (y/n): ").lower()
    if choice == 'y':
        play_game()
    else:
        print("pai!")
    test_het_quan()
    test_xin_quan()
    test_an_lien_tiep()
    test_ket_thuc_game()
