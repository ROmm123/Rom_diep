import pygame
import sys
from Network_chat import *
import login_screen

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 300
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 24

# Create the display surface
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("signin Screen")

# Fonts
font = pygame.font.Font(None, FONT_SIZE)

# Text input fields
username_input = pygame.Rect(150, 100, 200, 30)
password_input = pygame.Rect(150, 150, 200, 30)
username = ""
password = ""

# Colors for input fields
input_color_active = pygame.Color("lightskyblue3")
input_color_inactive = pygame.Color("gray15")
username_color = input_color_inactive
password_color = input_color_inactive

# Login button
login_button = pygame.Rect(150, 200, 100, 40)
login_button_color = pygame.Color("dodgerblue2")
login_text = font.render("sign-in", True, BLACK)
login_text_rect = login_text.get_rect(center=login_button.center)

switch_button = pygame.Rect(275, 250, 100, 40)
switch_button_color = pygame.Color("darkorange1")
switch_text = font.render("toLogin-in", True, BLACK)
switch_text_rect = switch_text.get_rect(center=switch_button.center)


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def draw_signin_screen():
    screen.fill(WHITE)

    # Add title
    title_text = font.render("sign-in", True, BLACK)
    title_text_rect = title_text.get_rect(center=(WIDTH // 2, 50))
    screen.blit(title_text, title_text_rect)

    pygame.draw.rect(screen, username_color, username_input)
    pygame.draw.rect(screen, password_color, password_input)
    pygame.draw.rect(screen, login_button_color, login_button)
    pygame.draw.rect(screen, switch_button_color, switch_button)  # Draw the switch button
    draw_text("Username:", font, BLACK, screen, 50, 100)
    draw_text("Password:", font, BLACK, screen, 50, 150)
    draw_text(username, font, BLACK, screen, username_input.x + 5, username_input.y + 5)
    draw_text("*" * len(password), font, BLACK, screen, password_input.x + 5, password_input.y + 5)
    screen.blit(login_text, login_text_rect)
    screen.blit(switch_text, switch_text_rect)  # Display text on the switch button


def perform_signin():
    global username, password
    print("Username:", username)
    print("Password:", password)




def switch_to_login_screen( socket_database ):
    socket_database.close()
    login_screen.main()  # Call the main function from login_screen


def main():
    socket_database = Client_chat('localhost', 64444)  # global socket
    socket_database.connect()
    global username, password, username_color, password_color

    clock = pygame.time.Clock()
    running = True
    input_active = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if username_input.collidepoint(event.pos):
                    input_active = True
                    username_color = input_color_active
                    password_color = input_color_inactive
                elif password_input.collidepoint(event.pos):
                    input_active = True
                    password_color = input_color_active
                    username_color = input_color_inactive
                elif login_button.collidepoint(event.pos):
                    perform_signin()
                    print(username+","+password)
                    database_data = {
                        "username": username,
                        "password": password,
                        "query": "signin"
                    }

                    socket_database.send_database_data(database_data)

                elif switch_button.collidepoint(event.pos):  # Check if the switch button is clicked
                    switch_to_login_screen(socket_database)  # Call the function to switch screens

                else:
                    input_active = False
                    username_color = input_color_inactive
                    password_color = input_color_inactive

            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                        username_color = input_color_inactive
                        password_color = input_color_inactive
                        perform_signin()
                        print(username + "," + password)

                        database_data = {
                            "username": username,
                            "password": password,
                            "query": "signin"
                        }

                        socket_database.send_database_data(database_data)

                    elif event.key == pygame.K_BACKSPACE:
                        if username_input.collidepoint(pygame.mouse.get_pos()):
                            username = username[:-1]
                        elif password_input.collidepoint(pygame.mouse.get_pos()):
                            password = password[:-1]
                    else:
                        if username_input.collidepoint(pygame.mouse.get_pos()):
                            username += event.unicode
                        elif password_input.collidepoint(pygame.mouse.get_pos()):
                            password += event.unicode

        draw_signin_screen()
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
