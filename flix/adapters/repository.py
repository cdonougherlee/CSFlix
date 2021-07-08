import abc

from flix.domainmodel.movie import Movie
from flix.domainmodel.actor import Actor
from flix.domainmodel.genre import Genre
from flix.domainmodel.director import Director
from flix.domainmodel.user import User


repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass

class AbstractRepository(abc.ABC):

    @abc.abstractmethod #1
    def get_movies_by_title(self, title :str):
        """returns a list of movies with title == title string"""
        raise NotImplementedError

    @abc.abstractmethod #2
    def get_movies_by_director(self, director : str):
        """returns list of movies directed by director (Director object)"""
        raise NotImplementedError

    @abc.abstractmethod #3
    def get_movies_by_genre(self, genre: str):
        """returns list of all movies that are categorised as genre (Genre object)"""
        raise NotImplementedError

    @abc.abstractmethod #4
    def get_movies_by_actor(self, actor:str):
        """returns list of all movies that actor (Actor object) starred in"""
        raise NotImplementedError

    @abc.abstractmethod #5
    def get_first_movie(self):
        """returns first movie in dataset (sorted by alphabetical order), None if dataset is empty"""
        raise NotImplementedError

    @abc.abstractmethod #6
    def get_last_movie(self):
        """returns last movie in dataset, None if dataset is empty"""
        raise NotImplementedError

    @abc.abstractmethod #7
    def add_user(self, user:User):
        """add a user to the dataset"""
        raise NotImplementedError

    @abc.abstractmethod #8
    def get_user(self, name : str):
        """returns the user Object associated with the name string,None if the username isn't valid"""
        raise NotImplementedError

    @abc.abstractmethod #9
    def add_movie(self, movie: Movie):
        """Adds a movie to dataset of movies list, adds movie id to movie id dict"""
        raise NotImplementedError

    @abc.abstractmethod #10
    def get_movie_by_id(self, id:int):
        """Returns the movie associated with the id"""
        raise NotImplementedError

    @abc.abstractmethod #11
    def get_movies_by_id(self, id_list:list):
        """returns a list of movies associated with the ids in the id list"""
        raise NotImplementedError

    @abc.abstractmethod  # 12
    def get_number_of_movies(self):
        """returns amount of movies currently in dataset"""
        raise NotImplementedError

    @abc.abstractmethod #13
    def add_genre(self, genre:Genre):
        """adds genre to genre dataset"""
        raise NotImplementedError

    @abc.abstractmethod  #14
    def get_genres(self):
        """Returns genre dataset"""
        raise NotImplementedError

    @abc.abstractmethod #15
    def add_actor(self, actor:Actor):
        """Adds actor to actor dataset"""
        raise NotImplementedError

    @abc.abstractmethod#16
    def get_actors(self):
        """Returns actor dataset"""
        raise NotImplementedError

    @abc.abstractmethod #17
    def add_director(self, director: Director):
        """Adds director obj to director datset"""
        raise NotImplementedError

    @abc.abstractmethod #18
    def get_directors(self):
        """returns directors dataset"""
        raise NotImplementedError

    @abc.abstractmethod #19
    def get_movie_index(self, movie: Movie):
        """returns the index of given movie obj in dataset of movies"""
        raise NotImplementedError

    @abc.abstractmethod #20
    def get_title_of_previous_movie(self, movie: Movie):
        """returns the previous movie title in the movies index dict"""
        raise NotImplementedError

    @abc.abstractmethod #21
    def get_title_of_next_movie(self, movie:Movie):
        """returns the next movie title in the movies index dict"""
        raise NotImplementedError

    @abc.abstractmethod #22
    def get_movies(self):
        """returns movies dataset"""
        raise NotImplementedError

    def get_movie_ids_for_genre(self, genre: Genre): #23
        """returns a list of ids of movies associated with the genre obj"""
        raise NotImplementedError

    def get_movies_by_exact_title(self, title: str):
        """returns the movie objects with title == title string in a list"""
        raise NotImplementedError
