from moviepy.editor import VideoFileClip
import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the width and height of the screen
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Video Player")

# Load the intro video
intro_clip = VideoFileClip("Screens/intro.mp4")

# Play the intro video
intro_clip.preview()

# Load and display the post-intro image
post_intro_image = pygame.image.load("Screens/post_intro.jpg")
screen.blit(post_intro_image, (0, 0))
pygame.display.flip()

# Wait for user input to close the window
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()
sys.exit()
