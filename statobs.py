import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Viewing Static Objects on Map")

# Create a clock to control the frame rate
clock = pygame.time.Clock()

# Define colors
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Create a surface for the map
map_width = 1000  # Example map width
map_height = 1000  # Example map height
map_surface = pygame.Surface((map_width, map_height))
map_surface.fill((255, 255, 255))  # Fill the map surface with white (background color)

# Create a list to store static objects (Rect objects)
static_objects = []

# Create multiple static objects and add them to the list
for _ in range(50):  # Create 50 static objects for example
    x = random.randint(0, map_width - 20)  # Random x-coordinate within map boundaries
    y = random.randint(0, map_height - 20)  # Random y-coordinate within map boundaries
    width = 20  # Width of the rectangle
    height = 20  # Height of the rectangle
    color = random.choice([red, green, blue])  # Random color
    static_obj = pygame.Rect(x, y, width, height)
    static_objects.append((static_obj, color))

# Define the viewport (camera) position
viewport_x = 0
viewport_y = 0
viewport_width = screen_width
viewport_height = screen_height

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle user input to move the viewport (camera)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        viewport_x -= 5
    if keys[pygame.K_RIGHT]:
        viewport_x += 5
    if keys[pygame.K_UP]:
        viewport_y -= 5
    if keys[pygame.K_DOWN]:
        viewport_y += 5

    # Ensure the viewport stays within bounds
    viewport_x = max(0, min(viewport_x, map_width - viewport_width))
    viewport_y = max(0, min(viewport_y, map_height - viewport_height))

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw all static objects on the map surface relative to the viewport position
    for static_obj, color in static_objects:
        obj_x = static_obj.x - viewport_x
        obj_y = static_obj.y - viewport_y
        if 0 <= obj_x <= viewport_width and 0 <= obj_y <= viewport_height:
            pygame.draw.rect(screen, color, (obj_x, obj_y, static_obj.width, static_obj.height))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
