import pygame as pg
from board import Board
from scoreBoard import ScoreBoard
from boardAI import BoardAI
import mainAI
from startScreen import run_start_screen
pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((1000, 600))
bg_image = pg.image.load('image/bg.png')
bg_image = pg.transform.scale(bg_image, screen.get_size())  
board = Board(screen)
scoreboard = ScoreBoard()
boardAI =  BoardAI()
current_player = 1
running = True
game_over = False
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

        if event.type == pg.MOUSEBUTTONDOWN and not game_over and current_player == 2:
            pos = pg.mouse.get_pos()
            
            # Kiểm tra nếu người chơi đang chọn hướng từ mũi tên
            direction = board.handle_arrow_click(pos[0], pos[1])
            if direction:
                selected_tile = board.get_selected_tile_index()
                if selected_tile is not None:
                    if (board.current_player == 1 and 1 <= selected_tile <= 5) or (board.current_player == 2 and 7 <= selected_tile <= 11):
                        current_player = 1
                        if board.current_player == 1:
                            direction = 'left' if direction == 'right' else 'right'
                        if board.leftRight(direction, board.current_player, scoreboard):
                            print("Lượt của bạn (người chơi 2):")
                            if board.end_game(scoreboard):
                                game_over = True
                            #final_scores = board.calculate_final_socres
            else:
                # Nếu không phải click mũi tên thì chọn ô
                board.drawEnterdArea(pos[0], pos[1])
                board.show_arrows = True  # bật hiển thị mũi tên sau khi chọn ô
            
            print(pos[0], pos[1])
        elif current_player == 1:
            for i in range(0, 12):
                boardAI.squares[i].value = board.tiles[i]  # sao chép giá trị từ bàn cờ vào bàn cờ AI
            # boardAI.squares = board.tiles + board.scores
            print("Lượt của AI:")
            #dung thuat toan tu man hinh chon
            algorithm = ai_option.lower()
            board_state, score = mainAI.ai_move(boardAI, algorithm=algorithm)
            print(f"Sử dụng thuật toán: {ai_option}")
            
            # Hiển thị thông báo về thuật toán đang được sử dụng trên màn hình
            font = pg.font.SysFont(None, 30)
            algorithm_text = font.render(f"AI đang sử dụng thuật toán: {ai_option}", True, (255, 255, 255))
            screen.blit(algorithm_text, (20, 560))
            pg.display.update()
            pg.time.delay(1000)  # Hiển thị 1 giây để người chơi có thể đọc
            
            print(board_state)
            # board_state là mảng chứa giá trị của các ô từ 0-11
            board.draw_ai_move(board_state, score, scoreboard)  # Hiển thị nước đi của AI trên bàn cờ
        # Kiểm tra và bổ sung quân nếu hàng trống
            current_player = 2

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
