import pygame
from settings import*

class inventory():
    def __init__(self, settings):
        self.settings = settings

    def draw_inventory(self):
        white_background=pygame.image.load("white.png")
        background_rect=white_background.get_rect(topleft=(0,0))
        self.settings.surface.blit(white_background,background_rect)

        text_front=pygame.font.Font('Power Smash.ttf',15)
        t="True"
        f="False"
        a=[ None,None,None,None,None]
        a[0]='skill1:'+" "+f
        a[2]='skill2:'+" "+f
        x=5
        y=5
        for i in range(len(a)):
            y+=20
            text_surface=text_front.render(a[i],False,'Black')
            self.settings.surface.blit(text_surface,(x,y))


