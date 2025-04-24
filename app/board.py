import pygame as pg

class Board:
    def __init__(self, screen):
        self.screen = screen
        self.tile_size = 120
        self.rows = 2
        self.cols = 5

        
        self.square = pg.image.load('../image/default.png')
        self.quan_trai = pg.image.load('../image/quanTrai.png')
        self.quan_phai = pg.image.load('../image/quanPhai.png')

        
        self.square = pg.transform.scale(self.square, (self.tile_size, self.tile_size))
        self.quan_trai = pg.transform.scale(self.quan_trai, (self.tile_size, self.tile_size * 2))
        self.quan_phai = pg.transform.scale(self.quan_phai, (self.tile_size, self.tile_size * 2))

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
