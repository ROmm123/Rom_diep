import socket
import threading
import time
import queue  # Import the queue module
import pygame
from player import Player
from map import Map
from settings import setting
from weapon import Weapon
from Network import Client
from enemy_main import *
import queue

class Game():
    def __init__(self , x, y, speed_c, size_c, shield_c, hp_c_60, hp_c_30, hp_c_15, hp_c_5):
        pygame.init()
        self.setting = setting()
        self.player = Player(0, 0, 35, self.setting.red, self.setting)
        self.map = Map(self.player, self.setting)
        self.weapon = Weapon(20, 20, self.setting.green_fn, self.player.radius, self.setting, self.player.center_x,
                             self.player.center_y, self.player.angle)
        self.client = Client('localhost', 10022, 10020)
        self.num_enemies = 0
        self.enemy_threads = 0
        self.running = True
        self.draw_queue = queue.Queue()
        # self.drawing_thread = DrawingThread(self.draw_queue, self.map, self.player)  # Create a drawing thread
        self.draw_event = threading.Event()  # Create an event for synchronization  # Set the event initially
        # self.drawing_thread.start()  # Start the drawing thread
        self.index = 0
        self.lock = threading.Lock()


    def run_thread(self , index):
        print("in draw thread")
        while self.running:
            data = self.client.receive_data()

            if data:
                enemy_instance = enemy_main(data, self.player, self.setting, self.weapon)
                self.draw_queue.put(enemy_instance)
                print(f"thread {index} q size {self.draw_queue.qsize()} ")
                self.draw_event.wait()
                print("finished waiting , queue size :"+str(self.draw_queue.qsize()))
            self.draw_event.clear()



    def run(self):
        while self.running:
            self.player.calc_angle()
            self.weapon = Weapon(20, 20, self.setting.green_fn, self.player.radius, self.setting,
                                 self.player.center_x, self.player.center_y, self.player.angle)
            self.player.handle_events()
            self.player.move()
            chunk = self.map.calc_chunk()
            self.map.draw_map(chunk)
            self.player.draw()

            self.weapon.run_weapon()
            data = {
                "rect_center_x": self.weapon.rect_center_x,
                "rect_center_y": self.weapon.rect_center_y,
                "rect_width": self.weapon.rect_width,
                "rect_height": self.weapon.rect_height,
                "tangent_x": self.weapon.tangent_x,
                "player_position_x": self.player.screen_position[0],
                "player_position_y": self.player.screen_position[1],
                "player_color": self.player.color,
                "player_radius": self.player.radius,
                "weapon_angle": self.weapon.angle
            }
            self.client.send_data(data)

            if self.num_enemies > 0 and self.draw_queue.qsize() == self.num_enemies:
                with self.lock:
                    print("num enemies: "+str(self.num_enemies))
                    for i in range(0,self.num_enemies):
                        enemy = self.draw_queue.get()
                        print("consuming , q size: "+str(self.draw_queue.qsize()))
                        enemy.main()
                    if not self.draw_event.is_set():
                        print("set event")
                        self.draw_event.set()
                    self.setting.update()
                          # Signal to producer thread that items have been consumed


            else:
                self.setting.update()

    def close_connections(self):
        self.client.close()

    def EnemiesAm_handling(self):
        self.client.send_to_Enemies_Am()
        self.index = 0
        while True:
            enemies = self.client.receive_data_EnemiesAm()
            print(enemies)
            enemies = int(enemies)
            diff = enemies - self.num_enemies
            self.num_enemies = enemies
            if diff > 0:
                for _ in range(diff):
                    threading.Thread(target=self.run_thread , args=(self.index,)).start()
                    self.index += 1
                    time.sleep(0.8)
                    self.enemy_threads+=1
            elif diff < 0:
                for _ in range(-diff):
                    # CHANGE!!!! LIDOR IDEA
                    thread = self.enemy_threads.pop()
                    thread.running = False
                    thread.join()

    def stop(self):
        self.running = False
        self.close_connections()
        pygame.quit()


def main(x, y, speed_c, size_c, shield_c, hp_c_60, hp_c_30, hp_c_15, hp_c_5):
    print("x : "+str(x))
    game = Game(x, y, speed_c, size_c, shield_c, hp_c_60, hp_c_30, hp_c_15, hp_c_5)
    threading.Thread(target=game.EnemiesAm_handling).start()
    try:
        print("starting game.run")
        game.run()
    finally:
        game.stop()


if __name__ == '__main__':
    main()

