import queue
import threading
import time


class Check():
    def __init__(self):
        self.draw_q = queue.Queue()
        self.draw_event = threading.Event()
        self.lock = threading.Lock()
        self.data = "hello"
        self.thread_amount = 10

    def insert_to_q(self , index,):
        while True:
            self.draw_q.put(self.data)
            print(f"thread {index} q size: "+str(self.draw_q.qsize()))
            self.draw_event.wait()  # Wait for signal from main thread
            print(f"thread {index} finished waiting")
            self.draw_event.clear()  # Reset the event for the next iteration


    def main(self):
        while True:
            if self.thread_amount == self.draw_q.qsize():
                for _ in range(self.thread_amount):
                    print("Consuming item:", self.draw_q.get())
                self.draw_event.set()  # Signal to producer thread that items have been consumed

if __name__ == '__main__':
    checker = Check()
    num_threads = 10
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=checker.insert_to_q, args=(i,))
        t.daemon = True
        t.start()
        print(f"i - {i}")
        threads.append(t)
    checker.main()
