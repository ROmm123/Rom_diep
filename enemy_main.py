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

    def __init__(self,dataa,player,setting,weapon):
        self.data = dataa
        self.Playerrr = player
        self.set = setting
        self.WEAPON = weapon

    def main(self):
        if self.data =='0':
            pass
        else:
            Enemy_player = enemy_player(self.data,self.set,self.Playerrr,self.WEAPON)
            Enemy_player.calculate()

