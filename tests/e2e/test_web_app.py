import pytest

from flask import session


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid username and password.
    response = client.post(
        '/authentication/register',
        data={'username': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Your username is required'),
        ('cj', '', b'Your username is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter, '
                         b'a lower case letter and a digit'),
        ('fmercury', 'Test#6^0', b'Your username is already taken - please supply another'),
))
def test_register_with_invalid_input(client, username, password, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['username'] == 'thorke'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'CSFlix' in response.data


def test_login_required_to_review(client):
    response = client.post('/review')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_review(client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the review page.
    response = client.get('/review?movie=2')

    response = client.post(
        '/review', data={'review': 'This moves bad', 'rating': 5, 'movie_id': 2}
    )
    assert response.headers['Location'] == 'http://localhost/movies_by_title?title=Prometheus&view_reviews_for=2'


@pytest.mark.parametrize(('review', 'messages'), (
        ('Who thinks tom cruise is a fuckwit?', (b'Your review must not contain profanity')),
        ('Hey', b'Your review is too short'),
        ('ass', (b'Your review is too short', b'Your review must not contain profanity')),
))
def test_review_with_invalid_input(client, auth, review, messages):
    # Login a user.
    auth.login()

    # Attempt to review on a movie.
    response = client.post(
        '/review',
        data={'review': review, 'movie_id': 2}
    )
    # Check that supplying invalid review text generates appropriate error messages.
    for message in messages:
        assert message in response.data


def test_movies_without_title(client):
    # Check that we can retrieve the movies page.
    response = client.get('/movies_by_title')
    assert response.status_code == 200

    # Check that without providing a title query parameter the page includes the first movie.
    assert b'Guardians of the Galaxy' in response.data
    assert b'A group of intergalactic criminals' in response.data


def test_movies_with_title(client):
    # Check that we can retrieve the movies page.
    response = client.get('/movies_by_title?title=prometheus')
    assert response.status_code == 200

    # Check that all movies on the requested title are included on the page.
    assert b'Prometheus' in response.data
    assert b'Following clues to the origin of mankind' in response.data


def test_movies_with_genre(client):
    # Check that we can retrieve the movies page.
    response = client.get('/movies_by_genre?genre=Action')
    assert response.status_code == 200

    # Check that all movies tagged with genre 'Action' are included on the page.
    assert b'Movies of genre Action' in response.data
    assert b'Guardians of the Galaxy' in response.data


def test_stats_page_logged_in(client, auth):
    auth.login()
    response = client.get("/display_stats")
    assert response.status_code == 200
    assert b'Reviews made:' in response.data


def test_stats_page_not_logged_in(client):
    response = client.get("/display_stats")
    assert response.headers['Location'] == 'http://localhost/authentication/login'
