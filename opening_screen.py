import pygame
import sys

def show_opening_screen():
    # Initialize Pygame
    pygame.init()

    # Constants
    WIDTH, HEIGHT = 800, 600
    IMAGE_PATH = "pictures/Opening_Screen.png"
    RECT1_POS = (310, 190)
    RECT1_SIZE = (197, 67.7)
    RECT2_POS = (310, 272)
    RECT2_SIZE = (197, 27.7)

    # Load the image
    image = pygame.image.load(IMAGE_PATH)

    # Create the display surface
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Opening Screen")

    # Define the rectangles
    rect1 = pygame.Rect(RECT1_POS, RECT1_SIZE)
    rect2 = pygame.Rect(RECT2_POS, RECT2_SIZE)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect1.collidepoint(event.pos):
                    return False
                if rect2.collidepoint(event.pos):
                    return True

        screen.blit(image, (0, 0))
        pygame.display.flip()
        clock.tick(30)

