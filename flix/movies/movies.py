from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, IntegerField
from wtforms import validators

import flix.adapters.repository as repo
import flix.utilities.utilities as utilities
import flix.movies.services as services

from flix.domainmodel.genre import Genre

from flix.authentication.authentication import login_required

# Configure Blueprint.
movies_blueprint = Blueprint('movies_bp', __name__)


@movies_blueprint.route('/movies_by_search', methods=["GET"])
def movies_by_search():
    username = None
    try:
        username = session['username']
    except:
        pass
    recommendations = utilities.get_recommendations(username)

    search_query = request.args.get('search_query')
    search_type = request.args.get('search_type')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent movie id.
        movie_to_show_reviews = -1
    else:
        # Convert movie_to_show_reviews from string to int.
        movie_to_show_reviews = int(movie_to_show_reviews)
    movies = []

    if search_type == "title":
        # movies = list of dicts
        movies, previous_title, next_title = services.get_movies_by_title(search_query, repo.repo_instance)
    elif search_type == "director":
        movies = services.get_movies_by_director(search_query, repo.repo_instance)
    elif search_type == "actor":
        movies = services.get_movies_by_actor(search_query, repo.repo_instance)
    for movie in movies:
        movie['display_movie_url'] = url_for('movies_bp.display_movie', movie=movie['id'])

    return render_template("movies/search_results.html",
                           search_query=search_query,
                           search_type=search_type,
                           movies=movies,
                           selected_movies=utilities.get_selected_movies(len(movies) + 2),
                           recommendations=recommendations,
                           genre_urls=utilities.get_genres_and_urls(),

                           )


