import pygame as pg
from board import Board
from scoreBoard import ScoreBoard

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((1000, 600))
bg_image = pg.image.load('../image/bg.jpg')
bg_image = pg.transform.scale(bg_image, screen.get_size())  
board = Board(screen)
scoreboard = ScoreBoard()
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            pos=pg.mouse.get_pos()
            board.drawEnterdArea(pos[0], pos[1])
            print(pos[0], pos[1])
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                board.leftRight("left", 1)
            if event.key == pg.K_RIGHT:
                board.leftRight("right", 1)
    
    screen.blit(bg_image, (0, 0))  
    board.draw()  
    scoreboard.draw(screen)
            
    pg.display.flip()
    # pg.display.update()
    clock.tick(60)                 
pg.quit()
