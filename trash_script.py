import threading
import time
import queue  # Import the queue module
import random
import pygame

from player import Player
from npc import NPC
from npc import NPCS
from map import Map
from settings import setting
from Network import Client
from enemy_main import *
from moviepy.editor import VideoFileClip
from chat_client import *
from Network_chat import *
import os
from Static_Obj import StaticObjects
from npc import *


# game almost done
class Game():
    def __init__(self):
        pygame.init()
        self.setting = setting()
        self.player = Player(14700, 0, 30, self.setting.red, self.setting)
        self.map = Map(self.player, self.setting)
        self.num_enemies = 0
        self.enemy_threads = []
        self.client_main = Client('localhost', 55555, 55556)
        self.client_main.connect()
        self.crate_positions = self.client_main.receive_list_obj_once()
        self.static_object = StaticObjects(self.setting, 600 * 64, 675 * 64, self.crate_positions)
        self.client = Client(None, None)
        self.enemies_socket = Client_chat (None,None)
        self.running = True
        self.speed_start_time = 0
        self.size_start_time = 0
        self.shield_start_time = 0
        self.FLAG_SERVER_1 = False
        self.FLAG_SERVER_2 = False
        self.FLAG_SERVER_3 = False
        self.FLAG_SERVER_4 = False
        self.flag_obj = False
        self.flag_handle_enemies = False
        self.list_position_clients = []

        #npc init
        self.client_npc_socket = Client_chat('localhost',55558)
        self.client_npc_socket.connect()
        self.npc_positions = self.client_npc_socket.receive_npc_posiyions_dict()
        self.array_damage_list = self.client_npc_socket.receive_npc_posiyions_dict()
        print(self.npc_positions)
        print(self.array_damage_list)
        print(type(self.npc_positions))
        print(type(self.array_damage_list))



        self.NPCs = NPCS(None,None,None,None)


    def run_therad(self, count):
        print("in draw thread")
        #self.list_position_clients.append(self.player.screen_position)  # defult [x,y] for first time
        while True:
            try:
                data = self.client.receive_data()
                # print(data)
            except:
                print("socket is close")
                break

            if data == -1:
                print("socket is close")
                break

            if data != '0' and data:
                enemy_instance = enemy_main(data, self.player, self.setting)
                #vector_enemy_position = [data["player_position_x"], data["player_position_y"]]
                #self.list_position_clients[count] = vector_enemy_position
                enemy_instance.main()

    def obj_recv(self):
        print("in draw obj")

        while True:
            try:
                data = self.client_main.receive_obj_prameters()
                # print(data)
            except:
                print("socket obj is close")
                break

            if data["position_collision"] != None:

                # call prozedora hurt in class obj
                for static_obj in self.static_object.Static_objects:
                    if static_obj.position == data["position_collision"]:
                            static_obj.isAlive = False




    def run(self):
        self.speed_start_time = 0
        self.size_start_time = 0
        self.shield_start_time = 0
        collisions = None


        while self.running:
            key_state = pygame.key.get_pressed()
            player_rect = self.player.get_rect_player(self.player.radius, self.player.position[0],
                                                      self.player.position[1])
            self.player.handle_events_movement(self.client)
            self.chat = None
            if self.player.chat_flag:
                self.chat = ChatClient("localhost", 55557, self.player)
            if not self.player.chat_flag:
                if self.chat is not None:  # Check if self.chat exists before deleting
                    del self.chat
            for layer in range(2):
                chunk = self.map.calc_chunk(layer)
                self.map.draw_map(chunk)
            self.setting.darw_fps()

            mouse_pos = pygame.mouse.get_pos()
            self.player.draw(mouse_pos)


            """self.NPCs.run(self.player.screen_position[0], self.player.screen_position[1], player_rect,
                          self.player.NORMAL_SHOT.get_shot_rects(self.player.screen_position),
                          self.static_object.Static_objects, self.player.position)"""

            collisions, position_collision = self.static_object.draw(
                self.player.screen_position[0],
                self.player.screen_position[1],
                self.setting,
                player_rect)

            ability = None
            if collisions is not None:
                for collision in collisions:
                    if "player hit" in collision:
                        ability = self.static_object.give_ability()
                        self.player.stored_abilities.append(ability)

            speed = self.player.move(ability, collisions)
            self.player.update_ability()  # Update ability timers


            if position_collision is not None:
                data_for_obj = {
                    "position_collision": position_collision  # pos of player only
                }

            else:
                data_for_obj = {
                    "position_collision": None  # pos of player only
                }

            """if len(self.NPCs.NPCs) < 2:  # if the npc is dead repawn a new one (need to be 100 enemies)
                self.NPCs.add_player(self.player.position)"""

            ability_size = False
            self.player.handle_events_shots(key_state)
            self.player.handle_events_shapes(key_state)
            self.player.handle_events_abilities(key_state)
            if "Size" in self.player.ability:
                ability_size = True

            data = {

                "player_position_x": self.player.screen_position[0],
                "player_position_y": self.player.screen_position[1],
                "player_color": self.player.color,
                "player_radius": self.player.radius,
                "weapon_angle": self.player.angle,
                "normal_shot_velocity_x": self.player.NORMAL_SHOT.velocity[0],
                "normal_shot_velocity_y": self.player.NORMAL_SHOT.velocity[1],
                "normal_shot_start_x": self.player.NORMAL_SHOT.start_x,
                "normal_shot_start_y": self.player.NORMAL_SHOT.start_y,
                "damage dealt": self.player.hp.Damage,
                "big_shot_velocity_x": self.player.BIG_SHOT.velocity[0],
                "big_shot_velocity_y": self.player.BIG_SHOT.velocity[1],
                "big_shot_start_x": self.player.BIG_SHOT.start_x,
                "big_shot_start_y": self.player.BIG_SHOT.start_y,
                "ultimate_shot_velocity_x": self.player.ULTIMATE_SHOT.velocity[0],
                "ultimate_shot_velocity_y": self.player.ULTIMATE_SHOT.velocity[1],
                "ultimate_shot_start_x": self.player.ULTIMATE_SHOT.start_x,
                "ultimate_shot_start_y": self.player.ULTIMATE_SHOT.start_y,
                "ability": ability_size,
                "which_picture": self.player.num_of_image

            }

            data_for_main_server = {
                "player_position_x": self.player.screen_position[0],
                "player_position_y": self.player.screen_position[1]
            }

            self.client_main.send_data(data_for_main_server)
            data_from_main_server = self.client_main.recevie_only_data_from_main()
            data_from_main_server = data_from_main_server.split("_")
            self.number_of_server = int(data_from_main_server[0])

            if self.number_of_server == 1:
                if self.FLAG_SERVER_1 == False:
                    # Connect to server 1 if not already connected
                    self.client.close()
                    self.enemies_socket.close()
                    # self.transition()
                    self.list_position_clients = []
                    self.client.host = 'localhost'
                    self.enemies_socket.host = 'localhost'
                    self.client.port = 11110
                    self.enemies_socket.port = 11119

                    self.client.connect()
                    self.enemies_socket.connect()

                    # Set flags
                    self.FLAG_SERVER_1 = True
                    self.FLAG_SERVER_2 = False
                    self.FLAG_SERVER_3 = False
                    self.FLAG_SERVER_4 = False

                    self.NPCs = NPCS(self.setting, self.player.position, self.npc_positions, 1)
                    #TODO update the list pos from server if i want to go to another server

                    threading.Thread(target=self.EnemiesAm_handling).start()

                    # Start handling enemies for server 1

                    # Send player data to server
                    self.client.send_data(data)
                else:
                    # Already connected to server 1, just send player data
                    self.client.send_data(data)

            elif self.number_of_server == 2:
                if self.FLAG_SERVER_2 == False:
                    # Connect to server 1 if not already connected
                    print("already_close")
                    self.client.close()
                    self.enemies_socket.close()

                    self.transition()
                    time.sleep(0.2)
                    self.list_position_clients = []
                    self.client.host = 'localhost'
                    self.enemies_socket.host = 'localhost'
                    self.client.port = 22222
                    self.enemies_socket.port = 22223

                    self.client.connect()
                    self.enemies_socket.connect()

                    # Set flags
                    self.FLAG_SERVER_1 = False
                    self.FLAG_SERVER_2 = True
                    self.FLAG_SERVER_3 = False
                    self.FLAG_SERVER_4 = False

                    self.NPCs = NPCS(self.setting, self.player.position, self.npc_positions, 2)

                    threading.Thread(target=self.EnemiesAm_handling).start()

                    # Start handling enemies for server 2
                    # Send player data to server
                    self.client.send_data(data)
                else:
                    # Already connected to server 2, just send player data
                    self.client.send_data(data)

            elif self.number_of_server == 3:
                if self.FLAG_SERVER_3 == False:
                    # Connect to server 1 if not already connected
                    self.client.close()
                    self.client.close_enemies_Am()
                    self.transition()
                    time.sleep(0.2)
                    self.list_position_clients = []
                    self.client.host = 'localhost'
                    self.client.port = 33333
                    self.client.enemies_or_obj_Am_port = 33334
                    self.client.connect()
                    # Set flags
                    self.FLAG_SERVER_1 = False
                    self.FLAG_SERVER_2 = False
                    self.FLAG_SERVER_3 = True
                    self.FLAG_SERVER_4 = False

                    self.NPCs = NPCS(self.setting, self.player.position, self.npc_positions, 3)
                    #TODO update the list pos from server if i want to go to another server

                    # Start handling enemies for server 3
                    threading.Thread(target=self.EnemiesAm_handling, args=(self.client,)).start()

                    # Send player data to server
                    self.client.send_data(data)
                else:
                    # Already connected to server 3, just send player data
                    self.client.send_data(data)

            elif self.number_of_server == 4:
                if self.FLAG_SERVER_4 == False:
                    # Connect to server 1 if not already connected
                    self.client.close()
                    self.client.close_enemies_Am()
                    self.transition()
                    time.sleep(0.2)
                    self.list_position_clients = []
                    self.client.host = 'localhost'
                    self.client.port = 44444
                    self.client.enemies_or_obj_Am_port = 44445
                    self.client.connect()
                    # Set flags
                    self.FLAG_SERVER_1 = False
                    self.FLAG_SERVER_2 = False
                    self.FLAG_SERVER_3 = False
                    self.FLAG_SERVER_4 = True

                    self.NPCs = NPCS(self.setting, self.player.position, self.npc_positions, 4)
                    #TODO update the list pos from server if i want to go to another server

                    # Start handling enemies for server 4
                    threading.Thread(target=self.EnemiesAm_handling, args=(self.client,)).start()

                    # Send player data to server
                    self.client.send_data(data)
                else:
                    # Already connected to server 4, just send player data
                    self.client.send_data(data)

            if data_for_obj["position_collision"] is not None:
                self.client_main.send_data_obj_parmetrs(data_for_obj)
                print(data_for_obj)

            if not self.flag_obj:
                threading.Thread(target=self.obj_recv).start()
                self.flag_obj = True





            self.NPCs.run(self.player.screen_position[0], self.player.screen_position[1], player_rect,
                          self.player.NORMAL_SHOT.get_shot_rects(self.player.screen_position),
                          self.static_object.Static_objects, self.player.position)

            if len(self.NPCs.NPCs) < 2:  # if the npc is dead repawn a new one (need to be 100 enemies)
                self.NPCs.add_player(self.player.position)



            if self.num_enemies > 0:
                hit_result = self.player.hit()
                self.player.hurt(hit_result)

                for NPC in self.NPCs.NPCs:
                    npc_hit_result = self.player.npc_hit(NPC.SHOT.get_shot_rects(self.player.screen_position))
                    if "npc shot" in npc_hit_result:
                        NPC.SHOT.remove_shots.append(npc_hit_result[1])
                        NPC.SHOT.remove()

                    self.player.hurt(npc_hit_result)
                    NPC.SHOT.calc_relative(self.player.screen_position, self.player.move_button, self.player.speed)
                    NPC.SHOT.update()
                    NPC.SHOT.reset()


                self.player.NORMAL_SHOT.calc_relative(self.player.screen_position, self.player.move_button,
                                                      speed)
                self.player.BIG_SHOT.calc_relative(self.player.screen_position, self.player.move_button,
                                                   speed)
                self.player.ULTIMATE_SHOT.calc_relative(self.player.screen_position, self.player.move_button,
                                                        speed)
                self.player.NORMAL_SHOT.update()
                self.player.BIG_SHOT.update()
                self.player.ULTIMATE_SHOT.update()

                self.player.NORMAL_SHOT.reset()
                self.player.BIG_SHOT.reset()
                self.player.ULTIMATE_SHOT.reset()
                self.setting.update()

                # Reset the event for the next iteration
            else:
                hit_result = self.player.hit()
                self.player.hurt(hit_result)

                for NPC in self.NPCs.NPCs:
                    npc_hit_result = self.player.npc_hit(NPC.SHOT.get_shot_rects(self.player.screen_position))
                    if "npc shot" in npc_hit_result:
                        NPC.SHOT.remove_shots.append(npc_hit_result[1])
                        NPC.SHOT.remove()

                    self.player.hurt(npc_hit_result)
                    NPC.SHOT.calc_relative(self.player.screen_position, self.player.move_button, self.player.speed)
                    NPC.SHOT.update()
                    NPC.SHOT.reset()

                #self.player.hurt(hit_result)
                self.player.NORMAL_SHOT.calc_relative(self.player.screen_position, self.player.move_button, speed)
                self.player.BIG_SHOT.calc_relative(self.player.screen_position, self.player.move_button, speed)
                self.player.ULTIMATE_SHOT.calc_relative(self.player.screen_position, self.player.move_button, speed)
                self.player.NORMAL_SHOT.update()
                self.player.BIG_SHOT.update()
                self.player.ULTIMATE_SHOT.update()

                self.player.NORMAL_SHOT.reset()
                self.player.BIG_SHOT.reset()
                self.player.ULTIMATE_SHOT.reset()
                self.setting.update()

    def close_connections(self):
        self.client.close()
        self.client.close_enemies_Am()

    def EnemiesAm_handling(self):
        # Thread function to handle enemies received from server
        time.sleep(2)
        self.enemies_socket.send_to_Enemies_Am()
        count = 0
        while True:
            try:
                enemies = self.enemies_socket.receive_data_EnemiesAm()
            except:
                enemies = self.num_enemies - 1
                diff = enemies - self.num_enemies
                self.num_enemies = enemies
                print(diff)
                if diff < 0:
                    for _ in range(-diff):
                        print("join th")
                        if self.enemy_threads:
                            thread = self.enemy_threads.pop()
                            thread.join()
                self.num_enemies = 0
                print("close thread handeling")
                break

            enemies = int(enemies)
            diff = enemies - self.num_enemies
            self.num_enemies = enemies

            print(diff)

            if diff > 0:
                for _ in range(diff):
                    enemy_thread = threading.Thread(target=self.run_therad, args=(count,))
                    enemy_thread.start()
                    count = count + 1
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
            thread.running = False
            thread.join()
        # self.drawing_thread.join()  # Wait for the drawing thread to exit
        self.close_connections()
        pygame.quit()

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


    #def add_npc(self, static_objects):  # enemy,
     #   npc_id = self.npc_counter
      #  self.npc_counter += 1
       # self.NPC = NPC(npc_id, 0, 0, 30, self.setting.red, self.setting, 400, static_objects)   # Enemy.get_positions(enemy),
        #self.npcs.append(self.NPC)
        #return self.NPC

    def transition(self):
        # makes sure the player doesn't keep moving in the direction of the transition
        for i in range(len(self.player.move_button)):
            self.player.move_button[i] = False
        # transition between servers
        video_path = "shmulik2.mp4"
        if not os.path.exists(video_path):
            print("Video file not found.")
            return
        clip = VideoFileClip(video_path)
        clip.preview()
        clip.close()


if __name__ == '__main__':
    game = Game()

    try:
        print("starting game.run")
        game.run()
    finally:
        game.stop()
        game.close_connections()
        pygame.quit()
