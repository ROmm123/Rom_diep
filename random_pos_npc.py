import random


class Npc_pos():
    def __init__(self, which_server):

        if (which_server == 1):
            self.position = [random.randint(0, 240 * 64 - 430)  # Random x-coordinate
                , random.randint(0, 177 * 64 - 330)]  # Random y-coordinate
        elif (which_server == 2):
            self.position = [random.randint (261 * 64 - 430 , 30784)  # Random x-coordinate
                , random.randint(0, 177 * 64 - 330)]  # Random y-coordinate
        elif (which_server == 3):
            self.position = [random.randint(0, 240 * 64 - 430)  # Random x-coordinate
                , random.randint(198 * 64 - 330, 22724)]  # Random y-coordinate
        elif (which_server == 4):
            self.position = [random.randint(261 * 64 - 430 , 30784)  # Random x-coordinate
                , random.randint(198 * 64 - 330, 22724)]  # Random y-coordinate


class Random_Position_npc():

    def __init__(self):
            # self.surface = setting.surface
        self.npc_position = []  # the static object list
        for _ in range(25):
           pos = Npc_pos(1)
           self.npc_position.append(pos)

        for _ in range(25):
            pos = Npc_pos(2)
            self.npc_position.append(pos)

        for _ in range(25):
            pos = Npc_pos(3)
            self.npc_position.append(pos)

        for _ in range(25):
            pos = Npc_pos(4)
            self.npc_position.append(pos)


    def crate_position_dst_data(self):
        locations = {}
        i = 0
        for pos in self.npc_position:
            locations.update({'pos_' + str(i): pos.position})
            i = i +1
        return locations