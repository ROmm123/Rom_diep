import pygame
import threading

from enemy import Enemy
from player import Player
from map import Map
from settings import settings
from weapon import Weapon
from normal_shot import NormalShot
from Network import Client
import random
from server_oop import Server


class Game:

    def __init__(self):
        pygame.init()
        self.setting = settings()
        self.players = []  # list of all the players in the game
        self.player_id_counter = 0  # player id counter
        self.Map = None  # first map initialization

        #ADD HP REGENERATION


    def run(self):
        # main game loop

        player1 = self.add_player()  # adds a player to the game
        enemy1 = self.add_enemy()
        self.initialize_map(player1)  # initializes the map

        while True:
            key_state = pygame.key.get_pressed()  # gets the state of all keyboard keys
            mouse_state = pygame.mouse.get_pressed()  # gets the state of the mouse
            chunk = self.MAP.calc_chunk()  # loads a chunk of the map
            self.MAP.draw_map(chunk)  # draws chunk
            self.shot_relative_vector = [0, 0]  # shot relative vector to control bullet movement
            # NEED TO CHANGE THE LOGIC OF THE SHOTS' MOVEMENT

            if self.Playerr.screen_position[0] > 0:
                if self.Playerr.move_button[0]:
                    self.shot_relative_vector[0] = self.Playerr.speed

                if self.Playerr.move_button[1]:
                    self.shot_relative_vector[0] = -self.Playerr.speed

            if self.Playerr.screen_position[1] > 0:
                if self.Playerr.move_button[2]:
                    self.shot_relative_vector[1] = self.Playerr.speed

                if self.Playerr.move_button[3]:
                    self.shot_relative_vector[1] = -self.Playerr.speed

            self.Playerr.handle_events_movement()
            self.Playerr.move()
            self.Playerr.draw()
            self.Playerr.handle_events_shapes(key_state)


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

            if self.Playerr.shape == "circle":  # if the player is a circle, it draws the weapon and allows to shoot
                self.Playerr.WEAPON.run_weapon()
                self.Playerr.handle_events_shots(key_state, mouse_state)

            else:
                self.Playerr.WEAPON.remove()

            self.Playerr.NORMAL_SHOT.update(self.shot_relative_vector)  # updates the normal shots
            self.Playerr.BIG_SHOT.update(self.shot_relative_vector)  # updates the big shots

            self.setting.update()  # updates the settings (timer)

            self.client.send_data(str(self.Playerr.screen_position))

    def connect_to_server(self):
        self.client = Client('localhost', 10009)

    def close_connections(self):
        self.client.close()
        self.server.close()

    def add_player(self):
        # adds a player to the game with a unique id
        player_id = self.player_id_counter
        self.player_id_counter += 1
        self.Playerr = Player(player_id, 0, 0, 30, "circle", self.setting.rand_color, self.setting)
        self.players.append(self.Playerr)
        return self.Playerr

    def add_enemy(self):
        enemy_id = self.player_id_counter
        self.player_id_counter += 1
        # Adjust the initial position of the enemy to be different from the player
        self.Enemy = Enemy(enemy_id, 0, 0, 30, "circle", self.setting.rand_color, self.setting)
        self.players.append(self.Enemy)
        return self.Enemy

    def initialize_map(self, player):
        # initializes the map
        self.MAP = Map(player, self.setting)




if __name__ == '__main__':
    game = Game()
    game.connect_to_server()
    game.run()
    game.close_connections()
    pygame.quit()
