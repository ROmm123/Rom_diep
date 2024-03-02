import pygame
import sys
import math
from pytmx import load_pygame
import socket

# Initialize pygame
pygame.init()

# Set up the display window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
z = pygame.math.Vector2(400, 300)



# Load the TMX map data from the file 'cubed_map.tmx'
tmx_data = load_pygame("cubed_map.tmx")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 10009))


# Define a function to load a chunk of tiles
def load_chunk(chunk_x, chunk_y):
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


# Set up clock for controlling the frame rate
clock = pygame.time.Clock()

# Initial screen position and speed
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)  # New color for the rectangle

# Define rectangle properties
rect_width, rect_height = 30, 30  # Adjusted size
circle_radius = 35  # Adjusted radius of the circular path
circle_center = [screen_width // 2, screen_height // 2]  # Center of the circular path
offset_distance = 15  # Distance to offset the rectangle from the circle's radius
player_circle_color = (RED)

# Initialize variables to track movement direction
screen_position = [0, 0]
speed = 5

# Initialize variables to track movement direction
move_left = False
move_right = False
move_up = False
move_down = False

# Main game loop
running = True
while running:
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

        z.x -= speed
    if move_right:
        screen_position[0] += speed
        z.x += speed

    if move_up:
        screen_position[1] -= speed
        if screen_position[1] < 0:
            screen_position[1] += speed
        z.y -= speed

    if move_down:
        screen_position[1] += speed
        z.y += speed

    # Clear the screen
    screen.fill(WHITE)  # Fill screen with white

    # Calculate the screen's position on the map
    player_x = screen_position[0]
    player_y = screen_position[1]

    camera_x = circle_center[0] - screen_width // 2
    camera_y = circle_center[1] - screen_height // 2

    # Draw the current chunk at the correct screen position
    COUNT_X = int(player_x // 64)
    COUNT_Y = int(player_y // 64)

    current_chunk = load_chunk(COUNT_X, COUNT_Y)

    # Draw the tiles in the current chunk
    for sprite in current_chunk:
        sprite.rect.x = sprite.rect.x - screen_position[0]
        sprite.rect.y = sprite.rect.y - screen_position[1]
        screen.blit(sprite.image, sprite.rect)

    # Draw red circle representing the player
    pygame.draw.circle(screen, player_circle_color, circle_center, circle_radius)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - (circle_center[0] - camera_x)  # Adjusted mouse position
    dy = mouse_y - (circle_center[1] - camera_y)  # Adjusted mouse position
    angle = math.atan2(dy, dx)

    # Calculate the point on the circle tangent to the mouse position
    tangent_x = circle_center[0] + circle_radius * math.cos(angle)
    tangent_y = circle_center[1] + circle_radius * math.sin(angle)

    # Calculate the angle between the horizontal axis and the line connecting the circle's center to the point of tangency
    angle_to_tangent = math.atan2(tangent_y - circle_center[1], tangent_x - circle_center[0])

    # Calculate rectangle position on circular path
    rect_center_x = tangent_x + offset_distance * math.cos(angle_to_tangent)
    rect_center_y = tangent_y + offset_distance * math.sin(angle_to_tangent)

    # Adjust the rectangle position to fit the circle
    rect_center_x += (circle_radius - 15 - offset_distance) * math.cos(angle)
    rect_center_y += (circle_radius - 15 - offset_distance) * math.sin(angle)

    # Create rectangle weapon_surf
    rect_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
    pygame.draw.rect(rect_surface, RED, (0, 0, rect_width, rect_height))  # Draw green rectangle on weapon_surf
    rotated_rect = pygame.transform.rotate(rect_surface, math.degrees(-angle_to_tangent))
    print(rotated_rect)
    # Get rectangle's rect
    rect_rect = rotated_rect.get_rect(center=(rect_center_x - camera_x, rect_center_y - camera_y))

    # Draw rectangle
    screen.blit(rotated_rect, rect_rect)

    # Sending positional data of circle and rectangle
    #circle_data = f"CIRCLE,{circle_center[0]},{circle_center[1]},{circle_radius}"
    rectangle_data = f"RECTANGLE,{rect_center_x},{rect_center_y},{rect_width},{rect_height},{angle_to_tangent}"
    #z_data = f"z_position,{z.x},{z.y}"

    # Concatenate both pieces of data
    data_to_send = rectangle_data

    # Encode and send the data

    '''rectangle_info = client_socket.recv(2048).decode("utf-8")
    # Process rectangle info
    # Process received data
    circle_info, rectangle_info = rectangle_info.split("|")

    # Process circle info
    circle_data = circle_info.split()
    circle_center_x = int(circle_data[1])
    circle_center_y = int(circle_data[2])
    circle_radius = int(circle_data[3])

    # Process rectangle info
    rectangle_data = rectangle_info.split()
    rect_center_x = int(rectangle_data[1])
    rect_center_y = int(rectangle_data[2])
    rect_width = int(rectangle_data[3])
    rect_height = int(rectangle_data[4])
    rotation_angle = int(rectangle_data[5])

    # Create rectangle weapon_surf
    rect_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
    pygame.draw.rect(rect_surface, RED, (0, 0, rect_width, rect_height))

    # Rotate the rectangle weapon_surf
    rotated_rect_surface = pygame.transform.rotate(rect_surface, rotation_angle)

    # Get rectangle's rect
    rotated_rect = rotated_rect_surface.get_rect(center=(rect_center_x, rect_center_y))

    # Draw rotated rectangle onto the screen
    screen.blit(rozztated_rect_surface, rotated_rect)'''
    try:
        data_to_send = data_to_send.encode()
        client_socket.send(data_to_send)
        client2_pos = client_socket.recv(2048).decode("utf-8")
        if client2_pos != '0':
            numbers = client2_pos.split(",")
            print(numbers)
            k1 = int(float(numbers[1]))  # Convert float to int
            k2 = int(float(numbers[2]))  # Convert float to int
            b1 = k1 - int(z.x)
            b2 = k2 - int(z.y)
            a1 = abs(k1 - int(z.x))
            a2 = abs(k2 - int(z.y))
            if a2 < screen_height and a1 < screen_width:
                weapon_surf = pygame.Surface((int(numbers[3]), int(numbers[4])), pygame.SRCALPHA)
                pygame.draw.rect(weapon_surf , RED ,(0 , 0 , int(numbers[3]) , int(numbers[4])))
                rotated_weapon = pygame.transform.rotate(weapon_surf, math.degrees(-angle_to_tangent))
                rect2 = weapon_surf.get_rect(topleft=(350 + b1, 250 + b2))
                screen.blit(weapon_surf, rect2)


    except KeyboardInterrupt:
        print("Client interrupted by user.")
        client_socket.close()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()