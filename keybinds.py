import pygame

def run():
    # Initialize Pygame
    pygame.init()

    # Set up the display
    window_size = (800, 600)  # Adjust the window size as needed
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Image Display")

    # Load the image
    image = pygame.image.load("pictures/Keybinds.png")

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    running = False

        # Draw the image
        window.fill((0, 0, 0))  # Clear the screen with a black color
        window.blit(image, (0, 0))  # Draw the image in the top-left corner
        pygame.display.flip()  # Update the display

