import time


class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass


def service_shutdown(signum, frame):
    print(f'{time.asctime()} - Caught signal {signum}')
    raise ServiceExit
