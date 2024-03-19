import pygame
import sys
import math
from pytmx import load_pygame
import socket
from game_to_funcs import *

tmx_data, screen, screen_position, speed, clock = initiate()

move_left, move_right, move_up, move_down = init_move()

while True:
    while True:
        move_left, move_right, move_up, move_down = handle_events(move_left, move_right, move_up, move_down)
        move(screen_position, speed, move_left, move_right, move_up, move_down)
        current_chunk = calc_chunk(screen_position, tmx_data)
        draw_chunk(current_chunk, screen_position, screen)
        update_screen(clock)

