import pygame as pg

class Board:
    def __init__(self, screen):
        self.screen = screen
        self.tile_size = 120
        self.rows = 2
        self.cols = 5

        self.entered_tiles = []

        self.square = pg.image.load(r"C:\Users\Lenovo\Desktop\GameAI\image\default.png")
        self.quan_trai = pg.image.load(r"C:\Users\Lenovo\Desktop\GameAI\image\quanTrai.png")
        self.quan_phai = pg.image.load(r"C:\Users\Lenovo\Desktop\GameAI\image\quanPhai.png")
        self.entered = pg.image.load(r"C:\Users\Lenovo\Desktop\GameAI\image\entered.png")
        # self.enteredRight = pg.image.load('../image/enteredRight.png')
        # self.enteredLeft = pg.image.load('../image/enteredLeft.png')
        self.arrow_left = pg.image.load(r"C:\Users\Lenovo\Desktop\GameAI\image\trai.png")
        self.arrow_right = pg.image.load(r"C:\Users\Lenovo\Desktop\GameAI\image\phai.png")
        self.stone = pg.image.load(r"C:\Users\Lenovo\Desktop\GameAI\image\stone.png")

        self.entered = pg.transform.scale(self.entered, (self.tile_size, self.tile_size))
        self.square = pg.transform.scale(self.square, (self.tile_size, self.tile_size))
        self.quan_trai = pg.transform.scale(self.quan_trai, (self.tile_size, self.tile_size * 2))
        self.quan_phai = pg.transform.scale(self.quan_phai, (self.tile_size, self.tile_size * 2))
        # self.enteredRight = pg.transform.scale(self.enteredRight, (self.tile_size, self.tile_size * 2))
        # self.enteredLeft = pg.transform.scale(self.enteredLeft, (self.tile_size, self.tile_size * 2))
        self.arrow_left = pg.transform.scale(self.arrow_left, (self.tile_size //2 -10, self.tile_size -20))
        self.arrow_right = pg.transform.scale(self.arrow_right, (self.tile_size// 2-10, self.tile_size -20))
        self.stone = pg.transform.scale(self.stone, (30,30))

    def draw(self):
       
        for col in range(self.cols):
            x = col * self.tile_size + 200
            y = 100
            self.screen.blit(self.square, (x, y))
            #vẽ stone
            for i in range(5):
                stone_x = x + (i%3) *40 +10
                stone_y = y + (i//3) * 40 +30
                self.screen.blit(self.stone, (stone_x, stone_y))
        
        for col in range(self.cols):
            x = (self.cols - 1 - col) * self.tile_size + 200
            y = 220
            self.screen.blit(self.square, (x, y))
                        #vẽ stone
            for i in range(5):
                stone_x = x + (i%3) *40 +10
                stone_y = y + (i//3) * 40 +30
                self.screen.blit(self.stone, (stone_x, stone_y))
            
        #mandarin draw for both sides
        self.screen.blit(self.quan_trai, (80, 100))
        self.screen.blit(self.quan_phai, (800, 100))

       
        if self.entered_tiles:
            self.screen.blit(self.entered, self.entered_tiles[0])
            tile_x, tile_y = self.entered_tiles[0]
            arrow_left_x = tile_x +5
            arrow_left_y = tile_y +10
            arrow_right_x = tile_x + self.tile_size // 2 + 5
            arrow_right_y = tile_y + 10
            self.screen.blit(self.arrow_left, (arrow_left_x, arrow_left_y))
            self.screen.blit(self.arrow_right, (arrow_right_x, arrow_right_y))


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

       
        if direction == "left":
            new_index = (current_index + steps) % 10
        elif direction == "right":
            new_index = (current_index - steps) % 10
        else:
            return

        
        if new_index < 5:
            new_x = new_index * self.tile_size + 200
            new_y = 100
        else:
            new_x = (9 - new_index) * self.tile_size + 200
            new_y = 220

        self.entered_tiles = [(new_x, new_y)]


