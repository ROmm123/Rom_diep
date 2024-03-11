import pygame
import threading

import main
from player import Player
from map import Map
from weapon import Weapon
from Network import Client
from server_oop import Server
from enemy_player import *

class enemy_main():

    def __int__(self,dataa,player):
        self.data = dataa
        self.Playerrr = player

    def main(self):
        if self.data =='0':
            pass
        else:
            print ("join ")
            print(self.data)
            #enemy_player = enemy_player
           # enemy_player.calculate(self)

