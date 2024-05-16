import pygame
from pytmx import load_pygame
from settings import *


class Map():
    def __init__(self, Player1, settings):
        self.map = load_pygame("map.tmx")
        self.chunk_size = 20
        self.player = Player1
        self.screen = settings.surface
        self.setting = settings

    def load_chunk(self, chunk_x, chunk_y, layer):
        chunk_group = pygame.sprite.Group()
        chunk_size = 20
        for x in range(chunk_x, chunk_x + chunk_size):
            for y in range(chunk_y, chunk_y + chunk_size):
                tile_image = self.map.get_tile_image(x, y, layer)  # Assuming layer index is 0
                if tile_image is not None:
                    pos = (x * self.map.tilewidth, y * self.map.tileheight)
                    tile_rect = tile_image.get_rect(topleft=pos)
                    sprite = pygame.sprite.Sprite()
                    sprite.image = tile_image
                    sprite.rect = tile_rect
                    chunk_group.add(sprite)
        return chunk_group

    def calc_chunk(self, layer):
        player_x = self.player.screen_position[0]
        player_y = self.player.screen_position[1]

        # Draw the current chunk at the correct screen position
        COUNT_X = int(player_x // 64)
        COUNT_Y = int(player_y // 64)

        current_chunk = self.load_chunk(COUNT_X, COUNT_Y, layer)
        return current_chunk

    def draw_map(self, current_chunk):
        for sprite in current_chunk:
            sprite.rect.x = sprite.rect.x - self.player.screen_position[0]
            sprite.rect.y = sprite.rect.y - self.player.screen_position[1]
            self.screen.blit(sprite.image, sprite.rect)
