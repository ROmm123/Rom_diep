import pygame
import sys
import connection_with_database
from connection_with_database import *
from login_screen import Login


class Sign_in:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Constants
        self.WIDTH, self.HEIGHT = 400, 300
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.FONT_SIZE = 24

        # Create the display surface
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("signin Screen")

        # Fonts
        self.font = pygame.font.Font(None, self.FONT_SIZE)

        # Text input fields
        self.username_input = pygame.Rect(150, 100, 200, 30)
        self.password_input = pygame.Rect(150, 150, 200, 30)
        self.username = ""
        self.password = ""

        # Colors for input fields
        self.input_color_active = pygame.Color("lightskyblue3")
        self.input_color_inactive = pygame.Color("gray15")
        self.username_color = self.input_color_inactive
        self.password_color = self.input_color_inactive

        # Login button
        self.login_button = pygame.Rect(150, 200, 100, 40)
        self.login_button_color = pygame.Color("dodgerblue2")
        self.login_text = self.font.render("sign-in", True, self.BLACK)
        self.login_text_rect = self.login_text.get_rect(center=self.login_button.center)

    def draw_text(self, text, font, color, surface, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_obj, text_rect)

    def draw_signin_screen(self):
        self.screen.fill(self.WHITE)

        # Add title
        title_text = self.font.render("sign-in", True, self.BLACK)
        title_text_rect = title_text.get_rect(center=(self.WIDTH // 2, 50))
        self.screen.blit(title_text, title_text_rect)

        pygame.draw.rect(self.screen, self.username_color, self.username_input)
        pygame.draw.rect(self.screen, self.password_color, self.password_input)
        pygame.draw.rect(self.screen, self.login_button_color, self.login_button)
        self.draw_text("Username:", self.font, self.BLACK, self.screen, 50, 100)
        self.draw_text("Password:", self.font, self.BLACK, self.screen, 50, 150)
        self.draw_text(self.username, self.font, self.BLACK, self.screen, self.username_input.x + 5,
                       self.username_input.y + 5)
        self.draw_text("*" * len(self.password), self.font, self.BLACK, self.screen, self.password_input.x + 5,
                       self.password_input.y + 5)
        self.screen.blit(self.login_text, self.login_text_rect)

    def perform_signin(self):
        print("Username:", self.username)
        print("Password:", self.password)

    def main(self):
        clock = pygame.time.Clock()
        running = True
        input_active = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.username_input.collidepoint(event.pos):
                        input_active = True
                        self.username_color = self.input_color_active
                        self.password_color = self.input_color_inactive
                    elif self.password_input.collidepoint(event.pos):
                        input_active = True
                        self.password_color = self.input_color_active
                        self.username_color = self.input_color_inactive
                    elif self.login_button.collidepoint(event.pos):
                        self.perform_signin()
                        handle_data_for_signin(self.username, self.password)

                    else:
                        input_active = False
                        self.username_color = self.input_color_inactive
                        self.password_color = self.input_color_inactive

                if event.type == pygame.KEYDOWN:
                    if input_active:
                        if event.key == pygame.K_RETURN:
                            input_active = False
                            self.username_color = self.input_color_inactive
                            self.password_color = self.input_color_inactive
                            self.perform_signin()
                            handle_data_for_signin(self.username, self.password)
                        elif event.key == pygame.K_BACKSPACE:
                            if self.username_input.collidepoint(pygame.mouse.get_pos()):
                                self.username = self.username[:-1]
                            elif self.password_input.collidepoint(pygame.mouse.get_pos()):
                                self.password = self.password[:-1]
                        else:
                            if self.username_input.collidepoint(pygame.mouse.get_pos()):
                                self.username += event.unicode
                            elif self.password_input.collidepoint(pygame.mouse.get_pos()):
                                self.password += event.unicode

            self.draw_signin_screen()
            pygame.display.flip()
            clock.tick(30)


if __name__ == "__main__":
    signin = Sign_in()
    signin.main()
