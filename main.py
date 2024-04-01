import json
import socket
import threading
import time

import pygame
from player import Player
from map import Map
from settings import setting
from weapon import Weapon
from Network import Client
from enemy_main import *


class EnemyThread(threading.Thread):
    def __init__(self, client, player, setting, weapon):
        super().__init__()
        self.client = client
        self.player = player
        self.setting = setting
        self.weapon = weapon
        self.running = True

    def run(self):
        print("in draw thread")

        while self.running:
            data = self.client.receive_data()
            print(data)

            if data != '0' and data:
                enemy_mainn = enemy_main(data, self.player, self.setting, self.weapon)
                enemy_mainn.main()




class Game():
    def __init__(self):
        pygame.init()
        self.setting = setting()
        self.player = Player(0, 0, 45, self.setting.red, self.setting)
        self.map = Map(self.player, self.setting)
        self.weapon = Weapon(20, 20, self.setting.green_fn, self.player.radius, self.setting, self.player.center_x,
                             self.player.center_y, self.player.angle)
        self.client = Client('localhost', 10022, 10020)
        self.num_enemies = 0
        self.enemy_threads = []
        self.running = True

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

            #data = f";{self.weapon.rect_center_x};{self.weapon.rect_center_y};{self.weapon.rect_width};{self.weapon.rect_height};{self.weapon.tangent_x};{self.player.screen_position[0]};{self.player.screen_position[1]};{self.player.color};{self.player.radius};{self.weapon.rect_center_x};{self.weapon.rect_center_y};{self.weapon.rect_width};{self.weapon.rect_height};{self.weapon.angle}"
            #self.client.send_data(data)

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
                    enemy_thread = EnemyThread(self.client, self.player, self.setting, self.weapon)
                    enemy_thread.start()
                    self.enemy_threads.append(enemy_thread)
            elif diff < 0:
                for _ in range(-diff):
                    if self.enemy_threads:
                        thread = self.enemy_threads.pop()
                        thread.running = False
                        thread.join()

    def stop(self):
        self.running = False
        for thread in self.enemy_threads:
            thread.running = False
            thread.join()


if __name__ == '__main__':
    game = Game()

    threading.Thread(target=game.EnemiesAm_handling).start()
    time.sleep(0.2)

    try:
        print("starting game.run")
        game.run()
    finally:
        game.stop()
        game.close_connections()
        pygame.quit()
