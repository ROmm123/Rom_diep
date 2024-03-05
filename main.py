from player import *
from settings import *

pygame.init()


setting = settings()
player1 = Player(0,0 , 35 , (255,0,0) , setting)
Map1 = Map(player1 , setting.screen_width , setting.screen_height , setting)

while True:
    player1.move()
    Map1.draw_map(Map1.wrapper_chunk_loading())
    player1.draw()
    Map1.clear()
