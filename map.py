import pygame
from pytmx import load_pygame
from  settings import *

class Map():
    def __init__(self , Player , screen_width , screen_height , setting):
        self.map = load_pygame("cubed_map.tmx")
        self.chunk = pygame.sprite.Group
        self.chunk_size = 20
        self.player = Player
        self.screen = pygame.display.set_mode((screen_width,screen_height))
        self.setting = setting

    def get_screen(self):
        return self.screen



    def load_chunk(self , x , y ):
        self.chunk = pygame.sprite.Group()

        # Load tiles in the specified chunk
        chunk_size = self.chunk_size
        for x in range(x, x + chunk_size):
            for y in range(y, y + chunk_size):
                tile_image = self.map.get_tile_image(x, y, 0)  # Assuming layer index is 0
                if tile_image is not None:
                    pos = (x * self.map.tilewidth, y * self.map.tileheight)
                    tile_rect = tile_image.get_rect(topleft=pos)
                    sprite = pygame.sprite.Sprite()
                    sprite.image = tile_image
                    sprite.rect = tile_rect
                    self.chunk.add(sprite)

        return self.chunk

    def wrapper_chunk_loading(self):
        player_x = self.player.x
        player_y = self.player.y

        # Draw the current chunk at the correct screen position
        COUNT_X = int(player_x // 64)
        COUNT_Y = int(player_y // 64)

        current_chunk = self.load_chunk(COUNT_X,COUNT_Y)
        return current_chunk

    def draw_map(self , current_chunk):
        for sprite in current_chunk:
            sprite.rect.x = sprite.rect.x - self.player.x
            sprite.rect.y = sprite.rect.y - self.player.y
            self.screen.blit(sprite.image, sprite.rect)

    def clear(self):
        self.screen.fill(self.setting.white)