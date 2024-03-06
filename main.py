import pygame
from player import Player
from map import Map
from settings import settings

pygame.init()

setting = settings()
Playerr = Player(0,0,35, setting.red , setting)
MAP = Map(Playerr , setting)

while True:
    Playerr.handle_events()
    Playerr.move()
    chunk = MAP.calc_chunk()
    MAP.draw_map(chunk)
    setting.update()

pygame.quit()