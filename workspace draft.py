import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the width and height of the screen
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Black Screen with White Rectangle")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black color
    screen.fill(BLACK)

    # Draw a white rectangle
    pygame.draw.rect(screen, WHITE, (412, 600, 200, 40))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
