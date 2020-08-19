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
        print(time.asctime(), "Starting %s" % (self.name))
        while not self.shutdown_flag.wait(self.interval.total_seconds()):
            # Get lock to synchronize threads
            lock.acquire()
            # Update cache here
            self.execute()
            # Free lock to release next thread
            lock.release()

    def stop(self):
        print(time.asctime(), "Stopping %s" % (self.name))
        self.shutdown_flag.set()
        self.join()
