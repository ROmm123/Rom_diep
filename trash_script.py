import socket
import threading
import pygame
from player import Player
from map import Map
from settings import setting
from weapon import Weapon
from Network import Client
from enemy_main import *


class EnemyThread(threading.Thread):
    def __init__(self, client, player, setting, weapon,data):
        super().__init__()
        self.client = client
        self.player = player
        self.setting = setting
        self.weapon = weapon
        self.running = True
        self.data = 0

    def run(self):
        while self.running:
            try:
                if self.data != '0' and self.data:
                    enemy_main = enemy_main(self.data, self.player, self.setting, self.weapon)
                    enemy_main.main()
            except Exception as e:

                print(f"Error in EnemyThread: {e}")


class Game():
    def __init__(self):
        pygame.init()
        self.setting = setting()
        self.player = Player(0, 0, 35, self.setting.red, self.setting)
        self.map = Map(self.player, self.setting)
        self.weapon = Weapon(20, 20, self.setting.green_fn, self.player.radius, self.setting, self.player.center_x,
                             self.player.center_y, self.player.angle)
        self.client = Client('localhost', 10023)
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
                        #0                           #1                          #4                     #5                          #6                      #7                              #8                              #9                      #10                 #11                         #12                         #13                     #14                         #15               #16
            data = f"{self.weapon.rect_center_x};{self.weapon.rect_center_y};{self.weapon.rect_width};{self.weapon.rect_height};{self.weapon.tangent_x};{self.player.screen_position[0]};{self.player.screen_position[1]};{self.player.color};{self.player.radius};{self.weapon.rect_center_x};{self.weapon.rect_center_y};{self.weapon.rect_width};{self.weapon.rect_height};{self.weapon.angle}"
            self.client.send_data(data)

            self.setting.update()

    def close_connections(self):
        self.client.close()

    def start_enemy_threads(self):
        while self.running:
            packet1 = self.client.receive_data()
            if packet1!="0":

                a=packet1.split('&')
                print(packet1)
                self.data=a[0]
                packet=a[1]
                self.num_enemies = int(packet)
                diff = self.num_enemies - len(self.enemy_threads)
                if diff > 0:
                    for _ in range(diff):
                        enemy_thread = EnemyThread(self.client, self.player, self.setting, self.weapon,self.data)
                        enemy_thread.start()
                        self.enemy_threads.append(enemy_thread)
                elif diff < 0:
                    for _ in range(-diff):
                        thread = self.enemy_threads.pop()
                        thread.running = False
                        thread.join()
                        '''
                except Exception as e:
                    print(f"Error in start_enemy_threads: {e}")
                    '''

    def stop(self):
        self.running = False
        for thread in self.enemy_threads:
            thread.running = False
            thread.join()


if __name__ == '__main__':
    game = Game()
    enemy_thread_handler = threading.Thread(target=game.start_enemy_threads)
    enemy_thread_handler.start()
    try:
        game.run()
    finally:
        game.stop()
        game.close_connections()
        pygame.quit()
