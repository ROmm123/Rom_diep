import threading



class EnemyThread(threading.Thread):
    def _init_(self, client):
        super().__init__()
        self.client = client


    def run(self):
        while True:
            print(self.client)



class Game():
    def _init_(self, client):
        super().__init__()
        self.client = client

    def run_game(self):
        enemy_thread = EnemyThread(self.client)
        enemy_thread.start()
        self.client = 3
        while True:
            print(self.client)


if __name__ == '__main__':
    game = Game(5)
    print("starting game.run")
    game.run_game()