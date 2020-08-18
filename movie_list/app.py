import signal
import time

from timeloop import Timeloop
from datetime import timedelta
from http.server import HTTPServer

from .cache_refresher import CacheRefresher
from .server import Handler
from .service import cache_films
from .service_exit import ServiceExit, service_shutdown

HOSTNAME = '0.0.0.0'
PORT_NUMBER = 8000


def run():
    print(time.asctime(), "Starting Now ...")
    # Register the signal handlers
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)
    # Warm up cache here
    # Ensure that the distant api is up and running
    cached_films = cache_films()
    if cached_films is not None:
        print(time.asctime(), "Cache Warmup Succeeded")
        # Create new thread
        refresher_thread = CacheRefresher("CacheRefresherThread")
        # Start new Thread
        refresher_thread.start()
        while refresher_thread.is_alive():
            try:
                refresher_thread.join(1)
                # Start server
                httpd = HTTPServer((HOSTNAME, PORT_NUMBER), Handler)
                print(time.asctime(), "Server Starts - %s:%s" % (HOSTNAME,
                      PORT_NUMBER))
                httpd.serve_forever()
            except ServiceExit:
                # Terminate the thread.
                # Set the shutdown flag on thread to trigger a clean shutdown.
                refresher_thread.shutdown_flag.set()
                refresher_thread.join()
                httpd.server_close()
                print(time.asctime(), "Server Stops - %s:%s" % (HOSTNAME,
                      PORT_NUMBER))
    else:
        print(time.asctime(), "Cache Warmup Failed")
        print(time.asctime(), "Exiting Now ...")
