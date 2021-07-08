from flask import Blueprint, render_template, session, url_for

import flix.utilities.utilities as utilities
from flix.authentication.authentication import login_required

stats_blueprint = Blueprint(
    'stats_bp', __name__)


@stats_blueprint.route('/display_stats', methods=['GET'])
@login_required
def stats():
    username = session['username']
    recommendations = utilities.get_recommendations(username)
    user = utilities.get_user_obj(username)
    for movie in user.watched_movies:
        movie['display_movie_url'] = url_for('movies_bp.display_movie', movie=movie['id'])
    return render_template(
        'stats/stats.html',
        selected_movies=utilities.get_selected_movies(),
        genre_urls=utilities.get_genres_and_urls(),
        recommendations=recommendations,
        user=user
    )
