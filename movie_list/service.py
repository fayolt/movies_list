from collections import defaultdict

from .api import get_data
from .cache import Cache


def movie_people():
    people = get_data("/people")
    movie_people = defaultdict(list)
    if people is not None:
        for person in people:
            for film in person.get("films"):
                film_id = film.split("/")[-1]
                movie_people[film_id].append(person.get("name"))
    return movie_people


def films():
    films = get_data("/films")
    if films is not None:
        people = movie_people()
        for film in films:
            film["people"] = people[film.get("id")]
    return films


def read_cache():
    return Cache.get_instance().get_cache()


# Set cache here
def cache_films():
    cached_films = films()
    if cached_films is not None:
        cache = Cache.get_instance()
        cache.set_cache(cached_films)
    return cached_films

# def cached_films():
#     cached_films = read_cache(films)
#     return cached_films
