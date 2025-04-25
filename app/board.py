import pygame as pg
import math
class Board:
    def __init__(self, screen):
        self.screen = screen
        self.tile_size = 120
        self.rows = 2
        self.cols = 5

        self.entered_tiles = []

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
        # self.enteredRight = pg.transform.scale(self.enteredRight, (self.tile_size, self.tile_size * 2))
        # self.enteredLeft = pg.transform.scale(self.enteredLeft, (self.tile_size, self.tile_size * 2))
        self.stone = pg.transform.scale(self.stone, (30, 30))
        self.arrow_left = pg.transform.scale(self.arrow_left, (40, 40))
        self.arrow_right = pg.transform.scale(self.arrow_right, (40, 40))
        self.show_arrows = False
        self.arrow_positions = {}

        # khởi tạo số quân cờ mỗi ô (5 quân ở ô thường, 10 quân ở ô quan)
        self.stones_per_tile = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
        self.mandarin_left = 10
        self.mandarin_right = 10

    def draw(self):
       
        for col in range(self.cols):
            x = col * self.tile_size + 200
            y = 100
            self.screen.blit(self.square, (x, y))
            
        
        for col in range(self.cols):
            x = (self.cols - 1 - col) * self.tile_size + 200
            y = 220
            self.screen.blit(self.square, (x, y))

        # Vẽ quân cờ trên hàng trên (5 ô)
        for col in range(self.cols):
            x = col * self.tile_size + 200
            y = 100
            count = self.stones_per_tile[col]
            self._draw_stones(x, y, count)

        # Vẽ quân cờ trên hàng dưới (5 ô)
        for col in range(self.cols):
            idx = self.cols + col
            x = (self.cols - 1 - col) * self.tile_size + 200
            y = 220
            count = self.stones_per_tile[idx]
            self._draw_stones(x, y, count)

        # Vẽ quân cờ ở ô quan
        # self._draw_stones(80, 100, self.mandarin_left)
        # self._draw_stones(800, 100, self.mandarin_right)
        self._draw_stones(80, 100, self.mandarin_left, is_mandarin=True)
        self._draw_stones(800, 100, self.mandarin_right, is_mandarin=True)
            
        #mandarin draw for both sides
        self.screen.blit(self.quan_trai, (80, 100))
        self.screen.blit(self.quan_phai, (800, 100))

       
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
                return

        for col in range(self.cols):
            tile_x = (self.cols - 1 - col) * self.tile_size + 200
            tile_y = 220
            if tile_x <= x < tile_x + self.tile_size and tile_y <= y < tile_y + self.tile_size:
                self.entered_tiles = [(tile_x, tile_y)]
                return
    
    def leftRight(self, direction, steps):
        if not self.entered_tiles:
            return  

        current_x, current_y = self.entered_tiles[0]

        for idx in range(10):
            if idx < 5:
                tile_x = idx * self.tile_size + 200
                tile_y = 100
            else:
                tile_x = (9 - idx) * self.tile_size + 200
                tile_y = 220

            if current_x == tile_x and current_y == tile_y:
                current_index = idx
                break
        else:
            return 
        
        # Lấy số quân ở ô hiện tại
        count = self.stones_per_tile[current_index]
        if count == 0:
            return  # Không có quân để rải

        self.stones_per_tile[current_index] = 0  # Lấy hết quân khỏi ô hiện tại

        i = current_index
        for _ in range(count):
            if direction == "left":
                i = (i+1) % 10
            elif direction == "right":
                i = (i-1+10) % 10
            self.stones_per_tile[i] += 1  # Rải vào ô tiếp theo
        
        # Cập nhật vị trí khung chọn theo ô cuối cùng đã rải
        
        if i < 5:
            new_x = i * self.tile_size + 200
            new_y = 100
        else:
            new_x = (9 - i) * self.tile_size + 200
            new_y = 220

        self.entered_tiles = [(new_x, new_y)]
        self.show_arrows = False  # Tắt mũi tên sau khi rải


    def _draw_stones(self, tile_x, tile_y, count, is_mandarin=False):
        if is_mandarin and count >=10:
            # Vien da lon
            big_stone = pg.transform.scale(self.stone, (100, 100))
            stone_x = tile_x + (self.tile_size - big_stone.get_width()) // 2
            stone_y = tile_y + ((self.tile_size * 2) - big_stone.get_height()) // 2
            self.screen.blit(big_stone, (stone_x, stone_y))

            # font = pg.font.SysFont(None, 36)
            # text = font.render(str(count), True, (255, 255, 255))  # chữ trắng
            # text_rect = text.get_rect(center=(tile_x + self.tile_size // 2, tile_y + self.tile_size // 2))
            # self.screen.blit(text, text_rect)
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
