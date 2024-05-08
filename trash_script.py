import threading
import time
import queue  # Import the queue module
import random
import pygame

from player import Player
from map import Map
from settings import setting
from Network import Client
from enemy_main import *
from moviepy.editor import VideoFileClip
#from chat_client import *
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


# game almost done
class Game():
    def __init__(self , username , password , x, y, speed_c, size_c, shield_c, hp_c_60, hp_c_30, hp_c_15, hp_c_5):
        pygame.init()
        self.setting = setting()
        self.player = Player(username , password , x, y, 28.5, self.setting.red, self.setting , speed_c, size_c, shield_c, hp_c_60, hp_c_30, hp_c_15, hp_c_5)
        self.map = Map(self.player, self.setting)
        self.num_enemies = 0
        self.enemy_threads = []
        self.client_main = Client('localhost', 55555, 55556)
        self.client_main.connect()
        self.crate_positions = self.client_main.receive_list_obj_once()
        self.static_object = StaticObjects(self.setting, 600 * 64, 675 * 64, self.crate_positions)
        self.client = Client(None, None)
        self.running = True
        # self.draw_queue = queue.PriorityQueue()  # Create a priority queue for drawing tasks
        # self.drawing_thread = DrawingThread(self.draw_queue, self.map, self.player)  # Create a drawing thread
        self.draw_event = threading.Event()  # Create an event for synchronization
        self.draw_event.set()  # Set the event initially
        # self.drawing_thread.start()  # Start the drawing thread
        self.speed_start_time = 0
        self.size_start_time = 0
        self.shield_start_time = 0
        self.FLAG_SERVER_1 = False
        self.FLAG_SERVER_2 = False
        self.FLAG_SERVER_3 = False
        self.FLAG_SERVER_4 = False
        self.flag_obj = False
        self.list_position_clients = []

    def run_therad(self, count):
        print("in draw thread")
        self.list_position_clients.append(self.player.screen_position)  # defult [x,y] for first time
        while True:
            try:
                print(self.list_position_clients)
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
                vector_enemy_position = [data["player_position_x"], data["player_position_y"]]
                self.list_position_clients[count] = vector_enemy_position
                enemy_instance.main()
                self.draw_event.set()


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
        print(self.crate_positions)
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
            '''if self.player.chat_flag:
                self.chat = ChatClient("localhost", 55557, self.player)'''
            if not self.player.chat_flag:
                if self.chat is not None:  # Check if self.chat exists before deleting
                    del self.chat
            for layer in range(2):
                chunk = self.map.calc_chunk(layer)
                self.map.draw_map(chunk)
            self.setting.darw_fps()

            mouse_pos = pygame.mouse.get_pos()
            self.player.draw(mouse_pos)

            '''
            for static_obj in self.static_object.Static_objects:
                self.static_object.move(static_obj)'''

            '''ability = self.static_object.give_ability()
            if ability is not None:
                self.player.stored_abilities.append(ability)'''
            # print(self.player.stored_abilities)



            collisions, position_collision = self.static_object.draw(
                self.player.screen_position[0],
                self.player.screen_position[1],
                self.setting,
                player_rect)

            ability = None
            print("collision", collisions)
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
                "ability": ability_size

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
                    self.client.close_enemies_Am()
                    # self.transition()
                    time.sleep(0.2)
                    self.list_position_clients = []
                    self.client.host = 'localhost'
                    self.client.port = 11110
                    self.client.enemies_or_obj_Am_port = 11119
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

            elif self.number_of_server == 2:
                if self.FLAG_SERVER_2 == False:
                    # Connect to server 1 if not already connected
                    print("already_close")
                    self.client.close()
                    self.client.close_enemies_Am()
                    self.transition()
                    time.sleep(0.2)
                    self.list_position_clients = []
                    self.client.host = 'localhost'
                    self.client.port = 22222
                    self.client.enemies_or_obj_Am_port = 22223
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

                    # Start handling enemies for server 4
                    threading.Thread(target=self.EnemiesAm_handling, args=(self.client,)).start()

                    # Send player data to server
                    self.client.send_data(data)
                else:
                    # Already connected to server 4, just send player data
                    self.client.send_data(data)

            if data_for_obj["position_collision"] is not None:
                self.client_main.send_data_obj_parmetrs(data_for_obj)

            if not self.flag_obj:
                threading.Thread(target=self.obj_recv).start()
                self.flag_obj = True

            if self.num_enemies > 0:
                self.draw_event.wait()
                hit_result = self.player.hit()
                self.player.hurt(hit_result)
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
                self.draw_event.clear()
            else:
                hit_result = self.player.hit()
                self.player.hurt(hit_result)
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

    def close_connections(self):
        self.client.close()
        self.client.close_enemies_Am()

    def EnemiesAm_handling(self, client):
        # Thread function to handle enemies received from server
        client.send_to_Enemies_Am()
        count = 0
        while True:
            try:
                enemies = client.receive_data_EnemiesAm()
            except:
                print("close thread handeling")
                break
            enemies = int(enemies)
            diff = enemies - self.num_enemies
            self.num_enemies = enemies

            print("diff " + str(diff))
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


def main(username , password , x, y, speed_c, size_c, shield_c, hp_c_60, hp_c_30, hp_c_15, hp_c_5):
    print("x : "+str(x))
    game = Game(username , password , x, y, speed_c, size_c, shield_c, hp_c_60, hp_c_30, hp_c_15, hp_c_5)
    try:
        print("starting game.run")
        game.run()
    finally:
        game.stop()
        game.close_connections()
        pygame.quit()



if __name__ == '__main__':

    main()
