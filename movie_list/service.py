import ast
import json
import time
from collections import defaultdict

from .api import get_data
from .cache import client


def movie_people():
    people = get_data("/people")
    movie_people = defaultdict(list)
    if people is not None:
        for person in people:
            for film in person.get("films"):
                film_id = film.split("/")[-1]
                movie_people[film_id].append(person.get("name"))
        movie_people = dict(movie_people)
        client.set("movie-people", movie_people, expire=3600)
    return movie_people


def films():
    films = get_data("/films")
    if films is not None:
        people = client.get("movie-people")
        if people is None:
            people = movie_people()
        else:
            people = ast.literal_eval(people.decode("utf-8"))
        for film in films:
            film["people"] = people.get(film.get("id"), [])
        client.set("movies", films, expire=60)
    return films


def read_cache():
    return ast.literal_eval(client.get('movies').decode("utf-8"))


def refresh():
    films()
    print(time.asctime(), "Cache Refreshed")
