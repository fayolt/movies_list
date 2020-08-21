import logging
import os
import signal
import threading
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

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
        logger.info(f'Starting {self.name} Thread')
        while not self.shutdown_flag.wait(self.interval.total_seconds()):
            with lock:
                self.execute()

    def stop(self):
        logger.info(f'Stopping {self.name} Thread')
        self.shutdown_flag.set()
        self.join()
