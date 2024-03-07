import pygame
import sys
import math
from pytmx import load_pygame

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (47, 47, 47)

# Define global variables
running = True
move_left = False
move_right = False
move_up = False
move_down = False
screen_position = [0, 0]

screen_width = 800
screen_height = 600

# Initial screen position and speed
speed = 5
circle_radius = 35  # Adjusted radius of the circular path
circle_center = [screen_width // 2, screen_height // 2]  # Center of the circular path
offset_distance = 50  # Distance from the middle of the circles to the middle of the rectangle
player_circle_color = RED
rect_width, rect_height = 30, 30
green_circles = []




def load_chunk(tmx_data, chunk_x, chunk_y):
    chunk_group = pygame.sprite.Group()
    chunk_size = 40
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


def shoot_green_circle(player_position, green_circles, mouse_x, mouse_y, circle_center):
    # Calculate the direction towards the mouse position
    player_x = player_position[0]
    player_y = player_position[1]

    direction_x = mouse_x - player_x
    direction_y = mouse_y - player_y

    # Calculate the magnitude of the direction vector
    magnitude = math.sqrt(direction_x ** 2 + direction_y ** 2)

    # Normalize the direction vector
    if magnitude != 0:
        direction_x /= magnitude
        direction_y /= magnitude


    #Green circles' velocity
    velocity = [2 * direction_x,2 * direction_y]

    #Calculate the starting position
    angle_with_x_axis = math.atan2(direction_y, direction_x)
    angle_degrees = math.degrees(angle_with_x_axis)
    print("Angle with x-axis (degrees):", angle_degrees)

    start_x = circle_center[0] + offset_distance * math.cos(angle_with_x_axis)
    start_y = circle_center[1] + offset_distance * math.sin(angle_with_x_axis)

    print(start_x, start_y)

    # Add the green circle to the list with its initial position and velocity
    green_circles.append({"position": [start_x, start_y], "velocity": velocity})




def update_green_circles(screen, green_circles):
    # List to store indices of circles to remove
    remove_indices = []


    for i, circle in enumerate(green_circles):
        # Update the position of the green circle based on its velocity
        circle["position"][0] += circle["velocity"][0]
        circle["position"][1] += circle["velocity"][1]

        # Draw the green circle
        pygame.draw.circle(screen, GREEN, (
            int(circle["position"][0]), int(circle["position"][1])), 5)

        # If the green circle moves off-screen, mark it for removal
        if circle["position"][0] < 0 or circle["position"][0] > screen.get_width() or \
                circle["position"][1] < 0 or circle["position"][1] > screen.get_height():
            remove_indices.append(i)

    # Remove circles that have moved off-screen
    for index in remove_indices[::-1]:
        del green_circles[index]


def handle_events(circle_center, player_position, green_circles, circle_radius, screen_position, rect_width, rect_height):
    global running, move_left, move_right, move_up, move_down
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_left = True
            elif event.key == pygame.K_d:
                move_right = True
            elif event.key == pygame.K_w:
                move_up = True
            elif event.key == pygame.K_s:
                move_down = True
            elif event.key == pygame.K_SPACE:  # Check if space bar is pressed
                # Get the current mouse position
                mouse_pos = pygame.mouse.get_pos()

                # Adjust mouse position based on player and screen movement
                mouse_pos = pygame.mouse.get_pos()  # Get the current mouse position
                mouse_x = screen_position[0] + mouse_pos[0] - circle_center[0]  # Break down mouse position into x and y components
                mouse_y = screen_position[1] + mouse_pos[1] - circle_center[1]
                if (mouse_x >= 0 and mouse_y >= 0):
                    print("Mouse position when space bar is pressed - X:", mouse_x, "Y:", mouse_y)
                    print("player - ", player_position)
                    print("screen position - ", screen_position)

                # Shoot the green circle towards the mouse position
                shoot_green_circle(player_position, green_circles, mouse_x, mouse_y, circle_center)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            elif event.key == pygame.K_d:
                move_right = False
            elif event.key == pygame.K_w:
                move_up = False
            elif event.key == pygame.K_s:
                move_down = False


def update_screen_position():
    global screen_position, move_left, move_right, move_up, move_down
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


def render(screen, player_x, player_y, current_chunk, circle_center, circle_radius, player_circle_color, rect_width,
           rect_height, offset_distance, tmx_data, camera_x, camera_y, green_circles):
    screen.fill(WHITE)
    for sprite in current_chunk:
        sprite.rect.x = sprite.rect.x - screen_position[0]
        sprite.rect.y = sprite.rect.y - screen_position[1]
        screen.blit(sprite.image, sprite.rect)

    pygame.draw.circle(screen, player_circle_color, circle_center, circle_radius)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - (circle_center[0])  # Adjusted mouse position
    dy = mouse_y - (circle_center[1])  # Adjusted mouse position
    angle = math.atan2(dy, dx)
    print(str(angle))

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

    # Create rectangle surface
    rect_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
    pygame.draw.rect(rect_surface, GREY, (0, 0, rect_width, rect_height))  # Draw red rectangle on surface
    rotated_rect = pygame.transform.rotate(rect_surface, math.degrees(-angle_to_tangent))

    # Get rectangle's rect
    rect_rect = rotated_rect.get_rect(center=(rect_center_x , rect_center_y))

    # Draw rectangle
    screen.blit(rotated_rect, rect_rect)

    # Draw green circles
    for circle in green_circles:
        pygame.draw.circle(screen, GREEN,
                           (int(circle["position"][0] - camera_x), int(circle["position"][1] - camera_y)), 10)

    pygame.display.update()


def main():
    global running, move_left, move_right, move_up, move_down, screen_position, speed
    # Initialize pygame
    pygame.init()
    # Set up the display window
    screen = pygame.display.set_mode((screen_width, screen_height))
    # Load the TMX map data from the file 'cubed_map.tmx'
    tmx_data = load_pygame("cubed_map.tmx")
    # Set up clock for controlling the frame rate
    clock = pygame.time.Clock()



    running = True
    while running:
        # Handle events and retrieve mouse position
        # Handle events and retrieve mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Calculate the player's position relative to the game world
        player_position = [circle_center[0] + screen_position[0] - 400, circle_center[1] + screen_position[1] - 300]

        handle_events(circle_center, player_position,
                      green_circles, circle_radius, screen_position, rect_width, rect_height)

        player_x = screen_position[0]
        player_y = screen_position[1]
        update_screen_position()
        update_green_circles(screen, green_circles)
        player_x = screen_position[0]
        player_y = screen_position[1]
        COUNT_X = int(player_x // 64)
        COUNT_Y = int(player_y // 64)
        current_chunk = load_chunk(tmx_data, COUNT_X, COUNT_Y)
        render(screen, player_x, player_y, current_chunk, circle_center, circle_radius, player_circle_color, rect_width,
               rect_height, offset_distance, tmx_data, 0, 0, green_circles)
        clock.tick(90)


if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
