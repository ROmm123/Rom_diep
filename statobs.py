import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Drawing Static Objects")

# Create a clock to control the frame rate
clock = pygame.time.Clock()

# Define colors
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Create a list to store static objects (Rect objects)
static_objects = []

# Create multiple static objects and add them to the list
for _ in range(10):  # Create 10 static objects for example
    x = random.randint(0, screen_width - 20)  # Random x-coordinate
    y = random.randint(0, screen_height - 20)  # Random y-coordinate
    width = 20  # Width of the rectangle
    height = 20  # Height of the rectangle
    color = random.choice([red, green, blue])  # Random color
    static_obj = pygame.Rect(x, y, width, height)
    static_objects.append((static_obj, color))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw all static objects
    for static_obj, color in static_objects:
        pygame.draw.rect(screen, color, static_obj)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
