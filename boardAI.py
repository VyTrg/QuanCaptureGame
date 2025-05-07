from square import Square

class BoardAI:
    def __init__(self):
        self.squares = [None] * 14
        # Ô 0 và 6 là Quan: mỗi ô 5 quân Quan (value=5, is_mandarin=True)
        # Ô 1-5 và 7-11 là Dân: mỗi ô 5 quân Dân (value=5, is_mandarin=False)
        for i in range(12):
            if i == 0 or i == 6:
                self.squares[i] = Square(i, 10, True)
            else:
                self.squares[i] = Square(i, 5, False)
        # Ô 12 và 13 là điểm của 2 người chơi
        self.squares[12] = Square(12, 0, False)
        self.squares[13] = Square(13, 0, False)
        # Biến lưu trữ số quân mượn
        self.player1_borrowed = 0  # Người chơi 1 mượn
        self.player2_borrowed = 0  # Người chơi 2 mượn

    def display_board(self):
        print("\n" + "="*60)
        print("\t\tBÀN CỜ Ô ĂN QUAN")
        print("="*60)
        
        # Hiển thị ô Quan (0) và các ô của người chơi 1 (1-5)
        print(f"   [Quan:0]  ", end="")
        for i in range(1, 6):
            print(f"[Dân:{i}] ", end="")
        print(f"[Quan:6]")
        
        print(f"   ({self.squares[0].value:^5})  ", end="")
        for i in range(1, 6):
            print(f"({self.squares[i].value:^5}) ", end="")
        print(f"({self.squares[6].value:^5})")
        
        print(f"   {' '*8}  ", end="")
        for i in range(11, 6, -1):
            print(f"({self.squares[i].value:^5}) ", end="")
        print()
        
        print(f"   {' '*8}  ", end="")
        for i in range(11, 6, -1):
            print(f"[Dân:{i}] ", end="")
        print()
        
        print("\n" + "-"*60)
        print(f"Điểm AI (người chơi 1 - ô 12): {self.squares[12].value}")
        print(f"Điểm người chơi 2 (ô 13): {self.squares[13].value}")
        
        # Thông tin mượn quân
        if self.player1_borrowed > 0:
            print(f"AI đã mượn: {self.player1_borrowed} quân")
        if self.player2_borrowed > 0:
            print(f"Người chơi 2 đã mượn: {self.player2_borrowed} quân")
        
        # Hiển thị mảng trạng thái
        board_state = [self.squares[i].value for i in range(12)]
        print("\nBàn cờ (0-11):", board_state)
        
        # Tổng quân trên bàn
        player1_stones = sum(self.squares[i].value for i in range(1, 6))
        player2_stones = sum(self.squares[i].value for i in range(7, 12))
        print(f"Tổng quân AI (1-5): {player1_stones} quân")
        print(f"Tổng quân Người chơi 2 (7-11): {player2_stones} quân")
        print("="*60)

    def fill_if_empty(self, player_idx, enable_log=True):
        #check player1 (player_idx=0)
        if player_idx == 0 and not any(self.squares[i].value for i in range(1, 6)):
            # lay score hien tai cua player1
            current_score = self.squares[12].value
            
            if current_score >= 5:
                #truong hop du 5 quan de fill
                self.squares[12].value -= 5
                for i in range(1, 6):
                    self.squares[i].value = 1
                if enable_log:
                    print(f"player 1 du 5 diem de fill")
            else:
                #truong hop khong du quan-> muon quan
                borrowed = 5 - current_score
                self.player1_borrowed += borrowed
                
                #reset diem ve 0 vi muon quan tu doi thu
                self.squares[12].value = 0
                
                #fill lên cac o
                for i in range(1, 6):
                    self.squares[i].value = 1
                    
                if enable_log:
                    print(f"player1 co {current_score} diem và muon {borrowed} quan")
        
        # check player2 (player_idx=1)
        if player_idx == 1 and not any(self.squares[i].value for i in range(7, 12)):
            current_score = self.squares[13].value
            
            if current_score >= 5:
                self.squares[13].value -= 5
                for i in range(7, 12):
                    self.squares[i].value = 1
                if enable_log:
                    print(f"player 2 du 5 diem de fill")
            else:
                borrowed = 5 - current_score
                self.player2_borrowed += borrowed
                self.squares[13].value = 0
                for i in range(7, 12):
                    self.squares[i].value = 1
                if enable_log:
                    print(f"player2 co {current_score} diem và muon {borrowed} quan")

    def finished(self):
        # Kiem tra quan o 2 o Quan neu =0
        quan_empty = self.squares[0].value == 0 and self.squares[6].value == 0
        
        # Kiem tra neu mot ben khong con nuoc di hop le
        player1_moves = sum(1 for i in range(1, 6) if self.squares[i].value > 0)
        player2_moves = sum(1 for i in range(7, 12) if self.squares[i].value > 0)
        
        # Ket thuc neu mot ben het nuoc di va ben kia co it nhat mot o Quan da het
        player1_no_moves = player1_moves == 0
        player2_no_moves = player2_moves == 0
        
        # Ket thuc neu ca hai ben deu het nuoc di
        all_no_moves = player1_no_moves and player2_no_moves
        
        # Kiem tra neu tat ca cac o deu trong
        all_empty = all(self.squares[i].value == 0 for i in range(12))
        
        return quan_empty or all_empty or all_no_moves or (player1_no_moves and self.squares[0].value == 0) or (player2_no_moves and self.squares[6].value == 0)

    def move(self, start_pos, direction, player_idx, SLQuan=5, enable_log=True):
        # Kiểm tra nước đi hợp lệ
        if self.squares[start_pos].value == 0:
            if enable_log:
                print(f"Ô {start_pos} không có quân, không thể di chuyển!")
            return 0, [self.squares[i].value for i in range(12)]
        
        stones = self.squares[start_pos].value
        self.squares[start_pos].value = 0
        pos = start_pos
        score = 0
        eaten_info = []

        if enable_log:
            print(f"Người chơi {player_idx + 1} rải {stones} quân từ ô {start_pos}, {'phải' if direction == 1 else 'trái'}")
        
        # Hàm tính vị trí tiếp theo
        def next_position(current, dir):
            next_pos = (current + dir) % 12
            return next_pos
        
        # Bước 1: Rải quân đều cho tất cả các ô theo hướng đã chọn
        while stones > 0:
            pos = next_position(pos, direction)
            self.squares[pos].value += 1
            stones -= 1
            
        if enable_log:
            print(f"Kết thúc rải ở ô {pos}, có {self.squares[pos].value} quân")
        
        # Bước 2: Kiểm tra ăn quân hoặc tiếp tục rải
        continue_turn = True
        while continue_turn:
            next_pos = next_position(pos, direction)
            
            # Hiển thị thông tin về ô tiếp theo
            if enable_log:
                square_status = 'trống' if self.squares[next_pos].value == 0 else f'có {self.squares[next_pos].value} quân'
                square_type = 'Quan' if self.squares[next_pos].is_mandarin else 'Dân'
                print(f"Kiểm tra ô tiếp theo {next_pos} ({square_type}): {square_status}")
            
            # Kiểm tra nếu ô tiếp theo là ô Quan và có quân => kết thúc lượt
            if self.squares[next_pos].is_mandarin and self.squares[next_pos].value > 0:
                if enable_log:
                    print(f"Ô tiếp theo {next_pos} là ô Quan và có quân. Kết thúc lượt.")
                continue_turn = False
                break
            
            # Nếu ô tiếp theo trống (value=0)
            if self.squares[next_pos].value == 0:
                # Kiểm tra ô sau ô trống
                check_pos = next_position(next_pos, direction)
                sq = self.squares[check_pos]
                
                if enable_log:
                    check_status = 'trống' if sq.value == 0 else f'có {sq.value} quân'
                    check_type = 'Quan' if sq.is_mandarin else 'Dân'
                    print(f"Kiểm tra ô sau đó {check_pos} ({check_type}): {check_status}")
                
                # Nếu ô sau ô trống có quân thì ăn
                if sq.value > 0:
                    eaten_points = sq.value
                    score += eaten_points
                    sq.value = 0
                    
                    eaten_type = "Quan" if sq.is_mandarin else "Dân"
                    eaten_info.append(f"{eaten_points} quân {eaten_type} ở ô {check_pos}")
                    
                    if enable_log:
                        print(f"Ăn {eaten_points} quân {eaten_type} ở ô {check_pos}")
                    
                    if sq.is_mandarin and enable_log:
                        print(f"Ô {check_pos} là Quan và đã hết quân")
                    
                    # Sau khi ăn, cập nhật vị trí hiện tại và kiểm tra nếu có thể ăn tiếp
                    pos = check_pos
                    next_after_eaten = next_position(pos, direction)
                    
                    if enable_log:
                        next_status = 'trống' if self.squares[next_after_eaten].value == 0 else f'có {self.squares[next_after_eaten].value} quân'
                        next_type = 'Quan' if self.squares[next_after_eaten].is_mandarin else 'Dân'
                        print(f"Kiểm tra ô sau khi ăn {next_after_eaten} ({next_type}): {next_status}")
                    
                    # Kiểm tra ô sau khi ăn tiếp theo
                    if self.squares[next_after_eaten].value == 0:
                        # Nếu ô sau khi ăn tiếp theo trống, kiểm tra ô sau đó
                        next_check_pos = next_position(next_after_eaten, direction)
                        # Chỉ ăn quân nếu ô sau đó có quân
                        if self.squares[next_check_pos].value > 0:
                            continue
                        else:
                            if enable_log:
                                print("Dừng ăn quân vì ô sau ô trống không có quân")
                            continue_turn = False
                            break
                    else:
                        # Nếu ô sau khi ăn tiếp theo không trống, dừng ăn quân
                        if enable_log:
                            print("Dừng ăn quân vì ô tiếp theo không trống")
                        continue_turn = False
                        break
                else:
                    # Nếu ô sau ô trống không có quân, dừng lượt
                    if enable_log:
                        print("Không ăn quân vì ô sau ô trống cũng trống")
                    continue_turn = False
                    break
            else:
                # Nếu ô tiếp theo không trống và không phải Quan có quân
                # => Lấy quân từ ô này để rải tiếp
                stones = self.squares[next_pos].value
                self.squares[next_pos].value = 0
                pos = next_pos
                
                if enable_log:
                    print(f"Lấy {stones} quân từ ô {next_pos} để tiếp tục rải")
                
                # Rải quân lấy được
                while stones > 0:
                    pos = next_position(pos, direction)
                    self.squares[pos].value += 1
                    stones -= 1
                
                if enable_log:
                    print(f"Kết thúc rải ở ô {pos}, có {self.squares[pos].value} quân")
        
        # Tổng kết điểm ăn được
        if score > 0 and enable_log:
            print(f"Tổng điểm ăn được: {score} điểm: {', '.join(eaten_info)}")
        
        # Trả về điểm và trạng thái bàn cờ
        board_state = [self.squares[i].value for i in range(12)]
        return score, board_state

    def clone(self):
        new_board = BoardAI()
        for i in range(14):
            new_board.squares[i] = Square(
                self.squares[i].position,
                self.squares[i].value,
                self.squares[i].is_mandarin
            )
            # Sao chép thuộc tính is_eaten cho tất cả các ô
            new_board.squares[i].is_eaten = self.squares[i].is_eaten
        return new_board

    def final_score_adjustment(self):
        """Cập nhật điểm cuối cùng, trả lại số quân đã mượn"""
        # Trừ điểm người chơi nếu họ đã mượn quân
        if self.player1_borrowed > 0:
            self.squares[12].value -= self.player1_borrowed
            if self.squares[12].value < 0:
                self.squares[12].value = 0
        
        if self.player2_borrowed > 0:
            self.squares[13].value -= self.player2_borrowed
            if self.squares[13].value < 0:
                self.squares[13].value = 0
        
        return self.player1_borrowed, self.player2_borrowed