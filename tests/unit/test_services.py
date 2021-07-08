import pytest

from flix.authentication.services import AuthenticationException
from flix.movies import services as movies_services
from flix.authentication import services as auth_services
from flix.movies.services import NonExistentMovieException
from flix.domainmodel.review import Review
from flix.domainmodel.user import User
from flix.domainmodel.actor import Actor
from flix.domainmodel.genre import Genre
from flix.domainmodel.director import Director


def test_can_add_user(in_memory_repo):
    new_username = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    assert user_as_dict['username'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    username = 'thorke'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(username, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_username, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_username, '0987654321', in_memory_repo)


def test_can_add_review(in_memory_repo):
    movie_id = 1
    movie = in_memory_repo.get_movie_by_id(1)
    review_text = "Hi this is my review"
    rating = 9
    username = "Jonny Depp"
    password = "pirate"
    user = User(username, password)
    in_memory_repo.add_user(user)
    movies_services.add_review(movie_id, review_text, rating, username, in_memory_repo)
    assert Review(username, movie, review_text, rating) in movie.reviews


def test_cannot_add_review_for_non_existent_movie(in_memory_repo):
    movie_id = 12
    review_text = "Hi this is my review"
    rating = 9
    username = "Jonny Depp"
    password = "pirate"
    user = User(username, password)
    in_memory_repo.add_user(user)
    with pytest.raises(movies_services.NonExistentMovieException):
        movies_services.add_review(movie_id, review_text, rating, username, in_memory_repo)


def test_cannot_add_review_by_unknown_user(in_memory_repo):
    movie_id = 2
    review_text = "Hi this is my review"
    rating = 9
    username = 'gmichael'
    with pytest.raises(movies_services.UnknownUserException):
        movies_services.add_review(movie_id, review_text, rating, username, in_memory_repo)


def test_can_get_movie(in_memory_repo):
    movie_id = 1
    movie_as_dict = movies_services.get_movie(movie_id, in_memory_repo)

    assert movie_id == movie_as_dict['id']
    assert movie_as_dict['title'] == "Guardians of the Galaxy"
    assert movie_as_dict[
               'description'] == 'A group of intergalactic criminals are forced to work together to stop a fanatical ' \
                                 'warrior from taking control of the universe. '
    assert movie_as_dict['director'] == Director("James Gunn")
    actors = movie_as_dict['actors']
    assert Actor("Chris Pratt") in actors
    assert Actor("Vin Diesel") in actors
    genres = movie_as_dict['genres']
    assert Genre('Action') in genres
    assert Genre('Adventure') in genres
    assert movie_as_dict['release_year'] == 2014
    assert movie_as_dict["runtime_minutes"] == 121
    assert movie_as_dict["rating"] == 8.1
    assert movie_as_dict["votes"] == 757074
    assert movie_as_dict["revenue"] == 333.13
    assert movie_as_dict["metascore"] == 76


def test_cannot_get_movie_with_non_existent_id(in_memory_repo):
    movie_id = 12
    with pytest.raises(movies_services.NonExistentMovieException):
        movies_services.get_movie(movie_id, in_memory_repo)


def test_get_first_movie(in_memory_repo):
    movie_as_dict = movies_services.get_first_movie(in_memory_repo)
    # is in alphabetical order, id 1 just happens to be first
    assert movie_as_dict['id'] == 1


def test_get_last_movie(in_memory_repo):
    movie_as_dict = movies_services.get_last_movie(in_memory_repo)
    # last movie in alphabetical is The lost city of Z, id = 9
    assert movie_as_dict['id'] == 9


def test_get_movies_by_title_with_no_prev(in_memory_repo):
    title = "Guardians of the Galaxy"
    movies_dto, prev_title, next_title = movies_services.get_movies_by_title(title, in_memory_repo)
    assert prev_title == None
    assert next_title == "La La Land"
    assert len(movies_dto) == 1
    assert movies_dto[0]['id'] == 1


def test_get_movies_by_title_with_prev(in_memory_repo):
    title = "Prometheus"
    movies_dto, prev_title, next_title = movies_services.get_movies_by_title(title, in_memory_repo)
    # prev in alphabetical is passengers, after is sing
    assert prev_title == "Passengers"
    assert next_title == "Sing"
    assert len(movies_dto) == 1
    assert movies_dto[0]['id'] == 2


def test_get_movies_by_title_with_no_next(in_memory_repo):
    title = "The Lost City of Z"
    movies_dto, prev_title, next_title = movies_services.get_movies_by_title(title, in_memory_repo)
    # prev in alphabetical is The great wall, after is nothing
    assert prev_title == "The Great Wall"
    assert next_title == None
    assert len(movies_dto) == 1
    assert movies_dto[0]['id'] == 9


def test_get_movies_by_title_with_invalid_title(in_memory_repo):
    title = "this is invalid"
    movies_dto, prev_title, next_title = movies_services.get_movies_by_title(title, in_memory_repo)
    assert len(movies_dto) == 0


def test_get_movies_by_id(in_memory_repo):
    movie_ids = [1, 2, 3]
    movie_dict_list = movies_services.get_movies_by_id(movie_ids, in_memory_repo)
    assert len(movie_dict_list) == 3
    returned_ids = [movie['id'] for movie in movie_dict_list]
    assert set([1, 2]).issubset(returned_ids)


def test_get_reviews_for_movie(in_memory_repo):
    movie_id = 1
    movie = in_memory_repo.get_movie_by_id(1)
    review_text = "Hi this is my review"
    rating = 9
    username = "Jonny Depp"
    password = "pirate"
    user = User(username, password)
    in_memory_repo.add_user(user)
    movies_services.add_review(movie_id, review_text, rating, username, in_memory_repo)
    review_dict_list = movies_services.get_reviews_for_movie(movie_id, in_memory_repo)
    assert len(review_dict_list) == 1
    assert review_dict_list[0]["movie"] == movie


def test_get_reviews_for_non_existent_movie(in_memory_repo):
    with pytest.raises(NonExistentMovieException):
        movies_as_dict = movies_services.get_reviews_for_movie(12, in_memory_repo)


def test_get_reviews_for_movie_without_reviews(in_memory_repo):
    movies_as_dict = movies_services.get_reviews_for_movie(2, in_memory_repo)
    assert len(movies_as_dict) == 0
