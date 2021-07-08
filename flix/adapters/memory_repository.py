import csv
import os

from werkzeug.security import generate_password_hash

from flix.domainmodel.movie import Movie
from flix.domainmodel.actor import Actor
from flix.domainmodel.genre import Genre
from flix.domainmodel.director import Director
from flix.domainmodel.user import User
from bisect import bisect, bisect_left, insort_left

from flix.adapters.repository import AbstractRepository

from fuzzywuzzy import fuzz


class MemoryRepository(AbstractRepository):
    # Movies are sorted by title in alphabetical order.

    def __init__(self):
        self.__dataset_of_movies = list()
        self.__dataset_of_actors = set()
        self.__dataset_of_directors = set()
        self.__dataset_of_genres = set()
        self.__dataset_of_users = list()
        self.__movies_index = dict()

    @property
    def dataset_of_movies(self):
        return self.__dataset_of_movies

    @property
    def dataset_of_actors(self):
        return self.__dataset_of_actors

    @property
    def dataset_of_directors(self):
        return self.__dataset_of_directors

    @property
    def dataset_of_genres(self):
        return self.__dataset_of_genres

    @property
    def dataset_of_users(self):
        return self.__dataset_of_users

    def get_movies_by_title(self, title: str):  # 1
        # returns the movie objects with title == title string in a list.
        return_movies = []
        for movie in self.__dataset_of_movies:
            ratio = fuzz.ratio(title.lower().strip(), movie.title.lower())
            if ratio > 60:
                return_movies.append(movie)
        return return_movies

    def get_movies_by_director(self, director: str):  # 2
        # returns list of movies directed by director (str).
        movies_list = list()
        for movie in self.__dataset_of_movies:
            ratio = fuzz.ratio(director.lower().strip(), movie.director.director_full_name.lower())
            if ratio > 80:
                movies_list.append(movie)
        return movies_list

    def get_movies_by_genre(self, genre: str):  # 3
        # returns list of all movies that are categorised as genre (str).
        movie_list = list()
        for movie in self.__dataset_of_movies:
            for movie_genre in movie.genres:
                ratio = fuzz.ratio(genre.lower().strip(), movie_genre.genre.lower())
                if ratio == 100:
                    movie_list.append(movie)
        return movie_list

    def get_movies_by_actor(self, actor: str):  # 4
        # returns list of all movies that actor (str) starred in.
        movie_list = list()
        for movie in self.__dataset_of_movies:
            for movie_actor in movie.actors:
                ratio = fuzz.ratio(actor.lower().strip(), movie_actor.actor_full_name.lower())
                if ratio > 75:
                    movie_list.append(movie)
        return movie_list

    def get_first_movie(self):  # 5
        # returns first movie in dataset (sorted by alphabetical order).
        movie = None
        if len(self.__dataset_of_movies) > 0:
            movie = self.__dataset_of_movies[0]
        return movie

    def get_last_movie(self):  # 6
        # returns last movie in dataset
        movie = None
        if len(self.__dataset_of_movies) > 0:
            movie = self.__dataset_of_movies[-1]
        return movie

    def add_user(self, user: User):  # 7
        # add a user to the dataset
        self.__dataset_of_users.append(user)

    def get_user(self, name: str):  # 8
        # returns the user Object associated with the name string, None if the username isn't valid.
        return_user = None
        if type(name) == str:
            for user in self.__dataset_of_users:
                if name.lower() == user.user_name:
                    return_user = user
        return return_user

    def add_movie(self, movie: Movie):  # 9
        insort_left(self.__dataset_of_movies, movie)
        self.__movies_index[movie.id] = movie

    def get_movie_by_id(self, id: int):  # 10
        if id in self.__movies_index.keys():
            return self.__movies_index[id]

    def get_movies_by_id(self, id_list: list):  # 11
        actual_ids = list()
        for id in id_list:
            if id in self.__movies_index:
                actual_ids.append(id)
        movies_list = list()
        for id in actual_ids:
            for movie in self.__dataset_of_movies:
                if movie.id == id:
                    movies_list.append(movie)
        return movies_list

    def get_number_of_movies(self):  # 12
        # returns amount of movies currently in dataset.
        return len(self.__dataset_of_movies)

    def add_genre(self, genre: Genre):  # 13
        self.__dataset_of_genres.add(genre)

    def get_genres(self):  # 14
        return self.__dataset_of_genres

    def add_actor(self, actor: Actor):  # 15
        self.__dataset_of_actors.add(actor)

    def get_actors(self):  # 16
        return self.__dataset_of_actors

    def add_director(self, director: Director):  # 17
        self.__dataset_of_directors.add(director)

    def get_directors(self):  # 18
        return self.__dataset_of_directors

    def get_movie_index(self, movie: Movie):  # 19
        index = bisect_left(self.__dataset_of_movies, movie)
        if index != len(self.__dataset_of_movies):
            return index
        raise ValueError

    def get_title_of_previous_movie(self, movie: Movie):  # 20
        previous_title = None
        try:
            index = self.__dataset_of_movies.index(movie)
            for stored_movie in self.__dataset_of_movies[0:index]:
                previous_title = stored_movie.title
        except ValueError:
            pass
        return previous_title

    def get_title_of_next_movie(self, movie: Movie):  # 21
        next_title = None
        try:
            index = self.__dataset_of_movies.index(movie)
            for stored_movie in reversed(self.__dataset_of_movies[index + 1:len(self.__dataset_of_movies)]):
                next_title = stored_movie.title
        except ValueError:
            pass
        return next_title

    def get_movies(self):  # 22
        return self.__dataset_of_movies

    def get_movie_ids_for_genre(self, genre: Genre):  # 23
        movie_id_list = list()
        for movie in self.__dataset_of_movies:
            if genre in movie.genres:
                movie_id_list.append(movie.id)
        return movie_id_list

    def get_movies_by_exact_title(self, title: str):
        # returns the movie objects with title == title string in a list.
        return_movies = []
        for movie in self.__dataset_of_movies:
            ratio = fuzz.ratio(title.lower().strip(), movie.title.lower())
            if ratio == 100:
                return_movies.append(movie)
        return return_movies


