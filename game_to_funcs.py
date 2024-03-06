import pygame
import sys
import math
from pytmx import load_pygame
import socket

def initiate():
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    tmx_data = load_pygame("cubed_map.tmx")
    screen_position = [0,0]
    speed = 5
    clock = pygame.time.Clock()
    return tmx_data , screen , screen_position ,speed, clock

def load_chunk(chunk_x, chunk_y , tmx_data):
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

def init_move():
    move_left = False
    move_right = False
    move_up = False
    move_down = False
    return  move_left , move_right , move_up , move_down

def handle_events(move_left, move_right, move_up, move_down):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            elif event.key == pygame.K_RIGHT:
                move_right = True
            elif event.key == pygame.K_UP:
                move_up = True
            elif event.key == pygame.K_DOWN:
                move_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            elif event.key == pygame.K_RIGHT:
                move_right = False
            elif event.key == pygame.K_UP:
                move_up = False
            elif event.key == pygame.K_DOWN:
                move_down = False
    return move_left, move_right, move_up, move_down


def move(screen_position , speed ,move_left , move_right , move_up , move_down ):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            elif event.key == pygame.K_RIGHT:
                move_right = True
            elif event.key == pygame.K_UP:
                move_up = True
            elif event.key == pygame.K_DOWN:
                move_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            elif event.key == pygame.K_RIGHT:
                move_right = False
            elif event.key == pygame.K_UP:
                move_up = False
            elif event.key == pygame.K_DOWN:
                move_down = False

    # Update screen position based on movement direction
    if move_left:
        screen_position[0] -= speed
        if screen_position[0] < 0:
            screen_position[0] += speed


    if move_right:
        screen_position[0] += speed


    if move_up:
        screen_position[1] -= speed
        if screen_position[1] < 0:
            screen_position[1] += speed


    if move_down:
        screen_position[1] += speed

def calc_chunk(screen_position ,tmx_data):
    player_x = screen_position[0]
    player_y = screen_position[1]

    # Draw the current chunk at the correct screen position
    COUNT_X = int(player_x // 64)
    COUNT_Y = int(player_y // 64)

    current_chunk = load_chunk(COUNT_X, COUNT_Y , tmx_data)
    return current_chunk



def draw_chunk(current_chunk , screen_position , screen):
    for sprite in current_chunk:
        sprite.rect.x = sprite.rect.x - screen_position[0]
        sprite.rect.y = sprite.rect.y - screen_position[1]
        screen.blit(sprite.image, sprite.rect)

def update_screen(clock):
    pygame.display.update()
    clock.tick(60)