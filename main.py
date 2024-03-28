import pygame
from player import Player
from map import Map
from settings import setting
from weapon import Weapon
from Network import Client
from server_oop import Server
from test_enemy import *
from enemy_main import *
from staticObjrcts import StaticObject

class Game():

    def __init__(self):
        pygame.init()
        self.setting = setting()
        self.static_object = StaticObjects(setting, map_width, map_height)
        self.Playerr = Player(0, 0, 35, self.setting.red, self.setting)
        self.MAP = Map(self.Playerr, self.setting)
        self.WEAPON = Weapon(20, 20, self.setting.green_fn, self.Playerr.radius, self.setting, self.Playerr.center_x,
                             self.Playerr.center_y, self.Playerr.angle)
        self.staticobj = StaticObject(300, 200, 20, self.setting.red, setting)

    def run(self):
        while True:
            self.staticobj.draw()
            self.Playerr.calc_angle()
            self.WEAPON = Weapon(20, 20, self.setting.green_fn, self.Playerr.radius, self.setting,
                                 self.Playerr.center_x, self.Playerr.center_y, self.Playerr.angle)
            self.Playerr.handle_events()
            self.Playerr.move()
            chunk = self.MAP.calc_chunk()
            self.MAP.draw_map(chunk)
            self.Playerr.draw()
            self.Playerr.IsAlive()
            self.WEAPON.run_weapon()
            # 0                          #1                          #2                      #3                      #4                          #5                                  #6                              #7                      #8                      #9                          #10                          #11                        #12                  #13
            self.client.send_data(
                f"{self.WEAPON.rect_center_x};{self.WEAPON.rect_center_y};{self.WEAPON.rect_width};{self.WEAPON.rect_height};{self.WEAPON.tangent_x};{self.Playerr.screen_position[0]};{self.Playerr.screen_position[1]};{self.Playerr.color};{self.Playerr.radius};{self.WEAPON.rect_center_x};{self.WEAPON.rect_center_y};{self.WEAPON.rect_width};{self.WEAPON.rect_height};{self.WEAPON.angle}")
            data = self.client.receive_data()

            Enemy_main = enemy_main(data, self.Playerr, self.setting, self.WEAPON)
            Enemy_main.main()

            self.setting.update()

    def connect_to_server(self):
        self.client = Client('localhost', 10026)

    def close_connections(self):
        self.client.close()
        self.server.close()


if __name__ == '__main__':
    game = Game()
    game.connect_to_server()
    game.run()
    game.close_connections()
    pygame.quit()
