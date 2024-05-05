import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Drawing Text")

# Define text font and size
font = pygame.font.Font(None, 36)

# Define text content
text_content = "Hello, Pygame!"

# Render the text onto a surface
text_surface = font.render(text_content, True, (40, 158, 255))

# Get the rectangle that encloses the text
text_rect = text_surface.get_rect()

# Center the text on the screen
text_rect.center = (screen_width // 2, screen_height // 2)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # Blit the text surface onto the screen
    screen.blit(text_surface, text_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()