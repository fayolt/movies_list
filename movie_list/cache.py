# cache data structure
# function to warm up the cache
# function to read cache
# function to set cache

class Cache:
    __instance = None

    def __init__(self):
        self.__cache = None
        if Cache.__instance is None:
            Cache.__instance = self
        else:
            raise Exception("Only one instance of Cache is allowed")

    @staticmethod
    def get_instance():
        """ Static method to fetch the current instance.
        """
        if not Cache.__instance:
            Cache()
        return Cache.__instance

    def get_cache(self):
        return self.__cache

    def set_cache(self, cache):
        self.__cache = cache

    def read_cache(self, func):
        cache = self.get_cache()
        if cache is not None:
            print("read from cache")
            return cache
        print("read from server")
        cache = func()
        self.set_cache(cache)
        return cache


def read_cache(func):
    global cache
    if cache is not None:
        print("read from cache")
        return cache
    print("read from server")
    cache = func()
    return cache


def memoize(func):
    def memoized_func():
        global cache
        if cache is not None:
            print("read from cache")
            return cache
        print("read from server")
        cache = func()
        return cache
    return memoized_func
