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

        self.square = pg.image.load('../image/default.png')
        self.quan_trai = pg.image.load('../image/quanTrai.png')
        self.quan_phai = pg.image.load('../image/quanPhai.png')
        self.entered = pg.image.load('../image/entered.png')
        # self.enteredRight = pg.image.load('../image/enteredRight.png')
        # self.enteredLeft = pg.image.load('../image/enteredLeft.png')
        self.stone = pg.image.load('../image/stone.png')
        self.arrow_left = pg.image.load('../image/trai.png')
        self.arrow_right = pg.image.load('../image/phai.png')

        self.entered = pg.transform.scale(self.entered, (self.tile_size, self.tile_size))
        self.square = pg.transform.scale(self.square, (self.tile_size, self.tile_size))
        self.quan_trai = pg.transform.scale(self.quan_trai, (self.tile_size, self.tile_size * 2))
        self.quan_phai = pg.transform.scale(self.quan_phai, (self.tile_size, self.tile_size * 2))
        # self.enteredRight = pg.transform.scale(self.enteredRight, (self.tile_size, self.tile_size * 2))
        # self.enteredLeft = pg.transform.scale(self.enteredLeft, (self.tile_size, self.tile_size * 2))
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
        # Vẽ quân cờ ở ô quan
        
        self._draw_stones(80, 100, self.tiles[0], is_mandarin=True)
        self._draw_stones(800, 100, self.tiles[6], is_mandarin=True)
            
 
        if self.entered_tiles:
            self.screen.blit(self.entered, self.entered_tiles[0])

        if self.show_arrows and self.entered_tiles:
            tile_x, tile_y = self.entered_tiles[0]

            arrow_offset_y = self.tile_size // 2 - 20  # căn giữa theo chiều cao
            left_arrow_x = tile_x - 50  # cách trái 50px
            right_arrow_x = tile_x + self.tile_size + 10  # cách phải 10px
            arrow_y = tile_y + arrow_offset_y

            self.screen.blit(self.arrow_left, (left_arrow_x, arrow_y))
            self.screen.blit(self.arrow_right, (right_arrow_x, arrow_y))

            # Cập nhật vùng click mũi tên để xử lý click
            self.arrow_positions["left"] = (left_arrow_x, arrow_y)
            self.arrow_positions["right"] = (right_arrow_x, arrow_y)


    def drawEnterdArea(self, x, y):
        for col in range(self.cols):
            tile_x = col * self.tile_size + 200
            tile_y = 100
            if tile_x <= x < tile_x + self.tile_size and tile_y <= y < tile_y + self.tile_size:
                self.entered_tiles = [(tile_x, tile_y)]
                self.selected_index = col + 1  # tiles[1] đến tiles[5]
                self.show_arrows = True
                return

        for col in range(self.cols):
            idx = 7 + col
            tile_x = (self.cols - 1 - col) * self.tile_size + 200
            tile_y = 220
            if tile_x <= x < tile_x + self.tile_size and tile_y <= y < tile_y + self.tile_size:
                self.entered_tiles = [(tile_x, tile_y)]
                self.selected_index = idx
                self.show_arrows = True
                return
    
    def check_and_replenish_empty_rows(self):
        # Kiểm tra hàng trên (tiles[1-5])
        top_row_empty = all(self.tiles[i] == 0 for i in range(1, 6))
        if top_row_empty:
            print("Hàng trên trống, rải thêm 1 quân vào tiles[1-5]")
            for i in range(1, 6):
                self.tiles[i] = 1
            self.draw()
            pg.display.flip()
            pg.time.delay(500)  # Delay để người chơi thấy cập nhật

        # Kiểm tra hàng dưới (tiles[7-11])
        bottom_row_empty = all(self.tiles[i] == 0 for i in range(7, 12))
        if bottom_row_empty:
            print("Hàng dưới trống, rải thêm 1 quân vào tiles[7-11]")
            for i in range(7, 12):
                self.tiles[i] = 1
            self.draw()
            pg.display.flip()
            pg.time.delay(500)  # Delay để người chơi thấy cập nhật
    def leftRight(self, direction, player):
        if not self.entered_tiles or self.selected_index is None:
            return

        # Chỉ cho phép chọn ô thường (không phải ô quan 0 hoặc 6)
        if self.selected_index == 0 or self.selected_index == 6:
            print("Không thể chọn ô quan!")
            self.entered_tiles = []
            self.selected_index = None
            self.show_arrows = False
            return

        current_index = self.selected_index
        count = self.tiles[current_index]
        if count == 0:
            print(f"Ô {current_index} rỗng, không thể rải!")
            self.entered_tiles = []
            self.selected_index = None
            self.show_arrows = False
            return

        print(f"Người chơi {player} chọn ô {current_index}, số quân = {count}, hướng = {direction}")
        self.tiles[current_index] = 0  # Lấy hết quân
        total_tiles = 12
        i = current_index

        # Rải quân
        for _ in range(count):
            if direction == "left":
                i = (i + 1) % total_tiles
            elif direction == "right":
                i = (i - 1 + total_tiles) % total_tiles
            self.tiles[i] += 1
            print(f"Rải quân: i = {i}, tiles[{i}] = {self.tiles[i]}")
            self.draw()
            pg.display.flip()
            pg.time.delay(500)

        print(f"Trạng thái sau khi rải: {self.tiles}")

        # Kiểm tra và rải thêm quân nếu hàng trên hoặc dưới trống
        self.check_and_replenish_empty_rows()

        # Cập nhật ô được chọn
        if i >= 1 and i <= 5:
            new_x = (i - 1) * self.tile_size + 200
            new_y = 100
        elif i >= 7 and i <= 11:
            new_x = (11 - i) * self.tile_size + 200
            new_y = 220
        elif i == 0:
            new_x, new_y = 80, 100
        elif i == 6:
            new_x, new_y = 800, 100

        self.entered_tiles = [(new_x, new_y)]
        self.selected_index = i
        self.show_arrows = False

        # Chuyển lượt
        self.current_player = 2 if player == 1 else 1
        print(f"Lượt của người chơi {self.current_player}")



    def _draw_stones(self, tile_x, tile_y, count, is_mandarin=False):
        if is_mandarin:
            if count >=10:
                # Vien da lon
                big_stone = pg.transform.scale(self.stone, (100, 100))
                stone_x = tile_x + (self.tile_size - big_stone.get_width()) // 2
                stone_y = tile_y + ((self.tile_size * 2) - big_stone.get_height()) // 2
                self.screen.blit(big_stone, (stone_x, stone_y))

                font = pg.font.SysFont(None, 36)
                text = font.render(str(count), True, (0, 0, 0))  # chữ trắng
                text_rect = text.get_rect(center=(tile_x + self.tile_size // 2, tile_y + self.tile_size // 2))
                self.screen.blit(text, text_rect)
        else:

            if count <= 10:
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
