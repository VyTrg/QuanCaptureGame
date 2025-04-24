import pygame as pg
from board import Board
pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((1000, 600))
bg_image = pg.image.load('../image/bg.jpg')
bg_image = pg.transform.scale(bg_image, screen.get_size())  
board = Board(screen)
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.blit(bg_image, (0, 0))  
    board.draw()              
    pg.display.flip()
    clock.tick(60)                 
pg.quit()
