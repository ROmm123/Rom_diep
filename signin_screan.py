import keybinds
import trash_script
from database_manager import socket_data
import login_screen
import opening_screen
from opening_screen import *

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 30  # Adjusted font size for better visibility on the smaller screen

# Create the display surface
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Signin Screen")

# Fonts
font = pygame.font.Font(None, FONT_SIZE)

# Text input fields
username_input = pygame.Rect(300, 200, 200, 40)
password_input = pygame.Rect(300, 280, 200, 40)
username = ""
password = ""

# Colors for input fields
input_color_active = pygame.Color("lightskyblue3")
input_color_inactive = pygame.Color("gray15")
username_color = input_color_inactive
password_color = input_color_inactive

# Login button
login_button = pygame.Rect(300, 360, 100, 50)
login_button_color = pygame.Color("dodgerblue2")
login_text = font.render("Sign-in", True, BLACK)
login_text_rect = login_text.get_rect(center=login_button.center)

# Switch button
switch_button = pygame.Rect(425, 450, 100, 50)
switch_button_color = pygame.Color("darkorange1")
switch_text = font.render("To Login", True, BLACK)
switch_text_rect = switch_text.get_rect(center=switch_button.center)


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def draw_signin_screen():
    screen.fill(WHITE)

    # Add title
    title_text = font.render("Sign-in", True, BLACK)
    title_text_rect = title_text.get_rect(center=(WIDTH // 2, 100))
    screen.blit(title_text, title_text_rect)

    pygame.draw.rect(screen, username_color, username_input)
    pygame.draw.rect(screen, password_color, password_input)
    pygame.draw.rect(screen, login_button_color, login_button)
    pygame.draw.rect(screen, switch_button_color, switch_button)

    draw_text("Username:", font, BLACK, screen, 150, 210)
    draw_text("Password:", font, BLACK, screen, 150, 290)
    draw_text(username, font, BLACK, screen, username_input.x + 5, username_input.y + 5)
    draw_text("*" * len(password), font, BLACK, screen, password_input.x + 5, password_input.y + 5)
    screen.blit(login_text, login_text_rect)
    screen.blit(switch_text, switch_text_rect)


def perform_signin():
    global username, password
    print("Username:", username, flush=True)
    print("Password:", password, flush=True)


def switch_to_login_screen(socket_database):
    socket_database.close()
    username, password, x, y, speed_c, size_c, shield_c, hp_c_60, hp_c_30, hp_c_15, hp_c_5 = login_screen.main()
    trash_script.main(username, password, x, y, speed_c, size_c, shield_c, hp_c_60, hp_c_30, hp_c_15, hp_c_5)


def main():
    socket_database = socket_data()
    socket_database = socket_database.data_base_socket
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
                    database_data = {
                        "username": username,
                        "password": password,
                        "query": "signin"
                    }
                    socket_database.send_database_data(database_data)
                    switch_to_login_screen(socket_database)
                elif switch_button.collidepoint(event.pos):
                    switch_to_login_screen(socket_database)
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
                        database_data = {
                            "username": username,
                            "password": password,
                            "query": "signin"
                        }
                        socket_database.send_database_data(database_data)
                        switch_to_login_screen(socket_database)
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
    result = opening_screen.show_opening_screen()
    if result:
        keybinds.run()
    main()
