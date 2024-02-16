from threading import Thread
from time import sleep


class LoadThread(Thread):

    def run(self):
        print("Started Thread")
        sleep(3)
        print("Done with Thread")
