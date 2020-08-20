import signal
import time

from datetime import timedelta
from http.server import HTTPServer

from .cache_refresher import CacheRefresher
from .server import Handler
from .service import films, refresh
from .service_exit import ServiceExit, service_shutdown

HOSTNAME = '0.0.0.0'
PORT_NUMBER = 8000
WAIT_TIME_SECONDS = 60


def run():
    print(f'{time.asctime()} - Starting Now ...')
    # Register the signal handlers
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)
    # Warm up cache here
    # Ensure that the distant api is up and running
    cached_films = films()
    if cached_films is not None:
        print(f'{time.asctime()} - Cache Warmup Succeeded')
        # Create new thread
        refresher_thread = CacheRefresher(
            "CacheRefresher", timedelta(seconds=WAIT_TIME_SECONDS),
            refresh)
        # Start new Thread
        refresher_thread.start()
        while refresher_thread.is_alive():
            try:
                refresher_thread.join(1)
                # Start web server
                httpd = HTTPServer((HOSTNAME, PORT_NUMBER), Handler)
                message = (
                    f'{time.asctime()} - Server Starts - '
                    f'{HOSTNAME}:{PORT_NUMBER}'
                )
                print(message)
                httpd.serve_forever()
            except ServiceExit:
                # Terminate the thread.
                refresher_thread.stop()
                httpd.server_close()
                message = (
                    f'{time.asctime()} - Server Stops - '
                    f'{HOSTNAME}:{PORT_NUMBER}'
                )
                print(message)
    else:
        print(f'{time.asctime()} - Cache Warmup Failed')
        print(f'{time.asctime()} - Exiting Now ...')
