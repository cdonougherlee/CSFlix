from flask import Blueprint, render_template, redirect, url_for, session, request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from functools import wraps

import flix.utilities.utilities as utilities
import flix.search.services as services
import flix.adapters.repository as repo

search_blueprint = Blueprint(
    'search_bp', __name__)


@search_blueprint.route("/search_by_title", methods=["GET", "POST"])
def search_by_title():
    username = None
    try:
        username = session['username']
    except:
        pass
    recommendations = utilities.get_recommendations(username)

    form = SearchForm()
    search_invalid = None

    if form.validate_on_submit():
        if services.check_if_title_valid(form.search.data, repo.repo_instance):
            return redirect(url_for('movies_bp.movies_by_search', search_query=form.search.data, search_type="title"))
        else:
            search_invalid = "Your search doesn't match any results"
    return render_template("search/make_search.html",
                           title="Search by title",
                           search_invalid_message=search_invalid,
                           form=form,
                           selected_movies=utilities.get_selected_movies(3),
                           recommendations=recommendations
                           )


@search_blueprint.route("/search_by_director", methods=["GET", "POST"])
def search_by_director():
    username = None
    try:
        username = session['username']
    except:
        pass
    recommendations = utilities.get_recommendations(username)

    form = SearchForm()
    search_invalid = None

    if form.validate_on_submit():
        if services.check_if_director_valid(form.search.data, repo.repo_instance):
            return redirect(
                url_for('movies_bp.movies_by_search', search_query=form.search.data, search_type="director"))
        else:
            search_invalid = "Your search doesn't match any results"
    return render_template("search/make_search.html",
                           title="Search by director",
                           search_invalid_message=search_invalid,
                           form=form,
                           selected_movies=utilities.get_selected_movies(3),
                           recommendations=recommendations
                           )


@search_blueprint.route("/search_by_genre", methods=["GET", "POST"])
def search_by_genre():
    username = None
    try:
        username = session['username']
    except:
        pass
    recommendations = utilities.get_recommendations(username)

    form = SearchForm()
    search_invalid = None

    if form.validate_on_submit():
        if services.check_if_genre_valid(form.search.data, repo.repo_instance):
            return redirect(url_for('movies_bp.movies_by_genre', genre=form.search.data.title()))
        else:
            search_invalid = "Your search doesn't match any results"
    return render_template("search/make_search.html",
                           title="Search by genre",
                           search_invalid_message=search_invalid,
                           form=form,
                           selected_movies=utilities.get_selected_movies(3),
                           recommendations=recommendations
                           )


@search_blueprint.route("/search_by_actor", methods=["GET", "POST"])
def search_by_actor():
    username = None
    try:
        username = session['username']
    except:
        pass
    recommendations = utilities.get_recommendations(username)

    form = SearchForm()
    search_invalid = None

    if form.validate_on_submit():
        if services.check_if_actor_valid(form.search.data, repo.repo_instance):
            return redirect(url_for('movies_bp.movies_by_search', search_query=form.search.data, search_type="actor"))
        else:
            search_invalid = "Your search doesn't match any results"
    return render_template("search/make_search.html",
                           title="Search by actor",
                           search_invalid_message=search_invalid,
                           form=form,
                           selected_movies=utilities.get_selected_movies(3),
                           recommendations=recommendations
                           )


class SearchForm(FlaskForm):
    search = StringField('Search query', [DataRequired(message='Enter a search')])
    submit = SubmitField('Search')
