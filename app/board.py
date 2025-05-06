import pygame as pg
import math
class Board:
    def __init__(self, screen):
        self.screen = screen
        self.tile_size = 120
        self.rows = 2
        self.cols = 5

        self.entered_tiles = []
        self.current_player = 1  # Người chơi hiện tại (1 hoặc 2)
        self.scores = [0, 0]  # Điểm số (quân ăn được) của hai người chơi
        self.borrowed = [0, 0]
        self.square = pg.image.load('image/default.png')
        self.quan_trai = pg.image.load('image/quanTrai.png')
        self.quan_phai = pg.image.load('image/quanPhai.png')
        self.entered = pg.image.load('image/entered.png')
        # self.enteredRight = pg.image.load('../image/enteredRight.png')
        # self.enteredLeft = pg.image.load('../image/enteredLeft.png')
        self.stone = pg.image.load('image/stone.png')
        self.arrow_left = pg.image.load('image/trai.png')
        self.arrow_right = pg.image.load('image/phai.png')

        self.entered = pg.transform.scale(self.entered, (self.tile_size, self.tile_size))
        self.square = pg.transform.scale(self.square, (self.tile_size, self.tile_size))
        self.quan_trai = pg.transform.scale(self.quan_trai, (self.tile_size, self.tile_size * 2))
        self.quan_phai = pg.transform.scale(self.quan_phai, (self.tile_size, self.tile_size * 2))
        #self.enteredRight = pg.transform.scale(self.enteredRight, (self.tile_size, self.tile_size * 2))
        #self.enteredLeft = pg.transform.scale(self.enteredLeft, (self.tile_size, self.tile_size * 2))
        self.stone = pg.transform.scale(self.stone, (30, 30))
        self.arrow_left = pg.transform.scale(self.arrow_left, (40, 40))
        self.arrow_right = pg.transform.scale(self.arrow_right, (40, 40))
        self.show_arrows = False
        self.arrow_positions = {}


        # 10 ô thường, 2 ô quan
        self.tiles = [10] + [5] * 5 + [10] + [5] * 5

    def draw(self):
       
        for col in range(self.cols):
            x = col * self.tile_size + 200
            y = 100
            self.screen.blit(self.square, (x, y))
            self._draw_stones(x, y, self.tiles[col + 1])
        
        for col in range(self.cols):
            idx = 7 + col
            x = (self.cols - 1 - col) * self.tile_size + 200
            y = 220
            
            self.screen.blit(self.square, (x, y))
            self._draw_stones(x, y, self.tiles[idx])


        self.screen.blit(self.quan_trai, (80, 100))
        self.screen.blit(self.quan_phai, (800, 100))
        self._draw_stones(80, 100, self.tiles[0], is_mandarin=True)
        self._draw_stones(800, 100, self.tiles[6], is_mandarin=True)

        if self.entered_tiles and self.entered_tiles[0] != (80, 100) and self.entered_tiles[0] != (800, 100):
            self.screen.blit(self.entered, self.entered_tiles[0])

        if self.show_arrows and self.entered_tiles:
            tile_x, tile_y = self.entered_tiles[0]

            arrow_offset_y = self.tile_size // 2 - 20  
            left_arrow_x = tile_x - 50  
            right_arrow_x = tile_x + self.tile_size + 10 
            arrow_y = tile_y + arrow_offset_y

            self.screen.blit(self.arrow_left, (left_arrow_x, arrow_y))
            self.screen.blit(self.arrow_right, (right_arrow_x, arrow_y))

            self.arrow_positions["left"] = (left_arrow_x, arrow_y)
            self.arrow_positions["right"] = (right_arrow_x, arrow_y)


    def drawEnterdArea(self, x, y):
        for col in range(self.cols):
            tile_x = col * self.tile_size + 200
            tile_y = 100
            if tile_x <= x < tile_x + self.tile_size and tile_y <= y < tile_y + self.tile_size:
                index = col + 1
                if index !=0 and index != 6:
                    self.entered_tiles = [(tile_x, tile_y)]
                    self.selected_index = col + 1  # tiles[1] đến tiles[5]
                    self.show_arrows = True
                    return

        for col in range(self.cols):
            idx = 7 + col
            if idx == 6:
                continue
            tile_x = (self.cols - 1 - col) * self.tile_size + 200
            tile_y = 220
            if tile_x <= x < tile_x + self.tile_size and tile_y <= y < tile_y + self.tile_size:
                self.entered_tiles = [(tile_x, tile_y)]
                self.selected_index = idx
                self.show_arrows = True
                return
            
    def check_and_replenish_empty_rows(self, scoreboard):
        print("Kiểm tra hàng trống...")
        
        # Kiểm tra hàng trên (tiles[1-5])
        top_row_playable = any(self.tiles[i] > 0 for i in range(1, 6))
        if not top_row_playable:
            if self.scores[0] >= 5:
                print("Hàng trên không còn ô nào để rải, người chơi 1 rải 1 quân vào tiles[1-5]")
                for i in range(1, 6):
                    self.tiles[i] = 1
                self.scores[0] -= 5
                scoreboard.add_score(1, -5)
            elif self.scores[1] >= 5: # người chơi 1 mượn quân 
                for i in range(1,6):
                    self.tiles[i] = 1
                self.scores[1] -= 5
                self.borrowed[0] += 5
                scoreboard.add_score(2, -5)
            else:
                self.draw()
                pg.display.flip()
                pg.time.delay(500)

        # Kiểm tra hàng dưới (tiles[7-11])
        bottom_row_playable = any(self.tiles[i] > 0 for i in range(7, 12))
        if not bottom_row_playable:
            if self.scores[1] >= 5:
                print("Hàng dưới không còn ô nào để rải, người chơi 2 rải 1 quân vào tiles[7-11]")
                for i in range(7, 12):
                    self.tiles[i] = 1
                self.scores[1] -= 5
                scoreboard.add_score(2, -5)
            elif self.scores[0] >=5:
                for i in range(7, 12):
                    self.tiles[i] = 1
                self.scores[0] -= 5
                self.borrowed[1] += 5
                scoreboard.add_score(1, -5)
            else:
                self.draw()
                pg.display.flip()
                pg.time.delay(500)
        print(self.borrowed)
    # Hàm tính điểm cuối cùng, trừ đi số quân đã mượn
    def calculate_final_scores(self):
        top_row_stones = sum(self.tiles[1:6])
        self.scores[0] += top_row_stones
        print(f"Cộng {top_row_stones} quân từ hàng trên vào điểm AI")
        bottom_row_stones = sum(self.tiles[7:12])
        self.scores[1] += bottom_row_stones
        print(f"Cộng {bottom_row_stones} quân từ hàng dưới vào điểm PLAYER")
        
        for i in range(12):
            self.tiles[i] = 0
        # Trừ số quân đã mượn
        final_scores = [self.scores[0] - self.borrowed[0], self.scores[1] - self.borrowed[1]]
        print(f"Điểm cuối cùng - AI: {final_scores[0]}, PLAYER: {final_scores[1]}")
        return final_scores

    def leftRight(self, direction, player, scoreboard):
        if not self.entered_tiles or self.selected_index is None:
            return

        if self.selected_index == 0 or self.selected_index == 6:
            print("Không thể chọn ô quan!")
            self.entered_tiles = []
            self.selected_index = None
            self.show_arrows = False
            return 0

        # Kiểm tra ô được chọn có thuộc hàng của người chơi không
        if (player == 1 and not (1 <= self.selected_index <= 5)) or (player == 2 and not (7 <= self.selected_index <= 11)):
            print(f"Người chơi {player} không thể chọn ô {self.selected_index}!")
            self.entered_tiles = []
            self.selected_index = None
            self.show_arrows = False
            return False
        current_index = self.selected_index
        stones = self.tiles[current_index]
        if stones == 0:
            print(f"Ô {current_index} rỗng, không thể rải!")
            self.entered_tiles = []
            self.selected_index = None
            self.show_arrows = False
            return 0

        self.tiles[current_index] = 0

        total_tiles = 12
        pos = current_index
        step = 1 if direction == "left" else -1
        score = 0

        while True:
        # RẢI
            while stones > 0:
                pos = (pos + step + total_tiles) % total_tiles
                self.tiles[pos] += 1
                stones -= 1

            # Sau ăn, xem ô kế tiếp có quân và không phải ô quan
            next_pos = (pos + step + total_tiles) % total_tiles
            eat_pos = (next_pos + step + total_tiles) % total_tiles

            # Nếu ô kế tiếp là ô quan (0 hoặc 6), kết thúc lượt
            if next_pos == 0 or next_pos == 6:
                print(f"Ô kế tiếp là ô quan ({next_pos}), kết thúc lượt!")
                #self.check_and_replenish_empty_rows(scoreboard)  # Kiểm tra sau khi dừng lượt
                break

            # Trường hợp 1: Ô kế tiếp rỗng
            if self.tiles[next_pos] == 0:
                while self.tiles[next_pos] == 0:
                    if self.tiles[eat_pos] > 0:
                        print(f"Ăn quân ở ô {eat_pos} (sau ô rỗng)")
                        score += self.tiles[eat_pos]
                        self.tiles[eat_pos] = 0
                        pos = eat_pos
                       
                        next_pos = (pos + step + total_tiles) % total_tiles
                        eat_pos = (next_pos + step + total_tiles) % total_tiles

                        # Kiểm tra ô kế tiếp sau khi ăn
                        if next_pos == 0 or next_pos == 6:
                            print(f"Ô kế tiếp là ô quan ({next_pos}), kết thúc lượt!")
                            break
                    else:
                        break  # Không thể ăn tiếp
                break  # Kết thúc lượt sau khi ăn hoặc không ăn được
            # Trường hợp 2: Ô kế tiếp có quân
            elif self.tiles[next_pos] > 0 and next_pos != 0 and next_pos != 6:
                stones = self.tiles[next_pos]
                self.tiles[next_pos] = 0
                pos = next_pos
                
            else:
                break  # Không còn rải hay ăn tiếp nữa
        
        if player == 1:
            self.scores[0] += score
            scoreboard.add_score(1, score)
        else:
            self.scores[1] += score
            scoreboard.add_score(2, score)
        
        self.check_and_replenish_empty_rows(scoreboard)  # Kiểm tra sau khi dừng lượt
        self.draw()
        pg.display.flip()
        pg.time.delay(300)
        # Cập nhật con trỏ vị trí chọn
        if 1 <= pos <= 5:
            new_x = (pos - 1) * self.tile_size + 200
            new_y = 100
        elif 7 <= pos <= 11:
            new_x = (11 - pos) * self.tile_size + 200
            new_y = 220
        elif pos == 0:
            new_x, new_y = 80, 100
        elif pos == 6:
            new_x, new_y = 800, 100

        self.entered_tiles = [(new_x, new_y)]
        self.selected_index = pos
        self.show_arrows = False

        print(f"Trạng thái sau khi chơi: {self.tiles}")
        print(f"Điểm: AI = {self.scores[0]}, PLAYER = {self.scores[1]}")

        self.current_player = 2 if player == 1 else 1
        print(f"Chuyển lượt: Người chơi {self.current_player}")
        return False



    def _draw_stones(self, tile_x, tile_y, count, is_mandarin=False):
        if count == 0:
            return
        if is_mandarin:
            if count >=10:
                big_stone = pg.transform.scale(self.stone, (100, 100))
                stone_x = tile_x + (self.tile_size - big_stone.get_width()) // 2
                stone_y = tile_y + ((self.tile_size * 2) - big_stone.get_height()) // 2
                self.screen.blit(big_stone, (stone_x, stone_y))

                font = pg.font.SysFont(None, 36)
                text = font.render(str(count), True, (0, 0, 0))  # chữ trắng
                text_rect = text.get_rect(center=(tile_x + self.tile_size // 2, tile_y + self.tile_size // 2))
                self.screen.blit(text, text_rect)
            else:
                font = pg.font.SysFont(None, 36)
                text = font.render(str(count), True, (0, 0, 0))
                text_rect = text.get_rect(center=(tile_x + self.tile_size // 2, tile_y + self.tile_size))
                self.screen.blit(text, text_rect)
        else:
            if count < 10:
                center_x = tile_x + self.tile_size // 2
                center_y = tile_y + self.tile_size // 2
                radius = 35  # bán kính vòng tròn

                for i in range(count):
                    angle = 2 * math.pi * i / count
                    offset_x = int(math.cos(angle) * radius)
                    offset_y = int(math.sin(angle) * radius)
                    stone_x = center_x + offset_x - self.stone.get_width() // 2
                    stone_y = center_y + offset_y - self.stone.get_height() // 2
                    self.screen.blit(self.stone, (stone_x, stone_y))
            else:
                font = pg.font.SysFont(None, 48) 
                text = font.render(str(count), True, (0, 0, 0))
                text_rect = text.get_rect(center = (tile_x + self.tile_size // 2, tile_y + self.tile_size // 2))
                self.screen.blit(text, text_rect)

    def handle_arrow_click(self, x, y):
        for direction, pos in self.arrow_positions.items():
            arrow_x, arrow_y = pos
            arrow_rect = pg.Rect(arrow_x, arrow_y, 40, 40)
            if arrow_rect.collidepoint(x, y):
                self.show_arrows = False  # Ẩn mũi tên sau khi chọn
                return direction
        return None

    def get_selected_tile_index(self):
        if not self.entered_tiles:
            return None
        # return self.entered_tiles[0]

        selected_x, selected_y = self.entered_tiles[0]
        for idx in range(12):
            if idx >= 1 and idx <= 5:
                x = (idx - 1) * self.tile_size + 200
                y = 100
            elif idx >= 7 and idx <= 11:
                x = (11 - idx) * self.tile_size + 200
                y = 220
            elif idx == 0:
                x, y = 80, 100
            elif idx == 6:
                x, y = 800, 100
            else:
                continue
            if x <= selected_x < x + self.tile_size and y <= selected_y < y + self.tile_size:
                return idx
        return None

    def end_game(self, scoreboard):
        # Kiểm tra xem có ô nào còn quân không
        if all(tile == 0 for tile in self.tiles[1:12]):
            print("Game Over!")
            final_scores = self.calculate_final_scores()
            scoreboard.set_final_scores(final_scores[0], final_scores[1])
            return True
        elif self.tiles[0] == 0 and self.tiles[6] == 0:
            print("Game Over!")
            final_scores = self.calculate_final_scores()
            scoreboard.set_final_scores(final_scores[0], final_scores[1])
            return True
        return False
    

