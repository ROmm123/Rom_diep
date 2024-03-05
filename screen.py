import pygame
import sys
import math
from pytmx import load_pygame
import socket
from game import screen
########################layer0##################################################
def load_chunk(chunk_x, chunk_y,tmx_data):
    chunk_group = pygame.sprite.Group()

    # Load tiles in the specified chunk
    chunk_size = 20
    for x in range(chunk_x, chunk_x + chunk_size):
        for y in range(chunk_y, chunk_y + chunk_size):
            tile_image = tmx_data.get_tile_image(x, y, 0)  # Assuming layer index is 0
            if tile_image is not None:
                pos = (x * tmx_data.tilewidth, y * tmx_data.tileheight)
                tile_rect = tile_image.get_rect(topleft=pos)
                sprite = pygame.sprite.Sprite()
                sprite.image = tile_image
                sprite.rect = tile_rect
                chunk_group.add(sprite)

    return chunk_group

def setting():
    pygame.init()

    # Set up the display window
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    tmx_data = load_pygame("files and pic/cubed_map.tmx")

def end_tile(screen_position,circle_center,screen_width,screen_height):
    # Calculate the screen's position on the map
    player_x = screen_position[0]
    player_y = screen_position[1]

    camera_x = circle_center[0] - screen_width // 2
    camera_y = circle_center[1] - screen_height // 2

    # Draw the current chunk at the correct screen position
    COUNT_X = int(player_x // 64)
    COUNT_Y = int(player_y // 64)

    current_chunk = load_chunk(COUNT_X, COUNT_Y)
    return current_chunk

def draw_layer0(current_chunk,screen_position):
    WHITE = (255, 255, 255)
    screen.fill(WHITE)  # Fill screen with white


    # Draw the tiles in the current chunk
    for sprite in current_chunk:
        sprite.rect.x = sprite.rect.x - screen_position[0]
        sprite.rect.y = sprite.rect.y - screen_position[1]
        screen.blit(sprite.image, sprite.rect)
###############################end of layer0#########################################################
#####################################################################################################
#####################################################################################################
#####################################################################################################



###############################layer1##################################################


def draw_circle_layer1(screen,player_circle_color,circle_center,circle_radius):
    pygame.draw.circle(screen, player_circle_color, circle_center, circle_radius)