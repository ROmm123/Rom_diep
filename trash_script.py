import threading
import time
import queue  # Import the queue module
import random
import pygame

from player import Player
from map import Map
from settings import setting
from weapon import Weapon
from Network import Client
from enemy_main import *
from moviepy.editor import VideoFileClip

import os
from Static_Obj import StaticObjects

'''class DrawingThread(threading.Thread):
    def __init__(self, draw_queue, map, player):
        super().__init__()
        self.draw_queue = draw_queue
        self.map = map
        self.player = player

    def run(self):
        while True:
            # Get the next drawing task from the queue
            task = self.draw_queue.get()
            if task is not None:
                priority, obj = task
                print(priority)
                try:
                    if priority == 1:
                        enemy = enemy_main(obj[0],obj[1],obj[2],obj[3])
                        enemy.main()
                        self.draw_queue.task_done()
                    elif priority == 0:
                        self.draw_queue.task_done()
                except Exception as e:
                    print(e)'''


class Game():
    def __init__(self):
        pygame.init()
        self.setting = setting()
        self.player = Player(12000, 0, 30, self.setting.red, self.setting)
        self.map = Map(self.player, self.setting)
        self.num_enemies = 0
        self.enemy_threads = []
        self.client_main = Client('localhost', 55557,55558)
        self.client_main.connect()
        self.crate_positions = self.client_main.receive_list_obj_once()
        self.static_object = StaticObjects(self.setting, 600 * 64, 675 * 64, self.crate_positions)
        self.client = Client(None, None)
        self.running = True
        # self.draw_queue = queue.PriorityQueue()  # Create a priority queue for drawing tasks
        # self.drawing_thread = DrawingThread(self.draw_queue, self.map, self.player)  # Create a drawing thread


        self.FLAG_SERVER_1 = False
        self.FLAG_SERVER_2 = False
        self.FLAG_SERVER_3 = False
        self.FLAG_SERVER_4 = False

        self.ID = None


    def run(self):
        print(self.crate_positions)
        while self.running:
            key_state = pygame.key.get_pressed()
            mouse_state = pygame.mouse.get_pressed()
            player_rect = self.player.get_rect_player(self.player.radius,self.player.position[0],self.player.position[1])
            self.player.handle_events_movement(self.client)
            radius = self.player.radius


            for layer in range(2):
                chunk = self.map.calc_chunk(layer)
                self.map.draw_map(chunk)
            self.player.draw(radius)

            speed = self.player.speed

            if "Speed" in self.player.ability:
                self.player.move(speed * 1.2)
            else:
                self.player.move(speed)

            if "Health" in self.player.ability:
                self.player.ability.remove("Health")
                self.player.hp.Damage = 0

            if "Size" in self.player.ability:
                self.player.ability.remove("Size")
                radius *= 0.64
                self.player.WEAPON.rect_width *= 0.64
                self.player.WEAPON.rect_height *= 0.64

            self.player.draw(radius)
            for static_obj in self.static_object.Static_objects:
                self.static_object.move(static_obj)

            ability = self.static_object.give_ability()
            if ability is not None:
                self.player.ability.append(ability)

            self.player.WEAPON.run_weapon()
            self.player.handle_events_shots(key_state, mouse_state)

            collisions, pos_col = self.static_object.draw(self.player.screen_position[0],
                                                          self.player.screen_position[1],
                                                          self.setting,
                                                          player_rect,
                                                          self.player.NORMAL_SHOT.get_shot_rects(
                                                              self.player.screen_position))

            if collisions is not None:
                for collision in collisions:
                    if "shot index" in collision:
                        self.player.NORMAL_SHOT.remove_shots.append(collision[1])
                        self.player.NORMAL_SHOT.remove()
                    if "player hit" in collision:
                        damage = 1
                        self.player.hurt(damage)
                    if "player been hit" in collision:
                        self.player.speed = 3


            data =  {
                "ID" : self.ID ,
                "rect_center_x": self.player.WEAPON.rect_center_x,
                "rect_center_y": self.player.WEAPON.rect_center_y,
                "rect_width": self.player.WEAPON.rect_width,
                "rect_height": self.player.WEAPON.rect_height,
                "tangent_x": self.player.WEAPON.tangent_x,
                "player_position_x": self.player.screen_position[0],
                "player_position_y": self.player.screen_position[1],
                "player_radius": self.player.radius,
                "weapon_angle": self.player.WEAPON.angle,
                "shot_velocity_x": self.player.NORMAL_SHOT.velocity[0],
                "shot_velocity_y": self.player.NORMAL_SHOT.velocity[1],
                "shot_start_x": self.player.NORMAL_SHOT.start_x,
                "shot_start_y": self.player.NORMAL_SHOT.start_y,
                "damage dealt": self.player.hp.Damage

            }





            self.check_server()
            if self.number_of_server == 1:
                if self.FLAG_SERVER_1 == False:
                    # Connect to server 1 if not already connected
                    self.client.close()
                    self.client.host = 'localhost'
                    self.client.port = 11111
                    self.client.enemies_or_obj_Am_port = 11112
                    self.client.connect()
                    # Set flags
                    self.FLAG_SERVER_1 = True
                    self.FLAG_SERVER_2 = False
                    self.FLAG_SERVER_3 = False
                    self.FLAG_SERVER_4 = False

                    threading.Thread(target=self.EnemiesAm_handling, args=(self.client,)).start()
                    print("passed thread")

                    # Send player data to server
                    self.client.send_data(data)
                else:
                    # Already connected to server 1, just send player data
                    self.client.send_data(data)

            elif self.number_of_server == 2:
                if self.FLAG_SERVER_2 == False:
                    # Connect to server 1 if not already connected
                    print("alredy_close")
                    self.client.close()
                    #self.transition()
                    self.client.host = 'localhost'
                    self.client.port = 22222
                    self.client.enemies_or_obj_Am_port = 22223
                    self.client.connect()
                    # Set flags
                    self.FLAG_SERVER_1 = False
                    self.FLAG_SERVER_2 = True
                    self.FLAG_SERVER_3 = False
                    self.FLAG_SERVER_4 = False

                    threading.Thread(target=self.EnemiesAm_handling, args=(self.client,)).start()

                    # Send player data to server
                    self.client.send_data(data)
                else:
                    # Already connected to server 2, just send player data
                    self.client.send_data(data)

            elif self.number_of_server == 3:
                if self.FLAG_SERVER_3 == False:
                    # Connect to server 1 if not already connected
                    self.client.close()
                    self.client.host = 'localhost'
                    self.client.port = 33333
                    self.client.enemies_or_obj_Am_port = 33334
                    self.client.connect()
                    # Set flags
                    self.FLAG_SERVER_1 = False
                    self.FLAG_SERVER_2 = False
                    self.FLAG_SERVER_3 = True
                    self.FLAG_SERVER_4 = False

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
                    self.client.host = 'localhost'
                    self.client.port = 44444
                    self.client.enemies_or_obj_Am_port = 44445
                    self.client.connect()
                    # Set flags
                    self.FLAG_SERVER_1 = False
                    self.FLAG_SERVER_2 = False
                    self.FLAG_SERVER_3 = False
                    self.FLAG_SERVER_4 = True

                    threading.Thread(target=self.EnemiesAm_handling, args=(self.client,)).start()

                    # Send player data to server
                    self.client.send_data(data)
                else:
                    # Already connected to server 4, just send player data
                    self.client.send_data(data)






            if self.num_enemies > 0:
                print("in if , num_enemies >0")
                hit_result = self.player.hit()
                damage = 0
                if "normal shot" in hit_result:
                    amount = hit_result.count("normal shot")
                    damage += 3*amount

                self.player.hurt(damage)


                self.player.NORMAL_SHOT.calc_relative(self.player.screen_position, self.player.move_button,
                                                      self.player.speed)
                self.player.NORMAL_SHOT.update()
                self.player.NORMAL_SHOT.reset()
                print("before receive")
                data_list = self.client.receive_data()
                print("data list BEFORE REMOVE_MY_ID : " + str(data_list))
                data_list = self.remove_my_id(data_list) # [{} ,{} , {}]
                print("data list : "+str(data_list))
                if data_list:
                    for j in data_list: # [{j} , {j}]
                        enemy_main(j,self.setting,self.player,self.player.WEAPON)
                self.setting.update()

            else:
                self.player.hit()
                self.player.NORMAL_SHOT.calc_relative(self.player.screen_position, self.player.move_button,
                                                      self.player.speed)
                self.player.NORMAL_SHOT.update()
                self.player.NORMAL_SHOT.reset()
                self.setting.update()

    def close_connections(self):
        self.client.close()


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
    def check_server(self):
        data_for_main_server = {
            "player_position_x": self.player.screen_position[0],
            "player_position_y": self.player.screen_position[1]
        }

        self.client_main.send_data(data_for_main_server)
        data_from_main_server = self.client_main.recevie_only_data_from_main()
        data_from_main_server = data_from_main_server.split("_")
        self.number_of_server = int(data_from_main_server[0])

    def EnemiesAm_handling(self, client):
        # Thread function to handle enemies received from server
        client.send_to_Enemies_Am()
        while True:
            try:
                enemies = client.receive_data_EnemiesAm()
                self.num_enemies = enemies
                print("added enemy , enemies : "+str(self.num_enemies))
            except:
                print("close thread handeling")
                break


    def transition(self):
        # makes sure the player doesn't keep moving in the direction of the transition
        for i in range(len(self.player.move_button)):
            self.player.move_button[i] = False
        # transition between servers
        video_path = "shmulik.mp4"
        if not os.path.exists(video_path):
            print("Video file not found.")
            return
        clip = VideoFileClip(video_path)
        clip.preview()
        clip.close()

    def remove_my_id(self,data) -> list :
        for dictio in data:
            if self.ID == dictio["ID"]:
                data.remove(dictio)









if __name__ == '__main__':
    game = Game()
    game.ID = game.client_main.receive_data_ID()
    print("ID : "+str(game.ID))
    try:
        print("starting game.run")
        game.run()
    finally:
        game.close_connections()
        pygame.quit()
