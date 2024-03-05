from map import *



class Player():

    def __init__(self , x , y , radius , color , setting):
        self.surface = setting.surface
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = 5
        self.center_x = 400
        self.center_y = 300

    def draw(self):
        pygame.draw.circle(self.surface , self.color ,(self.center_x , self.center_y) , self.radius)

    def move(self):
        move_left = False
        move_right = False
        move_up = False
        move_down = False

        # Main game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    move_left = True
                elif event.key == pygame.K_d:
                    move_right = True
                elif event.key == pygame.K_w:
                    move_up = True
                elif event.key == pygame.K_s:
                    move_down = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    move_left = False
                elif event.key == pygame.K_d:
                    move_right = False
                elif event.key == pygame.K_w:
                    move_up = False
                elif event.key == pygame.K_s:
                    move_down = False

        # Update screen position based on movement direction
        if move_left:
            self.x -= self.speed
            if self.x < 0:
                self.x += self.speed

        if move_right:
            self.x += self.speed

        if move_up:
            self.y -= self.speed
            if self.y < 0:
                self.y += self.speed

        if move_down:
            self.y += self.speed

        return self.x










