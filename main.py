import pygame
from player import Player
from map import Map
from settings import settings

pygame.init()



setting = settings()
player1 = Player(0, 0, 35, (255, 0, 0), setting)
Map1 = Map(player1, setting)



running = True
while running:

    # Move player, draw map, and clear screen
    player1.move()
    chunk = Map1.wrapper_chunk_loading()
    Map1.draw_map(chunk)
    #player1.draw()



    # Update display
    pygame.display.flip()
    setting.clock.tick(60)

pygame.quit()