from collections import defaultdict

from .api import get_data

def movie_people():
    people = get_data("/people")
    movie_people = defaultdict(list)
    for person in people:
        for film in person.get("films"):
            film_id = film.split("/")[-1]
            movie_people[film_id].append(person.get("name"))
    return movie_people

def films():
    films = get_data("/films")
    people = movie_people()
    for film in films:
        film["people"] = people[film.get("id")]
    return films

