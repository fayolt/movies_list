import os
import signal
import threading
import time

from .service import cache_films


lock = threading.Lock()
WAIT_TIME_SECONDS = 60


class CacheRefresher (threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.counter = 0
        self.shutdown_flag = threading.Event()

    def run(self):
        print(time.asctime(), "Starting %s" % (self.name))
        while not self.shutdown_flag.is_set():
            # Get lock to synchronize threads
            lock.acquire()
            # Update cache here
            refresh()
            # Free lock to release next thread
            lock.release()
        print(time.asctime(), "Stopping %s" % (self.name))


def refresh():
    cache_films()
    print(time.asctime(), "Cache Refreshed")
    time.sleep(WAIT_TIME_SECONDS)
