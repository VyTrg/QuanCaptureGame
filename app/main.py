import pygame as pg
from board import Board
from scoreBoard import ScoreBoard

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((1000, 600))
bg_image = pg.image.load('image/bg.png')
bg_image = pg.transform.scale(bg_image, screen.get_size())  
board = Board(screen)
scoreboard = ScoreBoard()
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            
            # Kiểm tra nếu người chơi đang chọn hướng từ mũi tên
            direction = board.handle_arrow_click(pos[0], pos[1])
            if direction:
                selected_tile = board.get_selected_tile_index()
                if selected_tile is not None and 0 <= selected_tile <= 5:
                    direction = 'left' if direction == 'right' else 'right'

                board.leftRight(direction, 1)
            else:
                # Nếu không phải click mũi tên thì chọn ô
                board.drawEnterdArea(pos[0], pos[1])
                board.show_arrows = True  # bật hiển thị mũi tên sau khi chọn ô
            
            print(pos[0], pos[1])

    
    screen.blit(bg_image, (0, 0))  
    board.draw()  
    scoreboard.draw(screen)
            
    pg.display.flip()
    # pg.display.update()
    clock.tick(60)                 
pg.quit()
