import threading
import time
from numpy import double


class my_class(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def say_hello(self):
        print("hello",time.time(),double("3.1456"))

    def run(self):
        while True:
            time.sleep(1)
            self.say_hello()