import ast
import json
import time
import requests


from collections import defaultdict

from .cache import client

BASE_URL = 'https://ghibliapi.herokuapp.com'


def get_data(path):
    try:
        response = requests.get(BASE_URL + path,  timeout=5)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return None
    except requests.exceptions.Timeout as timeout_err:
        print(f'Timeout error occurred: {timeout_err}')
        return None
    else:
        return response.json()


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
        client.set("movies", films)
    return films


def refresh():
    films()
    print(f'{time.asctime()} - Cache Refreshed')


def read_cache():
    return ast.literal_eval(client.get('movies').decode("utf-8"))
