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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move player, draw map, and clear screen

    Map1.clear()
    Map1.draw_map(Map1.wrapper_chunk_loading())
    player1.move()
    player1.draw()



    # Update display
    pygame.display.flip()
    setting.clock.tick(60)

pygame.quit()