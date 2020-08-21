import os
import signal
import threading
import time


lock = threading.Lock()


class CacheRefresher (threading.Thread):
    def __init__(self, name, interval, execute):
        threading.Thread.__init__(self)
        self.daemon = False
        self.name = name
        self.shutdown_flag = threading.Event()
        self.interval = interval
        self.execute = execute

    def run(self):
        print(f'{time.asctime()} - Starting {self.name} Thread')
        while not self.shutdown_flag.wait(self.interval.total_seconds()):
            with lock:
                self.execute()

    def stop(self):
        print(f'{time.asctime()} - Stopping {self.name} Thread')
        self.shutdown_flag.set()
        self.join()
