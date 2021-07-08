from flask import Blueprint, request, render_template, redirect, url_for, session

import flix.adapters.repository as repo
import flix.utilities.services as services

# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_genres_and_urls():
    genre_names = services.get_genre_names(repo.repo_instance)
    genre_urls = dict()
    for genre_name in genre_names:
        genre_urls[genre_name] = url_for('movies_bp.movies_by_genre', genre=genre_name)

    return genre_urls


def get_selected_movies(quantity=3):
    movies = services.get_random_movies(quantity, repo.repo_instance)
    movies = services.movies_to_dict(movies)
    for movie in movies:
        movie['movie_url'] = url_for('movies_bp.movies_by_title', title=movie['title'])
    return movies


def get_recommendations(username):
    recommendations = []
    user = services.get_user(repo.repo_instance, username)
    if user is None:
        return recommendations
    else:
        recommendations += (services.get_genre_recommendation(repo.repo_instance, 1, user))
        recommendations += (services.get_director_recommendation(repo.repo_instance, 1, user))
        recommendations += (services.get_watch_it_again_recommendation(1, user))

    recommendations = services.movies_to_dict(recommendations)
    for movie in recommendations:
        movie['movie_url'] = url_for('movies_bp.movies_by_title', title=movie['title'])
    return recommendations


def get_user_obj(username):
    return services.get_user(repo.repo_instance, username)
