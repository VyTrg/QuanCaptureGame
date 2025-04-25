import pygame as pg

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

        self.entered = pg.transform.scale(self.entered, (self.tile_size, self.tile_size))
        self.square = pg.transform.scale(self.square, (self.tile_size, self.tile_size))
        self.quan_trai = pg.transform.scale(self.quan_trai, (self.tile_size, self.tile_size * 2))
        self.quan_phai = pg.transform.scale(self.quan_phai, (self.tile_size, self.tile_size * 2))
        # self.enteredRight = pg.transform.scale(self.enteredRight, (self.tile_size, self.tile_size * 2))
        # self.enteredLeft = pg.transform.scale(self.enteredLeft, (self.tile_size, self.tile_size * 2))

    def draw(self):
       
        for col in range(self.cols):
            x = col * self.tile_size + 200
            y = 100
            self.screen.blit(self.square, (x, y))
            
        
        for col in range(self.cols):
            x = (self.cols - 1 - col) * self.tile_size + 200
            y = 220
            self.screen.blit(self.square, (x, y))
            
        #mandarin draw for both sides
        self.screen.blit(self.quan_trai, (80, 100))
        self.screen.blit(self.quan_phai, (800, 100))

       
        if self.entered_tiles:
            self.screen.blit(self.entered, self.entered_tiles[0])

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


