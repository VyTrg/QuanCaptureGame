import pygame as pg

class ScoreBoard:
    def __init__ (self):
        self.player1_score = 0
        self.player2_score = 0
        self.font = pg.font.SysFont(None, 40)
    
    def add_score (self, player, points):
        if player == 1:
            self.player1_score += points
        elif player == 2:
            self.player2_score += points

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
