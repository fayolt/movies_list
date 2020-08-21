import logging
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

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


def run():
    logger.info('Starting Now ...')
    # Register the signal handlers
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)
    # Warm up cache here
    # Ensure that the distant api is up and running
    cached_films = films()
    if cached_films is not None:
        logger.info('Cache Warmup Succeeded')
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
                logger.info(f'Server Starting {HOSTNAME}:{PORT_NUMBER}')
                httpd.serve_forever()
            except ServiceExit:
                # Terminate the thread.
                refresher_thread.stop()
                httpd.server_close()
                logger.info(f'Server Stopping {HOSTNAME}:{PORT_NUMBER}')
    else:
        logger.critical('Cache Warmup Failed')
        logger.critical('Exiting Now ...')
