from flix.adapters.repository import AbstractRepository
from flix.domainmodel.movie import Movie
from typing import Iterable


def check_if_title_valid(title: str, repo: AbstractRepository):
    movies = repo.get_movies_by_title(title)
    if len(movies) > 0:
        return True
    else:
        return False


def check_if_director_valid(director_name: str, repo: AbstractRepository):
    movies = repo.get_movies_by_director(director_name)
    if len(movies) > 0:
        return True
    else:
        return False


def check_if_genre_valid(genre_name: str, repo: AbstractRepository):
    movies = repo.get_movies_by_genre(genre_name)
    if len(movies) > 0:
        return True
    else:
        return False


def check_if_actor_valid(actor_name: str, repo: AbstractRepository):
    movies = repo.get_movies_by_actor(actor_name)
    if len(movies) > 0:
        return True
    else:
        return False


class SearchInvalid(Exception):
    pass
