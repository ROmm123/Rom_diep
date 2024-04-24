import pygame
import threading
from enemy import Enemy
from player import Player
from map import Map
from settings import settings
from weapon import Weapon
from normal_shot import *
from Network import Client
import random
from server_oop import Server
from inventory import *
from stat_obj import StaticObjects
from enemy_main import Enemy_main


class EnemyThread(threading.Thread):
    def __init__(self, client, player, setting, weapon):
        super().__init__()
        self.client = client
        self.player = player
        self.setting = setting
        self.weapon = weapon

    def run(self):
        print("in draw thread")

        while True:
            if self.client.client_socket is None:
                print("Client disconnected")
                break
            data = self.client.receive_data()

            if data != '0' and data:
                enemy_instance = Enemy_main(data, self.player, self.setting, self.weapon)
                enemy_instance.main()


class Game:

    def __init__(self):
        pygame.init()
        self.setting = settings()
        self.players = []  # list of all the players in the game
        self.player_id_counter = 0  # player id counter
        self.Map = None  # first map initialization
        self.inventory = inventory(self.setting)
        self.num_enemies = 0
        self.enemy_threads = []
        self.client_main = Client('localhost', 55555)
        self.client_main.connect()
        self.crate_positions = self.client_main.receive_list_obj()
        self.static_object = StaticObjects(self.setting, 600 * 64, 675 * 64, self.crate_positions)
        self.client = Client(None, None)  # defult
        self.FLAG_SERVER_1 = False
        self.FLAG_SERVER_2 = False
        self.FLAG_SERVER_3 = False
        self.FLAG_SERVER_4 = False

        # ADD HP REGENERATION

    def run(self):
        # main game loop
        player1 = self.add_player()  # adds a player to the game
        enemy1 = self.add_enemy()
        self.initialize_map(player1)  # initializes the map
        radius = self.Playerr.radius

        while True:
            key_state = pygame.key.get_pressed()  # gets the state of all keyboard keys
            mouse_state = pygame.mouse.get_pressed()  # gets the state of the mouse
            chunk = self.MAP.calc_chunk()  # loads a chunk of the map
            self.MAP.draw_map(chunk)  # draws chunk
            self.shot_relative_vector = [0, 0]  # shot relative vector to control bullet movement

            player_rect = self.Playerr.get_rect_player()
            self.Playerr.handle_events_movement(self.client)
            speed = self.Playerr.speed

            if "Speed" in self.Playerr.ability:
                self.Playerr.move(speed * 1.2)
            else:
                self.Playerr.move(speed)

            if "Health" in self.Playerr.ability:
                self.Playerr.ability.remove("Health")
                self.Playerr.hp.Damage = 0

            if "Size" in self.Playerr.ability:
                self.Playerr.ability.remove("Size")
                radius *= 0.64
                self.Playerr.WEAPON.rect_width *= 0.64
                self.Playerr.WEAPON.rect_height *= 0.64

            self.Playerr.draw(radius)
            for static_obj in self.static_object.Static_objects:
                self.static_object.move(static_obj)

            ability = self.static_object.give_ability()
            if ability is not None:
                self.Playerr.ability.append(ability)
            # if self.Playerr.ability:
            # print(self.Playerr.ability)

            collisions = self.static_object.draw(self.Playerr.screen_position[0], self.Playerr.screen_position[1],
                                                 self.setting,
                                                 player_rect,
                                                 self.Playerr.NORMAL_SHOT.get_shot_rects(self.Playerr.screen_position))

            # print(collision)

            '''
            if collision != None:
                self.Playerr.hurt()
            self.Playerr.handle_events_shapes(key_state)
            '''

            # collisions

            if collisions is not None:
                for collision in collisions:
                    if "shot index" in collision:
                        self.Playerr.NORMAL_SHOT.remove_shots.append(collision[1])
                        self.Playerr.NORMAL_SHOT.remove()
                    if "player hit" in collision:
                        self.Playerr.hurt()
                    if "player been hit" in collision:
                        self.Playerr.speed = 3

            enemy_status = enemy1.isAlive()
            if not enemy_status:
                enemy1.position[0] = (enemy1.center[0] - self.Playerr.screen_position[0])
                enemy1.position[1] = (enemy1.center[1] - self.Playerr.screen_position[1])
                enemy1.draw()
            else:
                self.players.remove(enemy1)

            player_status = self.Playerr.isAlive()  # checks if the player is dead
            if player_status:  # if the player is dead, respawn
                game = Game()
                game.connect_to_server()
                game.run()
                game.close_connections()
                pygame.quit()

            for player in self.players:  # checks if the shot hit any of the players
                player_rect = player.get_rect_player()
                player_id = player.player_id
                check_hit = player1.hit(player_rect, player_id)
                if check_hit == "normal shot":
                    enemy1.hit_damage = 5
                    player.hurt()
                if check_hit == "big shot":
                    enemy1.hit_damage = 15
                    player.hurt()

                self.Playerr.WEAPON.run_weapon()
                self.Playerr.handle_events_shots(key_state, mouse_state)


            else:
                self.Playerr.WEAPON.remove()
            self.Playerr.NORMAL_SHOT.calc_relative(self.Playerr.screen_position, self.Playerr.move_button,
                                                   self.Playerr.speed)
            self.Playerr.BIG_SHOT.calc_relative(self.Playerr.screen_position, self.Playerr.move_button,
                                                self.Playerr.speed)
            self.Playerr.NORMAL_SHOT.update()  # updates the normal shots
            self.Playerr.BIG_SHOT.update()  # updates the big shots
            self.setting.update()  # updates the settings (timer)

            data_for_main_server = {
                "player_position_x": self.Playerr.screen_position[0],
                "player_position_y": self.Playerr.screen_position[1]
            }

            data = {
                "rect_center_x": self.Playerr.WEAPON.rect_center_x,
                "rect_center_y": self.Playerr.WEAPON.rect_center_y,
                "rect_width": self.Playerr.WEAPON.rect_width,
                "rect_height": self.Playerr.WEAPON.rect_height,
                "tangent_x": self.Playerr.WEAPON.tangent_x,
                "player_position_x": self.Playerr.screen_position[0],
                "player_position_y": self.Playerr.screen_position[1],
                "player_color": self.Playerr.color,
                "player_radius": self.Playerr.radius,
                "weapon_angle": self.Playerr.WEAPON.angle
            }

            self.client_main.send_data(data_for_main_server)
            number_of_server = self.client_main.receive_data()
            #print(str (self.Playerr.screen_position[0])+" , "+str(number_of_server))

            if number_of_server == 1:
                if self.FLAG_SERVER_1 == False:
                    # Connect to server 1 if not already connected
                    self.client.host = 'localhost'
                    self.client.port = 11111
                    self.client.enemies_Am_port = 11112
                    self.client.connect()
                    # Set flags
                    self.FLAG_SERVER_1 = True
                    self.FLAG_SERVER_2 = False
                    self.FLAG_SERVER_3 = False
                    self.FLAG_SERVER_4 = False

                    # Start handling enemies for server 1
                    threading.Thread(target=self.EnemiesAm_handling, args=(self.client,)).start()

                    # Send player data to server
                    self.client.send_data(data)
                else:
                    # Already connected to server 1, just send player data
                    self.client.send_data(data)

            elif number_of_server == 2:
                if self.FLAG_SERVER_2 == False:
                    # Connect to server 1 if not already connected
                    self.client.host = 'localhost'
                    self.client.port = 22222
                    self.client.enemies_Am_port = 22223
                    self.client.connect()
                    # Set flags
                    self.FLAG_SERVER_1 = False
                    self.FLAG_SERVER_2 = True
                    self.FLAG_SERVER_3 = False
                    self.FLAG_SERVER_4 = False

                    # Start handling enemies for server 2
                    threading.Thread(target=self.EnemiesAm_handling, args=(self.client,)).start()

                    # Send player data to server
                    self.client.send_data(data)
                else:
                    # Already connected to server 2, just send player data
                    self.client.send_data(data)

            elif number_of_server == 3:
                if self.FLAG_SERVER_3 == False:
                    # Connect to server 1 if not already connected
                    self.client.host = 'localhost'
                    self.client.port = 33333
                    self.client.enemies_Am_port = 33334
                    self.client.connect()
                    # Set flags
                    self.FLAG_SERVER_1 = False
                    self.FLAG_SERVER_2 = False
                    self.FLAG_SERVER_3 = True
                    self.FLAG_SERVER_4 = False

                    # Start handling enemies for server 3
                    threading.Thread(target=self.EnemiesAm_handling, args=(self.client,)).start()

                    # Send player data to server
                    self.client.send_data(data)
                else:
                    # Already connected to server 3, just send player data
                    self.client.send_data(data)

            elif number_of_server == 4:
                if self.FLAG_SERVER_4 == False:
                    # Connect to server 1 if not already connected
                    self.client.host = 'localhost'
                    self.client.port = 44444
                    self.client.enemies_Am_port = 44445
                    self.client.connect()
                    # Set flags
                    self.FLAG_SERVER_1 = False
                    self.FLAG_SERVER_2 = False
                    self.FLAG_SERVER_3 = False
                    self.FLAG_SERVER_4 = True

                    # Start handling enemies for server 4
                    threading.Thread(target=self.EnemiesAm_handling, args=(self.client,)).start()

                    # Send player data to server
                    self.client.send_data(data)
                else:
                    # Already connected to server 4, just send player data
                    self.client.send_data(data)

    def close_connections(self):
        # Close the connection to the main server
        self.client_main.close()

    def generate_random_with_condition_x(self):
        # Generate a random x position for player/enemy with specific condition
        while True:
            random_number_x = random.randint(0, 30000)
            if random_number_x < 267 * 64 or random_number_x > 320 * 64:
                return random_number_x

    def generate_random_with_condition_y(self):
        # Generate a random y position for player/enemy with specific condition
        while True:
            random_number_y = random.randint(0, 37000)
            if random_number_y < (294 * 64 + 32) or random_number_y > 398 * 64:
                return random_number_y

    def add_player(self):
        # Add a player to the game
        self.player_id_counter = self.num_enemies
        player_id = self.player_id_counter

        self.Playerr = Player(player_id, 17000, 0, 30, self.setting.rand_color, self.setting)
        self.players.append(self.Playerr)
        return self.Playerr

    def add_enemy(self):
        # Add an enemy to the game
        self.player_id_counter = self.num_enemies
        enemy_id = self.player_id_counter
        self.Enemy = Enemy(enemy_id, 0, 0, 60, self.setting.rand_color, self.setting)
        self.players.append(self.Enemy)
        return self.Enemy

    def initialize_map(self, player):
        # Initialize the game map
        self.MAP = Map(player, self.setting)

    def EnemiesAm_handling(self, client):
        # Thread function to handle enemies received from server
        client.send_to_Enemies_Am()
        while True:
            enemies = client.receive_data_EnemiesAm()
            enemies = int(enemies)
            diff = enemies - self.num_enemies
            self.num_enemies = enemies

            print("diff "+ str(diff))
            if diff > 0:
                for _ in range(diff):
                    enemy_thread = EnemyThread(client, self.Playerr, self.setting, self.Playerr.WEAPON)
                    enemy_thread.start()
                    self.enemy_threads.append(enemy_thread)
            elif diff < 0:
                for _ in range(-diff):
                    print("join th")
                    if self.enemy_threads:
                        thread = self.enemy_threads.pop()
                        thread.join()

    def stop(self):
        self.running = False
        for thread in self.enemy_threads:
            thread.join()


if __name__ == '__main__':
    game = Game()

    try:
        print("starting game.run")
        game.run()
    finally:
        game.stop()
        game.close_connections()
        pygame.quit()
