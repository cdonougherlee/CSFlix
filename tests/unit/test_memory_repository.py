import pytest

from flix.domainmodel.movie import Movie
from flix.domainmodel.actor import Actor
from flix.domainmodel.genre import Genre
from flix.domainmodel.director import Director
from flix.domainmodel.user import User
from bisect import bisect, bisect_left, insort_left

from flix.adapters.repository import RepositoryException


def test_repository_can_add_a_user(in_memory_repo):
    user = User('Dave', '123456789')
    in_memory_repo.add_user(user)
    assert in_memory_repo.get_user('Dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_movie_count(in_memory_repo):
    number_of_movies = in_memory_repo.get_number_of_movies()
    assert number_of_movies == 10


def test_repository_can_add_movie(in_memory_repo):
    movie = Movie("Fast and furious", 2001)
    movie.id = 11
    in_memory_repo.add_movie(movie)
    assert in_memory_repo.get_movie_by_id(11) is movie


def test_repository_can_retrieve_movie(in_memory_repo):
    movie = in_memory_repo.get_movie_by_id(1)
    assert movie.title == "Guardians of the Galaxy"
    assert movie.genres == [Genre("Action"), Genre("Adventure"), Genre("Sci-Fi")]
    assert movie.description == "A group of intergalactic criminals are forced to work together to stop a fanatical " \
                                "warrior from taking control of the universe. "
    assert movie.director == Director("James Gunn")
    assert movie.actors == [Actor("Chris Pratt"), Actor("Vin Diesel"), Actor("Bradley Cooper"), Actor("Zoe Saldana")]
    assert movie.release_year == 2014
    assert movie.runtime_minutes == 121
    assert movie.rating == 8.1
    assert movie.votes == 757074
    assert movie.revenue == 333.13
    assert movie.metascore == 76
    assert movie.reviews == []


def test_repository_does_not_retrieve_a_non_existent_movie(in_memory_repo):
    article = in_memory_repo.get_movie_by_id(101)
    assert article is None


def test_repository_can_retrieve_genres(in_memory_repo):
    assert in_memory_repo.get_genres() == {Genre("Fantasy"), Genre("Horror"), Genre("Mystery"), Genre("Action"),
                                           Genre("Drama"), Genre("Comedy"), Genre("Music"), Genre("Sci-Fi"),
                                           Genre("Animation"), Genre("Family"), Genre("Biography"), Genre("Adventure"),
                                           Genre("Romance"), Genre("Thriller")}
    assert len(in_memory_repo.get_genres()) == 14


def test_repository_can_get_first_movie(in_memory_repo):
    # note its from movies dataset, so first movie in alphabetical order
    assert in_memory_repo.get_first_movie().title == "Guardians of the Galaxy"


def test_repository_can_get_last_movie(in_memory_repo):
    # note its from movies dataset, so last movie in alphabetical order
    assert in_memory_repo.get_last_movie().title == "The Lost City of Z"


def test_repository_can_get_movies_by_ids(in_memory_repo):
    articles = in_memory_repo.get_movies_by_id([1, 5, 10])
    assert articles[0] == Movie("Guardians of the Galaxy", 2014)
    assert articles[1] == Movie("Suicide Squad", 2016)
    assert articles[2] == Movie("Passengers", 2016)


def test_repository_does_not_retrieve_movie_for_non_existent_id(in_memory_repo):
    articles = in_memory_repo.get_movies_by_id([2, 12])
    assert len(articles) == 1
    assert articles[0].title == "Prometheus"


def test_repository_returns_an_empty_list_for_non_existent_ids(in_memory_repo):
    articles = in_memory_repo.get_movies_by_id([0, 122])
    assert len(articles) == 0


def test_repository_can_add_a_genre(in_memory_repo):
    genre = Genre("Racing")
    in_memory_repo.add_genre(genre)
    assert genre in in_memory_repo.get_genres()


def test_repository_can_add_an_actor(in_memory_repo):
    actor = Actor("Dylan Yates")
    in_memory_repo.add_actor(actor)
    assert actor in in_memory_repo.get_actors()


def test_repository_can_add_a_director(in_memory_repo):
    director = Director("Toyota Curren")
    in_memory_repo.add_director(director)
    assert director in in_memory_repo.get_directors()


def test_repository_returns_title_of_previous_movie(in_memory_repo):
    movie = in_memory_repo.get_movies_by_title("Sing")
    previous_title = in_memory_repo.get_title_of_previous_movie(movie[0])
    assert previous_title == "Prometheus"


def test_repository_returns_title_of_next_movie(in_memory_repo):
    movie = in_memory_repo.get_movies_by_title("Sing")
    next_title = in_memory_repo.get_title_of_next_movie(movie[0])
    assert next_title == "Split"


def test_repository_returns_none_when_there_are_no_previous_movies(in_memory_repo):
    movie = in_memory_repo.get_movies()[0]
    previous_movie = in_memory_repo.get_title_of_previous_movie(movie)
    assert previous_movie == None


def test_repository_returns_none_when_there_are_no_next_movies(in_memory_repo):
    movie = in_memory_repo.get_movies()[9]
    next_movie = in_memory_repo.get_title_of_next_movie(movie)
    assert next_movie == None


def test_get_movie_ids_for_genre(in_memory_repo):
    genre = Genre("Action")
    id_list = in_memory_repo.get_movie_ids_for_genre(genre)
    assert len(id_list) == 4
    genre2 = Genre("Racing")  # invalid genre
    id_list2 = in_memory_repo.get_movie_ids_for_genre(genre2)
    assert len(id_list2) == 0