# functions to assist testing
def read_csv_file(filename: str):
    with open(filename, mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_users(data_path, repo):
    users = dict()

    for data_row in read_csv_file(os.path.join(data_path, 'users.csv')):
        username = data_row[1]
        password = generate_password_hash(data_row[2])
        user = User(username, password)
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def load_movies_and_genres_and_directors_and_actors(data_path, repo):
    for row in read_csv_file(os.path.join(data_path, 'Data1000Movies.csv')):
        title = row[1]
        release_year = int(row[6])
        runtime = int(row[7])
        description = row[3]

        genre_list = row[2].split(',')
        for i in range(len(genre_list)):
            genre_list[i] = Genre(genre_list[i])

        director = Director(row[4])

        actor_list = row[5].split(',')
        for i in range(len(actor_list)):
            actor_list[i] = Actor(actor_list[i])
        for actor_obj in actor_list:
            for colleague in actor_list:
                if colleague not in actor_obj.actor_colleagues:
                    actor_obj.add_actor_colleague(colleague)

        rating = float(row[8])
        votes = int(row[9])

        if row[10] == "N/A":
            revenue = "N/A"
        else:
            revenue = float(row[10])

        if row[11] == "N/A":
            metascore = "N/A"
        else:
            metascore = int(row[11])

        id = int(row[0])

        # create movie object and assign everything
        movie = Movie(title, release_year)
        movie.actors = actor_list
        movie.genres = genre_list
        movie.director = director
        movie.description = description
        movie.runtime_minutes = runtime
        movie.rating = rating
        movie.votes = votes
        movie.revenue = revenue
        movie.metascore = metascore
        movie.id = id

        repo.add_movie(movie)
        for genre in movie.genres:
            repo.add_genre(genre)
        for actor in movie.actors:
            repo.add_actor(actor)
        repo.add_director(movie.director)


def populate(data_path, repo):
    load_users(data_path, repo)
    load_movies_and_genres_and_directors_and_actors(data_path, repo)
