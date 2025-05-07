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
        print("\n" + "="*50)
        print("\t\tBÀN CỜ Ô ĂN QUAN")
        print("="*50)
        print(f"   ({'*'}{self.squares[0].value:>2}*)  ", end=" ")
        for i in range(1, 6):
            print(f"[{self.squares[i].value:^2}]", end=" ")
        print(f"  ({'*'}{self.squares[6].value:>2}*)")
        print(f"   ({'  '})  ", end=" ")
        for i in range(11, 6, -1):
            print(f"[{self.squares[i].value:^2}]", end=" ")
        print(f"  ({'  '})")
        print("\nĐiểm người chơi 1 (ô 12):", self.squares[12].value)
        print("Điểm người chơi 2 (ô 13):", self.squares[13].value)
        
        #hien thi mang
        board_state = [self.squares[i].value for i in range(12)]
        print("\nbàn cờ (0-11):", board_state)
        print("="*50)

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
        # kiem tra quan o 2 o Quan neu =0
        quan_empty = self.squares[0].value == 0 and self.squares[6].value == 0
        
        #kiem tra cac quan tren ban co
        all_empty = True
        for i in range(12):
            if self.squares[i].value > 0:
                all_empty = False
                break
        return quan_empty or all_empty

    def move(self, start_pos, direction, player_idx, SLQuan=5, enable_log=True):
        stones = self.squares[start_pos].value
        self.squares[start_pos].value = 0
        pos = start_pos
        score = 0
        eaten_info = []

        if enable_log:
            print(f"Người chơi {player_idx + 1} rải {stones} quân từ ô {start_pos}, {'phải' if direction == 1 else 'trái'}")
        
        # rai quan deu
        while stones > 0:
            pos = (pos + direction) % 12
            self.squares[pos].value += 1
            stones -= 1
            
        if enable_log:
            print(f"Kết thúc rải ở ô {pos}, có {self.squares[pos].value} quân")
        
        # kiem tra an quan or tiep tuc rai quan
        while True:
            next_pos = (pos + direction) % 12
            if enable_log:
                print(f"Kiểm tra ô tiếp theo {next_pos}: {'trống' if self.squares[next_pos].value == 0 else f'có {self.squares[next_pos].value} quân'}")
            
            #check o tiep theo la quan thi ket thuc luot
            if self.squares[next_pos].is_mandarin and self.squares[next_pos].value > 0:
                if enable_log:
                    print(f"Ô tiếp theo {next_pos} là ô Quan. Kết thúc lượt.")
                break
                
            if self.squares[next_pos].value == 0:
                check_pos = (next_pos + direction) % 12
                sq = self.squares[check_pos]
                
                if enable_log:
                    print(f"Kiểm tra ô sau đó {check_pos}: {'trống' if sq.value == 0 else f'có {sq.value} quân'}")
                
                if sq.value > 0:
                    # an quan o dan or mandarin roi + diem
                    eaten_points = sq.value
                    score += eaten_points
                    sq.value = 0
                    
                    eaten_type = "Quan" if sq.is_mandarin else "Dân"
                    eaten_info.append(f"{eaten_points} quân {eaten_type} ở ô {check_pos}")
                    
                    if enable_log:
                        print(f"Ăn {eaten_points} quân {eaten_type} ở ô {check_pos}")
                    
                    # neu an quan o mandarin thi set is_eaten
                    if sq.is_mandarin and enable_log:
                        print(f"Ô {check_pos} là Quan và đã hết quân")
                    
                    # kiem tra co an tiep khong
                    pos = check_pos
                    next_after_eaten = (pos + direction) % 12
                    
                    if enable_log:
                        print(f"Kiểm tra ô sau khi ăn {next_after_eaten}: {'trống' if self.squares[next_after_eaten].value == 0 else f'có {self.squares[next_after_eaten].value} quân'}")
                    
                    if self.squares[next_after_eaten].value == 0:
                        # neu o sau la o trong thi xet tiep
                        if enable_log:
                            print("Tiếp tục kiểm tra ăn quân")
                        continue
                    else:
                        # khong phai o trong thi dung an
                        if enable_log:
                            print("Dừng ăn quân vì ô tiếp theo không trống")
                        break
                else:
                    if enable_log:
                        print("Không ăn quân vì ô tiếp theo là trống")
                    break
            else:
                # lay quan o tiep theo ma rai
                stones = self.squares[next_pos].value
                self.squares[next_pos].value = 0
                pos = next_pos
                
                if enable_log:
                    print(f"Lấy {stones} quân từ ô {next_pos} để tiếp tục rải")
                
                while stones > 0:
                    pos = (pos + direction) % 12
                    self.squares[pos].value += 1
                    stones -= 1
                
                if enable_log:
                    print(f"ket thuc rai o {pos}, co {self.squares[pos].value} quan")
    
        #tong diem an duco
        if score > 0 and enable_log:
            print(f"tong diem an duoc {score} diem: {', '.join(eaten_info)}")
        board_state = [self.squares[i].value for i in range(12)]
        
        #tra ve score va mang
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

    def final_score_adjustment(self):#tra lai so quan da muon
        self.squares[12].value -= self.player1_borrowed
        self.squares[13].value += self.player1_borrowed

        self.squares[13].value -= self.player2_borrowed
        self.squares[12].value += self.player2_borrowed
        
        return self.player1_borrowed, self.player2_borrowed