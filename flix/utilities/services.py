from typing import Iterable
import random

from flix.adapters.repository import AbstractRepository
from flix.domainmodel.movie import Movie
from flix.domainmodel.user import User


class UnknownUserException(Exception):
    pass


def get_genre_names(repo: AbstractRepository):
    genres = repo.get_genres()
    genre_names = [genre.genre for genre in genres]
    return genre_names


def get_random_movies(quantity, repo: AbstractRepository):
    movie_count = repo.get_number_of_movies()

    if quantity >= movie_count:
        # Reduce the quantity of ids to generate if the repository has an insufficient number of movies.
        quantity = movie_count - 1

    # Pick distinct and random movies.
    random_indices = random.sample(range(1, movie_count), quantity)

    random_movies = []
    for index in random_indices:
        random_movies.append(repo.get_movies()[index])

    return random_movies


def movie_to_dict(movie: Movie):
    movie_dict = {
        'title': movie.title,
        'release_year': movie.release_year,
        'description': movie.description
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]


def get_user(repo: AbstractRepository, username):
    user = repo.get_user(username)
    return user


def get_genre_recommendation(repo: AbstractRepository, num_of_recommendations: int, user):
    genre_movies = []
    genre_recommendations = []
    if len(user.watched_movies) > 0:
        genre = get_random_watched_movie(user)['genres'][0]
        for movie in repo.get_movies():
            if movie.genres[0] == genre:
                genre_movies.append(movie)
        for num in range(num_of_recommendations):
            genre_recommendations.append(genre_movies[random.randrange(len(genre_movies))])
    return genre_recommendations


def get_director_recommendation(repo: AbstractRepository, num_of_recommendations: int, user):
    director_movies = []
    director_recommendations = []
    if len(user.watched_movies) > 0:
        director = get_random_watched_movie(user)['director']
        for movie in repo.get_movies():
            if movie.director == director:
                director_movies.append(movie)
        for num in range(num_of_recommendations):
            director_recommendations.append(director_movies[random.randrange(len(director_movies))])
    return director_recommendations


def get_watch_it_again_recommendation(num_of_recommendations: int, user):
    movies = []
    if len(user.watched_movies) > 0:
        for num in range(num_of_recommendations):
            movies.append(dict_to_movie(get_random_watched_movie(user)))
    return movies


def get_random_watched_movie(user):
    random_watched_movie = user.watched_movies[random.randrange(len(user.watched_movies))]
    return random_watched_movie


def dict_to_movie(dict):
    movie = Movie(dict['title'], dict['release_year'])
    movie.description = dict['description']
    # Note there's no reviews or genres. This is sufficient for here.
    return movie
