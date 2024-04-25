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


class EnemyThread(threading.Thread):
    def __init__(self, client, player, setting, weapon, draw_event): #draw_queue
        super().__init__()
        self.client = client
        self.player = player
        self.setting = setting
        self.weapon = weapon
        self.running = True
        self.draw_event = draw_event
        #self.draw_queue = draw_queue

    def run(self):
        print("in draw thread")
        while self.running:
            data = self.client.receive_data()
            #print(data)

            if data:
                print("yes")
                enemy_instance = enemy_main(data, self.player, self.setting, self.weapon)
                enemy_instance.main()
                self.draw_event.set()


                # Enqueue drawing task for the enemy
                #self.draw_queue.put((1, [data , self.player , self.setting , self.weapon]))  # Wrap enemy_mainn in a tuple






class Game():
    def __init__(self):
        pygame.init()
        self.setting = setting()
        self.player = Player(0, 0, 35, self.setting.red, self.setting)
        self.map = Map(self.player, self.setting)
        self.weapon = Weapon(20, 20, self.setting.green, self.player, self.setting)
        self.client = Client('localhost', 10018, 10023)
        self.num_enemies = 0
        self.enemy_threads = []
        self.running = True
        #self.draw_queue = queue.PriorityQueue()  # Create a priority queue for drawing tasks
        #self.drawing_thread = DrawingThread(self.draw_queue, self.map, self.player)  # Create a drawing thread
        self.draw_event = threading.Event()  # Create an event for synchronization
        self.draw_event.set()  # Set the event initially
        #self.drawing_thread.start()  # Start the drawing thread

    def run(self):
        while self.running:
            key_state = pygame.key.get_pressed()
            mouse_state = pygame.mouse.get_pressed()
            self.weapon = Weapon(20, 20, self.setting.green, self.player, self.setting)
            self.player.handle_events_movement()
            self.player.move()

            for layer in range(2):
                chunk = self.map.calc_chunk(layer)
                self.map.draw_map(chunk)
            self.player.draw()

            self.weapon.run_weapon()
            self.player.handle_events_shots(key_state, mouse_state)
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
                "weapon_angle": self.weapon.angle,
                "shot_mouse_x":self.player.NORMAL_SHOT.mouse_x,
                "shot_mouse_y": self.player.NORMAL_SHOT.mouse_y,
                "shot_magnitude":self.player.NORMAL_SHOT.magnitude,
                "shot_direction":self.player.NORMAL_SHOT.direction,
                "shot_start_x":self.player.NORMAL_SHOT.start_x,
                "shot_start_y": self.player.NORMAL_SHOT.start_y,



            }
            self.client.send_data(data)
            if self.num_enemies>0:
                self.draw_event.wait()
                self.player.NORMAL_SHOT.calc_relative(self.player.screen_position,self.player.move_button,self.player.speed)
                self.player.NORMAL_SHOT.update()
                self.player.NORMAL_SHOT.reset()
                self.setting.update()

            # Reset the event for the next iteration
                self.draw_event.clear()
            else:
                self.player.NORMAL_SHOT.calc_relative(self.player.screen_position,self.player.move_button,self.player.speed)
                self.player.NORMAL_SHOT.update()
                self.player.NORMAL_SHOT.reset()
                self.setting.update()

    def close_connections(self):
        self.client.close()

    def EnemiesAm_handling(self):
        self.client.send_to_Enemies_Am()
        while True:
            enemies = self.client.receive_data_EnemiesAm()
            print(enemies)
            enemies = int(enemies)
            diff = enemies - self.num_enemies
            self.num_enemies = enemies
            if diff > 0:
                for _ in range(diff):
                    enemy_thread = EnemyThread(self.client, self.player, self.setting, self.weapon, self.draw_event)
                    enemy_thread.start()
                    self.enemy_threads.append(enemy_thread)
            elif diff < 0:
                for _ in range(-diff):
                    # CHANGE!!!! LIDOR IDEA
                    thread = self.enemy_threads.pop()
                    thread.running = False
                    thread.join()

    def stop(self):
        self.running = False
        for thread in self.enemy_threads:
            thread.running = False
            thread.join()
        self.drawing_thread.join()  # Wait for the drawing thread to exit
        self.close_connections()
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    threading.Thread(target=game.EnemiesAm_handling).start()
    try:
        print("starting game.run")
        game.run()
    finally:
        game.stop()
