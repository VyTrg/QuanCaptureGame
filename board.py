from square import Square

class Board:
    def __init__(self):
        self.squares = [None] * 14
        # Ô 0 và 6 là Quan: mỗi ô 5 quân Quan (value=5, is_mandarin=True)
        # Ô 1-5 và 7-11 là Dân: mỗi ô 5 quân Dân (value=5, is_mandarin=False)
        for i in range(12):
            if i == 0 or i == 6:
                self.squares[i] = Square(i, 5, True)
            else:
                self.squares[i] = Square(i, 5, False)
        # Ô 12 và 13 là điểm của 2 người chơi
        self.squares[12] = Square(12, 0, False)
        self.squares[13] = Square(13, 0, False)

    def display_board(self):
        print("\n" + "="*50)
        print("\t\tBÀN CỜ Ô ĂN QUAN")
        print("="*50)
        print(f"   ({'*' if self.squares[0].is_mandarin and not self.squares[0].is_eaten else ' '}{self.squares[0].value if not self.squares[0].is_eaten else ' '}*)  ", end=" ")
        for i in range(1, 6):
            print(f"[{self.squares[i].value:^2}]", end=" ")
        print(f"  ({'*' if self.squares[6].is_mandarin and not self.squares[6].is_eaten else ' '}{self.squares[6].value if not self.squares[6].is_eaten else ' '}*)")
        print(f"   ({'  '})  ", end=" ")
        for i in range(11, 6, -1):
            print(f"[{self.squares[i].value:^2}]", end=" ")
        print(f"  ({'  '})")
        print("\nĐiểm người chơi 1 (ô 12):", self.squares[12].value)
        print("Điểm người chơi 2 (ô 13):", self.squares[13].value)
        print("="*50)

    def fill_if_empty(self, player_idx):
        if player_idx == 0 and not any(self.squares[i].value for i in range(1, 6)):
            self.squares[12].value -= 5
            for i in range(1, 6):
                self.squares[i].value = 1
        if player_idx == 1 and not any(self.squares[i].value for i in range(7, 12)):
            self.squares[13].value -= 5
            for i in range(7, 12):
                self.squares[i].value = 1

    def finished(self):
        return self.squares[0].is_eaten and self.squares[6].is_eaten

    def move(self, start_pos, direction, player_idx, SLQuan=5, enable_log=True):
        stones = self.squares[start_pos].value
        self.squares[start_pos].value = 0
        pos = start_pos
        score = 0
        # rai quan deu
        while stones > 0:
            pos = (pos + direction) % 12
            self.squares[pos].value += 1
            stones -= 1
        # kiem tra an quan or tiep tuc rai quan
        while True:
            next_pos = (pos + direction) % 12
            if self.squares[next_pos].value == 0:
                check_pos = (next_pos + direction) % 12
                sq = self.squares[check_pos]
                if sq.value > 0:
                    # an quan o dan or mandarin roi + diem
                    score += sq.value
                    sq.value = 0
                    # neu an quan o mandarin thi set is_eaten
                    if sq.is_mandarin:
                        sq.is_eaten = True
                    # kiem tra co an tiep khong
                    pos = check_pos
                    next_after_eaten = (pos + direction) % 12
                    if self.squares[next_after_eaten].value == 0:
                        # neu o sau la o trong thi xet tiep
                        continue
                    else:
                        # khong phai o trong thi dung an
                        break
                else:
                    # het quan dung de an, break
                    break
            else:
                # lay quan o tiep theo ma rai
                stones = self.squares[next_pos].value
                self.squares[next_pos].value = 0
                pos = next_pos
                while stones > 0:
                    pos = (pos + direction) % 12
                    self.squares[pos].value += 1
                    stones -= 1
        return score

    def clone(self):
        new_board = Board()
        new_board.squares = [Square(sq.value, sq.is_mandarin) for sq in self.squares]
        # Copy thêm các thuộc tính khác nếu có
        return new_board