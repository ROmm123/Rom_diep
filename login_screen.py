import sys
import trash_script
from trash_script import *
import signin_screan
from database_manager import socket_data

'''class get_variables():
    def __init__(self ,x ,y, usr , passw , spc , szc , shc , hp_60 , hp_30 , hp_15 , hp_5):
        self.x = x
        self.y = y
        self.username = usr
        self.password = passw
        self.speed_c = spc
        self.size_c = szc
        self.shield_c = shc
        self.hp_c_60 = hp_60
        self.hp_c_30 = hp_30
        self.hp_c_15 = hp_15
        self.hp_c_5 = hp_5'''
# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 300
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 24

# Create the display surface
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Login Screen")

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
login_text = font.render("Login", True, BLACK)
login_text_rect = login_text.get_rect(center=login_button.center)

# Switch button
switch_button = pygame.Rect(275, 250, 100, 40)
switch_button_color = pygame.Color("darkorange1")
switch_text = font.render("toSign-in", True, BLACK)
switch_text_rect = switch_text.get_rect(center=switch_button.center)


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def draw_login_screen():
    screen.fill(WHITE)

    # Add title
    title_text = font.render("Log-in", True, BLACK)
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


def perform_login():
    global username, password
    print("Username:", username)
    print("Password:", password)


def switch_to_signin_screen(socket_dataa):
    socket_dataa.close()
    signin_screan.main()  # Call the main function in the second script


def main():
    socket_class = socket_data()
    socket_class.data_base_socket.connect()
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
                    perform_login()
                    database_data = {
                        "username": username,
                        "password": password,
                        "quary": "login"
                    }

                    socket_class.data_base_socket.send_database_data(database_data)
                    tuple_data = socket_class.data_base_socket.receive_database_data()
                    print("received from main : " + str(tuple_data))
                    if tuple_data:
                        print("got after 'if tuple_data' PRINT 1")
                        username = tuple_data[0]
                        password = tuple_data[1]
                        x = tuple_data[2]
                        y = tuple_data[3]
                        speed_c = tuple_data[4]
                        size_c = tuple_data[5]
                        shield_c = tuple_data[6]
                        hp_c_60 = tuple_data[7]
                        hp_c_30 = tuple_data[8]
                        hp_c_15 = tuple_data[9]
                        hp_c_5 = tuple_data[10]
                        if x == None or y == None:
                            x = 0
                            y = 0
                            speed_c = 0
                            size_c = 0
                            shield_c = 0
                            hp_c_60 = 0
                            hp_c_30 = 0
                            hp_c_15 = 0
                            hp_c_5 = 0
                        print(username, password, x, y, speed_c, size_c, shield_c, hp_c_60, hp_c_30, hp_c_15, hp_c_5)
                        return username, password, x, y, speed_c, size_c, shield_c, hp_c_60, hp_c_30, hp_c_15, hp_c_5
                elif switch_button.collidepoint(event.pos):  # Check if the switch button is clicked
                    switch_to_signin_screen(socket_class.data_base_socket)  # Call the function to switch screens

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
                        perform_login()
                        database_data = {
                            "username": username,
                            "password": password,
                            "quary": "login"
                        }

                        socket_class.data_base_socket.send_database_data(database_data)
                        tuple_data = socket_class.data_base_socket.receive_database_data()
                        print("received from main : " + str(tuple_data))
                        if tuple_data:
                            print("got after 'if tuple_data' PRINT 2")
                            username = tuple_data[0]
                            password = tuple_data[1]
                            x = tuple_data[2]
                            y = tuple_data[3]
                            speed_c = tuple_data[4]
                            size_c = tuple_data[5]
                            shield_c = tuple_data[6]
                            hp_c_60 = tuple_data[7]
                            hp_c_30 = tuple_data[8]
                            hp_c_15 = tuple_data[9]
                            hp_c_5 = tuple_data[10]
                            if x == None or y == None:
                                x = 0
                                y = 0
                                speed_c = 0
                                size_c = 0
                                shield_c = 0
                                hp_c_60 = 0
                                hp_c_30 = 0
                                hp_c_15 = 0
                                hp_c_5 = 0
                            print(username , password , x, y, speed_c, size_c, shield_c, hp_c_60, hp_c_30, hp_c_15, hp_c_5)
                            return username , password , x, y, speed_c, size_c, shield_c, hp_c_60, hp_c_30, hp_c_15, hp_c_5
                            print("AFTER RETURN ")

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

        draw_login_screen()
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    print("finished function")
    username , password , x, y, speed_c, size_c, shield_c, hp_c_60, hp_c_30, hp_c_15, hp_c_5 = main()
    print("username variable in login : "+str(username))
    trash_script.main(username , password ,x, y, speed_c, size_c, shield_c, hp_c_60, hp_c_30, hp_c_15, hp_c_5)