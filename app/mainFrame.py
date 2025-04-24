import sys
import pygame as pg

clock = pg.time.Clock()
screen = pg.display.set_mode((1000, 600))
pg.init()
pg.font.init()
font = pg.font.Font(None, 30)
surface = pg.Surface((1000, 600),pg.SRCALPHA)
pg.display.set_caption("Main Frame") 
bg_image = pg.image.load('./image/bg.jpg')
menu_image = pg.image.load('./image/menudefault.png')
BUTTON_COLOR =(255,255,255)
button=pg.Rect(400, 200, 200, 30)
button1=pg.Rect(400, 300, 200, 30)
button2=pg.Rect(400, 400, 200, 30)
button_text="Easy"
button1_text= "Normal"
button2_text="Hard"
def draw():
    
    pg.draw.rect(surface, BUTTON_COLOR,button,2)
    pg.draw.rect(surface, BUTTON_COLOR,button1,2)
    pg.draw.rect(surface, BUTTON_COLOR,button2,2)
    text_surface=font.render(button_text, True, (255, 255, 255))
    text_react=text_surface.get_rect(center=button.center)
    screen.blit(text_surface, text_react)
    text_surface1 = font.render(button1_text, True, (255, 255, 255))
    text_react1=text_surface1.get_rect(center=button1.center)
    screen.blit(text_surface1, text_react1)
    text_surface2 = font.render(button2_text, True, (255, 255, 255))
    text_react2=text_surface2.get_rect(center=button2.center)
    screen.blit(text_surface2, text_react2)

while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            sys.exit()
    
    screen.blit(bg_image, (0, 0))  
    screen.blit(menu_image, (355, 100))
    draw()
    screen.blit(surface, (0, 0))    
    pg.display.flip()              
    clock.tick(60)    
    