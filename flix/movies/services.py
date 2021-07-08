from typing import List, Iterable

from flix.adapters.repository import AbstractRepository
from flix.domainmodel.movie import Movie
from flix.domainmodel.review import Review
from flix.domainmodel.genre import Genre


class NonExistentMovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(movie_id: int, review_text: str, rating: int, username: str, repo: AbstractRepository):
    # Check that the movie exists.
    movie = repo.get_movie_by_id(movie_id)
    if movie is None:
        raise NonExistentMovieException

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    # Create review.
    review = Review(username, movie, review_text, rating)

    # Update the repository.
    user.add_review(review)


def get_movie(movie_id: int, repo: AbstractRepository):
    movie = repo.get_movie_by_id(movie_id)

    if movie is None:
        raise NonExistentMovieException

    return movie_to_dict(movie)


def get_first_movie(repo: AbstractRepository):
    movie = repo.get_first_movie()
    return movie_to_dict(movie)


def get_last_movie(repo: AbstractRepository):
    movie = repo.get_last_movie()
    return movie_to_dict(movie)


def get_movies_by_exact_title(title: str, repo: AbstractRepository):
    movies = repo.get_movies_by_exact_title(title)
    movies_dto = list()
    prev_title = None
    next_title = None
    if len(movies) > 0:
        prev_title = repo.get_title_of_previous_movie(movies[0])
        next_title = repo.get_title_of_next_movie(movies[0])
        movies_dto = movies_to_dict(movies)
    return movies_dto, prev_title, next_title


def get_movies_by_title(title: str, repo: AbstractRepository):
    movies = repo.get_movies_by_title(title)
    movies_dto = list()
    prev_title = None
    next_title = None
    if len(movies) > 0:
        prev_title = repo.get_title_of_previous_movie(movies[0])
        next_title = repo.get_title_of_next_movie(movies[0])
        movies_dto = movies_to_dict(movies)
    return movies_dto, prev_title, next_title


def get_movies_by_director(director: str, repo: AbstractRepository):
    movies = repo.get_movies_by_director(director)
    if len(movies) > 0:
        movies = movies_to_dict(movies)
    return movies


def get_movies_by_genre(genre: str, repo: AbstractRepository):
    movies = repo.get_movies_by_genre(genre)
    if len(movies) > 0:
        movies = movies_to_dict(movies)
    return movies


def get_movies_by_actor(actor: str, repo: AbstractRepository):
    movies = repo.get_movies_by_actor(actor)
    if len(movies) > 0:
        movies = movies_to_dict(movies)
    return movies


def get_movie_ids_for_genre(genre: Genre, repo: AbstractRepository):
    movie_ids = repo.get_movie_ids_for_genre(genre)
    return movie_ids


def get_movies_by_id(id_list, repo: AbstractRepository):
    movies = repo.get_movies_by_id(id_list)

    # Convert Movies to dictionary form.
    movies_as_dict = movies_to_dict(movies)

    return movies_as_dict


def get_reviews_for_movie(movie_id, repo: AbstractRepository):
    movie = repo.get_movie_by_id(movie_id)

    if movie is None:
        raise NonExistentMovieException

    return reviews_to_dict(movie.reviews)


# Functions to convert model entities to dicts

def review_to_dict(review: Review):
    review_dict = {
        'username': review.username,
        'movie': review.movie,
        'review_text': review.review_text,
        'rating': review.rating,
        'timestamp': review.timestamp
    }
    return review_dict


def reviews_to_dict(reviews: list):
    return [review_to_dict(review) for review in reviews]


def movie_to_dict(movie: Movie):
    movie_dict = {
        'id': movie.id,
        'title': movie.title,
        'release_year': movie.release_year,
        'description': movie.description,
        'director': movie.director,
        'actors': movie.actors,
        'genres': movie.genres,
        'runtime_minutes': movie.runtime_minutes,
        'rating': movie.rating,
        'votes': movie.votes,
        'revenue': movie.revenue,
        'metascore': movie.metascore,
        'reviews': movie.reviews
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]


def genre_to_dict(genre: Genre):
    genre_dict = {
        'name': genre.genre,
    }
    return genre_dict


def genres_to_dict(genres: Iterable[Genre]):
    return [genre_to_dict(genre) for genre in genres]


def get_user(repo: AbstractRepository, username=None):
    user = None
    try:
        user = repo.get_user(username)
    except:
        pass
    return user