@movies_blueprint.route('/movies_by_title', methods=['GET'])
def movies_by_title():
    username = None
    try:
        username = session['username']
    except:
        pass
    recommendations = utilities.get_recommendations(username)

    # Read query parameters.
    target_title = request.args.get('title')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    # Fetch the first and last movies in the series.
    first_movie = services.get_first_movie(repo.repo_instance)
    last_movie = services.get_last_movie(repo.repo_instance)

    if target_title is None:
        # No title query parameter, so return first movie of the series.
        target_title = first_movie['title']

    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent movie id.
        movie_to_show_reviews = -1
    else:
        # Convert movie_to_show_reviews from string to int.
        movie_to_show_reviews = int(movie_to_show_reviews)

    # Fetch movie(s) for the target title. This call also returns the previous and next titles for movies immediately
    # before and after the target title.
    movies, previous_title, next_title = services.get_movies_by_exact_title(target_title, repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if len(movies) > 0:
        # There's at least one movie for the target title.
        if previous_title is not None:
            # There are movies for previous title, so generate URLs for the 'previous' and 'first' navigation buttons.
            prev_movie_url = url_for('movies_bp.movies_by_title', title=previous_title)
            first_movie_url = url_for('movies_bp.movies_by_title', title=first_movie['title'])

        if next_title is not None:
            # There are movies for subsequent title, so generate URLs for the 'next' and 'last' navigation buttons.
            next_movie_url = url_for('movies_bp.movies_by_title', title=next_title)
            last_movie_url = url_for('movies_bp.movies_by_title', title=last_movie['title'])

        # Construct urls for viewing movie reviews and adding reviews.
        for movie in movies:
            movie['view_reviews_url'] = url_for('movies_bp.movies_by_title', title=target_title,
                                                view_reviews_for=movie['id'])
            movie['add_review_url'] = url_for('movies_bp.review_movie', movie=movie['id'])
            movie['display_movie_url'] = url_for('movies_bp.display_movie', movie=movie['id'])

        # Generate the webpage to display the movies.
        return render_template(
            'movies/movies.html',
            title='Movies',
            movies_title=target_title.title(),
            movies=movies,
            selected_movies=utilities.get_selected_movies(len(movies) + 2),
            genre_urls=utilities.get_genres_and_urls(),
            first_movie_url=first_movie_url,
            last_movie_url=last_movie_url,
            prev_movie_url=prev_movie_url,
            next_movie_url=next_movie_url,
            show_reviews_for_movie=movie_to_show_reviews,
            recommendations=recommendations
        )

    # No movies to show, so return the homepage.
    return redirect(url_for('home_bp.home'))


@movies_blueprint.route('/movies_by_genre', methods=['GET'])
def movies_by_genre():
    username = None
    try:
        username = session['username']
    except:
        pass
    recommendations = utilities.get_recommendations(username)

    movies_per_page = 3
    # Read query parameters.
    genre_name = request.args.get('genre')
    cursor = request.args.get('cursor')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent movie id.
        movie_to_show_reviews = -1
    else:
        # Convert movie_to_show_reviews from string to int.
        movie_to_show_reviews = int(movie_to_show_reviews)

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    # Retrieve movie ids for movies that are tagged with genre_name.
    movie_ids = services.get_movie_ids_for_genre(Genre(genre_name), repo.repo_instance)

    # Retrieve the batch of movies to display on the Web page.
    movies = services.get_movies_by_id(movie_ids[cursor:cursor + movies_per_page],
                                       repo.repo_instance)  # list of movies as dicts

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor - movies_per_page)
        first_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name)

    if cursor + movies_per_page < len(movie_ids):
        # There are further movies, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movie_ids) / movies_per_page)
        if len(movie_ids) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=last_cursor)

    # Construct urls for viewing movie reviews and adding reviews.
    for movie in movies:
        movie['view_reviews_url'] = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor,
                                            view_reviews_for=movie['id'])
        movie['add_review_url'] = url_for('movies_bp.review_movie', movie=movie['id'])
        movie['display_movie_url'] = url_for('movies_bp.display_movie', movie=movie['id'])

    # Generate the webpage to display the movies.
    return render_template(
        'movies/movies.html',
        title='Movies',
        movies_title='Movies of genre ' + genre_name,
        movies=movies,
        selected_movies=utilities.get_selected_movies(len(movies) * 2),
        genre_urls=utilities.get_genres_and_urls(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        show_reviews_for_movie=movie_to_show_reviews,
        recommendations=recommendations
    )


@movies_blueprint.route('/display_movie', methods=['GET'])
def display_movie():
    username = None
    try:
        username = session['username']
    except:
        pass
    recommendations = utilities.get_recommendations(username)

    movie_id = int(request.args.get('movie'))
    movie = services.get_movie(movie_id, repo.repo_instance)
    movie['add_review_url'] = url_for('movies_bp.review_movie', movie=movie['id'])
    movie['watched_movie_url'] = url_for('movies_bp.watched_movie', movie=movie['id'])
    return render_template('movies/display_movie.html',
                           movie=movie,
                           genre_urls=utilities.get_genres_and_urls(),
                           selected_movies=utilities.get_selected_movies(2),
                           recommendations=recommendations
                           )


@movies_blueprint.route('/watched_movie', methods=['GET'])
@login_required
def watched_movie():
    username = session['username']
    recommendations = utilities.get_recommendations(username)
    movie_id = int(request.args.get('movie'))
    movie = services.get_movie(movie_id, repo.repo_instance)
    user = services.get_user(repo.repo_instance, username)
    user.watch_movie(movie)
    movie['add_review_url'] = url_for('movies_bp.review_movie', movie=movie['id'])
    return render_template('movies/watched_movie.html',
                           user=user,
                           movie=movie,
                           selected_movies=utilities.get_selected_movies(2),
                           recommendations=recommendations
                           )


@movies_blueprint.route('/browse_genres', methods=['GET'])
def browse_genres():
    username = None
    try:
        username = session['username']
    except:
        pass
    recommendations = utilities.get_recommendations(username)

    return render_template('movies/browse_genres.html',
                           genre_urls=utilities.get_genres_and_urls(),
                           selected_movies=utilities.get_selected_movies(),
                           recommendations=recommendations
                           )


@movies_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review_movie():
    # Obtain the username of the currently logged in user.
    username = session['username']
    recommendations = utilities.get_recommendations(username)

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with a movie id, when subsequently called with a HTTP POST request, the movie id remains in the
    # form.
    form = ReviewForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the review text has passed data validation.
        # Extract the movie id, representing the reviewed movie, from the form.
        movie_id = int(form.movie_id.data)

        # Use the service layer to store the new review.
        services.add_review(movie_id, form.review.data, form.rating.data, username, repo.repo_instance)

        # Retrieve the movie in dict form.
        movie = services.get_movie(movie_id, repo.repo_instance)

        # Cause the web browser to display the page of all movies that have the same title as the commented movie,
        # and display all reviews, including the new review.
        return redirect(url_for('movies_bp.movies_by_title', title=movie['title'], view_reviews_for=movie_id))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the movie id, representing the movie to review, from a query parameter of the GET request.
        movie_id = int(request.args.get('movie'))

        # Store the movie id in the form.
        form.movie_id.data = movie_id
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the movie id of the movie being reviewed from the form.
        movie_id = int(form.movie_id.data)

    # For a GET or an unsuccessful POST, retrieve the movie to review in dict form, and return a Web page that allows
    # the user to enter a review. The generated Web page includes a form object.
    movie = services.get_movie(movie_id, repo.repo_instance)
    return render_template(
        'movies/review_movie.html',
        title='Edit review',
        movie=movie,
        form=form,
        handler_url=url_for('movies_bp.review_movie'),
        selected_movies=utilities.get_selected_movies(),
        genre_urls=utilities.get_genres_and_urls(),
        recommendations=recommendations
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise validators.ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        validators.DataRequired(message="Your review is required"),
        validators.Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])
    rating = IntegerField("Rating", [validators.NumberRange(min=0, max=10)])
    movie_id = HiddenField("Movie id")
    submit = SubmitField('Submit')
