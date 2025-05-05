import pygame as pg
import sys


class Button:
    def __init__(self, text, x, y, width, height, callback):
        self.text = text
        self.text_color = (255, 255, 255)
        self.rect = pg.Rect(x, y, width, height)
        self.color = (0, 0, 0)
        self.callback = callback
        self.font = pg.font.SysFont(None, 40)

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.rect)
        pg.draw.rect(surface, (255, 255, 255), self.rect, 2)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()

def run_start_screen(screen, bg_image):
    clock = pg.time.Clock()
    running = True
    ai_option = None

    def start_game():
        nonlocal ai_option
        ai_option = run_ai_option_screen(screen, bg_image)
        running = False

    def quit_game():
        pg.quit()
        sys.exit()

    buttons = [
        Button("START", 400, 200, 200, 60, start_game),
        Button("QUIT", 400, 400, 200, 60, quit_game)
    ]

    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                for button in buttons:
                    button.check_click(pos)

        screen.blit(bg_image, (0, 0))
        for button in buttons:
            button.draw(screen)

        pg.display.flip()
        clock.tick(60)
    
    return ai_option  # hoặc trả về các lựa chọn đã chọn để dùng trong game chính

def run_ai_option_screen(screen, bg_image):
    clock = pg.time.Clock()
    running = True
    ai_option = None

    def select_minimax():
        nonlocal ai_option
        ai_option = "MINIMAX"
        print("Chọn AI: MINIMAX")
        running = False

    def select_alpha_beta():
        nonlocal ai_option
        ai_option = "ALPHA-BETA"
        print("Chọn AI: ALPHA-BETA")
        running = False

    buttons = [
        Button("MINIMAX", 400, 200, 200, 60, select_minimax),
        Button("ALPHA-BETA", 400, 300, 200, 60, select_alpha_beta)
    ]

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                for button in buttons:
                    button.check_click(pos)

        # Vẽ hình nền
        screen.blit(bg_image, (0, 0))

        # Vẽ các nút
        for button in buttons:
            button.draw(screen)

        pg.display.flip()
        clock.tick(60)
    
    return ai_option

