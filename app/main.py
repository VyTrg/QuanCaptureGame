import pygame as pg
from board import Board
from scoreBoard import ScoreBoard
from startScreen import run_start_screen

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((1000, 600))
bg_image = pg.image.load('image/bg.png')
bg_image = pg.transform.scale(bg_image, screen.get_size())  

ai_option = run_start_screen(screen, bg_image)
if ai_option is None:
    pg.quit()
    exit()

board = Board(screen)
scoreboard = ScoreBoard()
running = True
game_over = False


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONDOWN and not game_over:
            pos = pg.mouse.get_pos()
            
            # Kiểm tra nếu người chơi đang chọn hướng từ mũi tên
            direction = board.handle_arrow_click(pos[0], pos[1])
            if direction:
                selected_tile = board.get_selected_tile_index()
                if selected_tile is not None:
                    if (board.current_player == 1 and 1 <= selected_tile <= 5) or (board.current_player == 2 and 7 <= selected_tile <= 11):
                        if board.current_player == 1:
                            direction = 'left' if direction == 'right' else 'right'
                        if board.leftRight(direction, board.current_player, scoreboard):
                            if board.end_game(scoreboard):
                                game_over = True
                            #final_scores = board.calculate_final_socres
            else:
                # Nếu không phải click mũi tên thì chọn ô
                board.drawEnterdArea(pos[0], pos[1])
                board.show_arrows = True  # bật hiển thị mũi tên sau khi chọn ô
            
            print(pos[0], pos[1])

        # Kiểm tra và bổ sung quân nếu hàng trống
    if not game_over:
        board.check_and_replenish_empty_rows(scoreboard)
        if board.end_game(scoreboard):
            game_over = True
                #final_scores = board.calculate_final_scores()
                #scoreboard.set_final_scores(final_scores[0], final_scores[1])
    
    screen.blit(bg_image, (0, 0))  
    board.draw()  
    scoreboard.draw(screen)
            
    pg.display.flip()
    # pg.display.update()
    clock.tick(60)                 
pg.quit()
