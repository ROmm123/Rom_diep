import pygame
import threading

import enemy
from npc import NPC
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
        self.npcs = []  # list of all the npc in the game
        self.npc_id_counter = 0
        self.Map = None  # first map initialization
        self.inventory = inventory(self.setting)
        self.static_object = StaticObjects(self.setting, 600 * 64, 675 * 64)
        #ADD HP REGENERATION


    def run(self):
        # main game loop

        player1 = self.add_player()  # adds a player to the game
        enemy1 = self.add_enemy()
        npc1 = self.add_npc(enemy1, self.static_object.Static_objects)
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
            self.NPC.run(self.Playerr.screen_position[0], self.Playerr.screen_position[1], player_rect, self.Playerr.NORMAL_SHOT.get_shot_rects(self.Playerr.screen_position), self.static_object.Static_objects)
            collision = self.static_object.draw(self.Playerr.screen_position[0], self.Playerr.screen_position[1], self.setting,
                                    player_rect, self.Playerr.NORMAL_SHOT.get_shot_rects(self.Playerr.screen_position), self.NPC.SHOT.get_shot_rects(self.Playerr.screen_position),self.NPC.get_rect())
            print(collision)

            '''
            if collision != None:
                self.Playerr.hurt()
            self.Playerr.handle_events_shapes(key_state)
            '''

            if collision != None:
                if collision[2] == 0:
                    self.Playerr.NORMAL_SHOT.remove_shots.append(collision[1])
                    self.Playerr.NORMAL_SHOT.remove()
                if collision[2] == 1:
                    self.NPC.SHOT.remove_shots.append(collision[1])
                    self.NPC.SHOT.remove()

            if not npc1.is_alive():
                self.npcs.remove(npc1)
                self.npc_id_counter -=1

            if self.npc_id_counter < 2:     # if the npc is dead repawn a new one (need to be 100 enemies)
                npc1 =  self.add_npc(enemy1, self.static_object.Static_objects)


            enemy_status = enemy1.isntAlive()
            if not enemy_status:
                enemy1.move()
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
                check_hit = player1.hit(player_rect, player_id, self.NPC.SHOT.get_shot_rects(self.Playerr.screen_position))

                if check_hit != None:
                    if check_hit[0] == "normal shot":
                        enemy1.hit_damage = 5
                        player.hurt()
                    if check_hit[0] == "big shot":
                        enemy1.hit_damage = 15
                        player.hurt()
                    if check_hit[0] == "npc shot":
                        self.NPC.SHOT.remove_shots.append(check_hit[1])
                        self.NPC.SHOT.remove()
                        enemy1.hit_damage = 5
                        player.hurt()


                self.Playerr.WEAPON.run_weapon()
                self.Playerr.handle_events_shots(key_state, mouse_state)


            else:
                self.Playerr.WEAPON.remove()
            self.Playerr.NORMAL_SHOT.calc_relative(self.Playerr.screen_position,self.Playerr.move_button,self.Playerr.speed)
            self.Playerr.BIG_SHOT.calc_relative(self.Playerr.screen_position,self.Playerr.move_button,self.Playerr.speed)
            self.Playerr.NORMAL_SHOT.update()  # updates the normal shots
            self.NPC.SHOT.calc_relative(self.Playerr.screen_position, self.Playerr.move_button, self.Playerr.speed)
            self.NPC.SHOT.update()
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

    def add_npc(self, enemy, static_objects):
        npc_id = self.npc_id_counter
        self.npc_id_counter += 1
        self.NPC = NPC(npc_id,0, 0, 30, self.setting.red, self.setting, 400, Enemy.get_positions(enemy), static_objects)
        self.npcs.append(self.NPC)
        return self.NPC

    def initialize_map(self, player):
        # initializes the map
        self.MAP = Map(player, self.setting)




if __name__ == '__main__':
    game = Game()
    game.connect_to_server()
    game.run()
    game.close_connections()
    pygame.quit()
