import random
class RandomDead():
    def __init__(self, i):
        self.num_server = i

    def pos_after_dead(self):

        if (self.num_server == 1):
            position = [random.randint(0, 240 * 64 - 430)  # Random x-coordinate
                , random.randint(0, 177 * 64 - 330)]  # Random y-coordinate
        elif (self.num_server == 2):
            position = [random.randint (261 * 64 - 430 , 30784)  # Random x-coordinate
                , random.randint(0, 177 * 64 - 330)]  # Random y-coordinate
        elif (self.num_server == 3):
            position = [random.randint(0, 240 * 64 - 430)  # Random x-coordinate
                , random.randint(198 * 64 - 330, 22724)]  # Random y-coordinate
        else:
            position = [random.randint(261 * 64 - 430 , 30784)  # Random x-coordinate
                , random.randint(198 * 64 - 330, 22724)]  # Random y-coordinate

        return position
