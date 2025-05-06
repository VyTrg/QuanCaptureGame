import pygame as pg

class ScoreBoard:
    def __init__ (self):
        self.player1_score = 0
        self.player2_score = 0
        self.font = pg.font.SysFont(None, 40)
        self.game_over = False
        self.final_message = None

    def add_score (self, player, points):
        if player == 1:
            self.player1_score += points
        elif player == 2:
            self.player2_score += points
    def set_final_scores(self, player1_score, player2_score):
        # Cập nhật điểm cuối cùng và chuẩn bị thông báo trò chơi kết thúc
        self.player1_score = player1_score
        self.player2_score = player2_score
        self.game_over = True
        # Xác định người thắng
        if player1_score > player2_score:
            winner = "Player ai win!"
        elif player2_score > player1_score:
            winner = "Player win!"
        else:
            winner = "Hòa!"
        self.final_message = self.font.render(f"Trò chơi kết thúc! {winner}", True, (255, 0, 0))
    def draw (self, screen):
        #Hiển thị điểm người chơi 1
        text1 = self.font.render (f"PLAYER 1: {self.player1_score}", True, (0,0,0))
        text1_rect = text1.get_rect(center=(200, 520))
        pg.draw.ellipse(screen, (200, 200, 200), text1_rect.inflate(60, 40)) #khung elip màu xám nhạt
        screen.blit(text1, text1_rect)

        #Hiển thị điểm người chơi 2
        text2 = self.font.render (f"PLAYER 2: {self.player2_score}", True, (0,0,0))
        text2_rect= text2.get_rect( center = (800, 520))
        pg.draw.ellipse(screen, (200, 200, 200), text2_rect.inflate(60, 40 ))
        screen.blit(text2, text2_rect)

        # Hiển thị thông báo trò chơi kết thúc nếu có
        if self.game_over and self.final_message:
            message_rect = self.final_message.get_rect(center=(500, 300))
            pg.draw.rect(screen, (200, 200, 200), message_rect.inflate(20, 20))
            screen.blit(self.final_message, message_rect)