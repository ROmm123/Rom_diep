import pygame
from player import Player
from map import Map
from settings import setting
from weapon import Weapon
from Network import Client
from server_oop import Server
from test_enemy import*
from enemy_main import *

class Game():

    def __init__(self):
        pygame.init()
        self.setting = setting()
        self.Playerr = Player(0, 0, 35, self.setting.red, self.setting)
        self.MAP = Map(self.Playerr, self.setting)
        self.WEAPON = Weapon(20 , 20 , self.setting.green_fn , self.Playerr , self.setting )

    def run(self):

        while True:
            self.Playerr.handle_events()
            self.Playerr.move()
            chunk = self.MAP.calc_chunk()
            self.MAP.draw_map(chunk)
            self.Playerr.draw()
            self.WEAPON.run_weapon()
            self.setting.update()
                                        #0                          #1                          #2                      #3                      #4                          #5                                  #6                              #7                      #8                      #9                          #10
            self.client.send_data(f"{self.WEAPON.rect_center_x};{self.WEAPON.rect_center_y};{self.WEAPON.rect_width};{self.WEAPON.rect_height};{self.WEAPON.tangent_x};{self.Playerr.screen_position[0]};{self.Playerr.screen_position[1]};{self.Playerr.color};{self.Playerr.radius}")
            data = self.client.receive_data()
            Enemy_main = enemy_main(data,self.Playerr)
            Enemy_main.main()




    def connect_to_server(self):
        self.client = Client('localhost', 10022)

    def close_connections(self):
        self.client.close()
        self.server.close()

if __name__ == '__main__':
    game = Game()
    game.connect_to_server()
    game.run()
    game.close_connections()
    pygame.quit()
