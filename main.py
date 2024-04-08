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
from static_objects import StaticObjects

class Game:

    def __init__(self):
        pygame.init()
        self.setting = settings()
        self.players = []  # list of all the players in the game
        self.player_id_counter = 0  # player id counter
        self.Map = None  # first map initialization
        self.inventory = inventory(self.setting)
        self.static_object = StaticObjects(self.setting, 600 * 64, 675 * 64)
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


            player_rect = self.Playerr.get_rect_player()
            self.Playerr.handle_events_movement()
            self.Playerr.move()
            self.Playerr.draw()
            collision = self.static_object.draw(self.Playerr.screen_position[0], self.Playerr.screen_position[1], self.setting,
                                    player_rect, self.Playerr.NORMAL_SHOT.get_shot_rects(self.Playerr.screen_position))
            print(collision)

            '''
            if collision != None:
                self.Playerr.hurt()
            self.Playerr.handle_events_shapes(key_state)
            '''

            if collision != None:
                self.Playerr.NORMAL_SHOT.remove_shots.append(collision[1])
                self.Playerr.NORMAL_SHOT.remove()


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
            self.Playerr.NORMAL_SHOT.calc_relative(self.Playerr.screen_position,self.Playerr.move_button,self.Playerr.speed)
            self.Playerr.BIG_SHOT.calc_relative(self.Playerr.screen_position,self.Playerr.move_button,self.Playerr.speed)
            self.Playerr.NORMAL_SHOT.update()  # updates the normal shots
            self.Playerr.BIG_SHOT.update()  # updates the big shots

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
        self.Playerr = Player(player_id, 0, 0, 30, self.setting.rand_color, self.setting)
        self.players.append(self.Playerr)
        return self.Playerr

    def add_enemy(self):
        enemy_id = self.player_id_counter
        self.player_id_counter += 1
        # Adjust the initial position of the enemy to be different from the player
        self.Enemy = Enemy(enemy_id, 0, 0, 30, self.setting.rand_color, self.setting)
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
