from boardAI import BoardAI
from data import Data
from treenode import TreeNode
from alpha_beta import alpha_beta
from square import Square
from minimax import minimax

def create_game_tree(board, player, depth):
    squares = [square.value for square in board.squares]
    current_data = Data(player, board.squares[12].value, board.squares[13].value, squares)
    root = TreeNode("root", current_data)

    # Xác định các nước đi có thể cho người chơi hiện tại
    if player == 1:  # AI - các ô 1-5
        possible_moves = [(i, direction) for i in range(1, 6) for direction in ["left", "right"] if board.squares[i].value > 0]
    else:  # Người chơi - các ô 7-11
        possible_moves = [(i, direction) for i in range(7, 12) for direction in ["left", "right"] if board.squares[i].value > 0]

    for move in possible_moves:
        pos, direction = move
        # Sử dụng phương thức clone() đã cải tiến để sao chép bàn cờ
        new_board = board.clone()
        
        # Thực hiện nước đi trên bản sao bàn cờ
        dir_value = -1 if direction == "left" else 1
        score, board_state = new_board.move(pos, dir_value, 0 if player == 1 else 1, enable_log=False)
        
        # Cập nhật điểm số
        if player == 1:
            new_board.squares[12].value += score
        else:
            new_board.squares[13].value += score
            
        # Tạo dữ liệu cho node con
        child_squares = [square.value for square in new_board.squares]
        child_data = Data(1 if player == 2 else 2, new_board.squares[12].value, new_board.squares[13].value, child_squares)
        child_node = TreeNode(f"{pos}-{direction}", child_data, parent=root)

        # Đệ quy tạo cây trò chơi cho các nước đi tiếp theo nếu chưa đạt đến độ sâu tối đa
        if depth > 1:
            # Tạo cây con cho người chơi tiếp theo
            next_player = 1 if player == 2 else 2
    return root

def ai_move(board, depth=2):
    tree = create_game_tree(board, 1, depth)
    best_value = float('-inf')
    best_move = None
    for child in tree.children:
        # Use alpha-beta pruning instead of minimax
        value = alpha_beta(child, depth, float('-inf'), float('inf'), False)
        if value > best_value:
            best_value = value
            best_move = child.name
    if best_move:
        pos, direction = best_move.split('-')
        pos = int(pos)
        print(f"AI chọn: ô {pos}, hướng {direction}")
        if direction == "left":
            score, board_state = board.move(pos, -1, 0, enable_log=True)
        else:
            score, board_state = board.move(pos, 1, 0, enable_log=True)
        board.squares[12].value += score
        
        # Trả về mảng một chiều chứa giá trị của các ô từ 0-11
        return board_state, score
    return [0] * 12  # Mảng mặc định nếu không tìm được nước đi tốt nhất

def play_game():
    board = BoardAI()
    current_player = 1
    game_over = False

    while not game_over:
        board.display_board()
        if current_player == 1:
            print("Lượt của AI:")
            board_state = ai_move(board)
            # board_state là mảng chứa giá trị của các ô từ 0-11
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
                    score, board_state = board.move(pos, -1, 1, enable_log=True)
                else:
                    score, board_state = board.move(pos, 1, 1, enable_log=True)
                board.squares[13].value += score
                board.fill_if_empty(1)  #check và xin quân cho người chơi 2
                current_player = 1
            except ValueError:
                print("Vui lòng nhập số hợp lệ!")
                continue

        # Kiểm tra điều kiện kết thúc trò chơi
        if board.finished():
            # Khi trò chơi kết thúc, cộng tất cả các quân còn lại cho người chơi tương ứng
            player1_stones = sum(board.squares[i].value for i in range(1, 6))
            player2_stones = sum(board.squares[i].value for i in range(7, 12))
            
            if player1_stones > 0:
                print(f"Trò chơi kết thúc, AI (người chơi 1) nhận thêm {player1_stones} điểm từ quân còn lại của mình.")
                board.squares[12].value += player1_stones
                # Đặt tất cả quân về 0
                for i in range(1, 6):
                    board.squares[i].value = 0
                    
            if player2_stones > 0:
                print(f"Trò chơi kết thúc, Người chơi 2 nhận thêm {player2_stones} điểm từ quân còn lại của mình.")
                board.squares[13].value += player2_stones
                # Đặt tất cả quân về 0
                for i in range(7, 12):
                    board.squares[i].value = 0
            
            game_over = True
            print("\nTrò chơi kết thúc!")
            
            #chinh lai diem da muon
            player1_borrowed, player2_borrowed = board.final_score_adjustment()
            if player1_borrowed > 0:
                print(f"AI da muon {player1_borrowed} quân")
            if player2_borrowed > 0:
                print(f"player da muon {player2_borrowed} quan")
            
            board.display_board()
            print(f"Điểm AI: {board.squares[12].value}")
            print(f"Điểm người chơi: {board.squares[13].value}")
            if board.squares[12].value > board.squares[13].value:
                print("Kết quả: AI thắng!")
            elif board.squares[13].value > board.squares[12].value:
                print("Kết quả: Người chơi thắng!")
            else:
                print("Kết quả: Hòa!")
        
        # Hiển thị thông tin về quân của hai bên
        player1_stones = sum(board.squares[i].value for i in range(1, 6))
        player2_stones = sum(board.squares[i].value for i in range(7, 12))
        
        # In thông tin về Quan
        print(f"Quan ở ô 0 có {board.squares[0].value} quân.")
        print(f"Quan ở ô 6 có {board.squares[6].value} quân.")
            
        # In thông tin về số quân còn lại
        print(f"AI còn {player1_stones} quân Dân.")
        print(f"Người chơi 2 còn {player2_stones} quân Dân.")
        
        # Cảnh báo khi một bên hết quân nhưng vẫn còn Quan
        if player1_stones == 0 and (board.squares[0].value > 0 or board.squares[6].value > 0):
            print("Người chơi 1 (AI) đã hết quân Dân nhưng vẫn còn ít nhất một ô Quan trên bàn cờ.")
        if player2_stones == 0 and (board.squares[0].value > 0 or board.squares[6].value > 0):
            print("Người chơi 2 đã hết quân Dân nhưng vẫn còn ít nhất một ô Quan trên bàn cờ.")

if __name__ == "__main__":
    choice = input("Do you want to start? (y/n): ").lower()
    if choice == 'y':
        play_game()
    else:
        print("Goodbye!")