
from enemy_calculate import *

class Enemy_main():

    def __init__(self,dataa,player,setting,weapon):
        self.data = dataa
        self.Playerrr = player
        self.set = setting
        self.WEAPON = weapon

    def main(self):

        Enemy_calculate = enemy_calculate(self.data,self.set,self.Playerrr,self.WEAPON)
        Enemy_calculate.calculate()
        self.set.update()




