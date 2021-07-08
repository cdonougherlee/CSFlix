
from flix.domainmodel.director import Director
#from flix.domainmodel.review import Review

class Movie:
    def __init__(self, title : str, release_year : int ):
        if title == "" or type(title) is not str:
            self.__title = None
        else:
            self.__title = title.strip()

        if type(release_year) is not int or release_year<1900:
            self.__release_year = None
        else:
            self.__release_year = release_year

        self.description = None
        self.director = None
        self.actors = []
        self.genres = []
        self.runtime_minutes = None
        self.rating = None
        self.votes = None
        self.revenue = "N/A" #millions
        self.metascore = "N/A"
        self.reviews =[]
        self.id = None

    @property
    def title(self):
        return self.__title

    @property
    def release_year(self):
        return self.__release_year

    @property
    def description(self):
        return self.__description
    @description.setter
    def description(self, description):
        if description == "" or type(description) is not str:
            self.__description = None
        else:
            self.__description = description.strip()

    @property
    def director(self):
        return self.__director
    @director.setter
    def director(self, director):
        if type(director) != Director:
            self.__director = None
        else:
            self.__director = director

    @property
    def actors(self):
        return self.__actors
    @actors.setter
    def actors(self, actors):
        if type(actors) != list:
            self.__actors = []
        else:
            self.__actors = actors

    @property
    def genres(self):
        return self.__genres
    @genres.setter
    def genres(self, genres):
        if type(genres) != list:
            self.__genres = []
        else:
            self.__genres = genres

    @property
    def reviews(self):
        return self.__reviews
    @reviews.setter
    def reviews(self, reviews):
        if type(reviews) != list:
            self.__reviews = []
        else:
            self.__reviews = reviews


    @property
    def runtime_minutes(self):
        return self.__runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, runtime_minutes):
        if type(runtime_minutes) != int:
            self.__runtime_minutes = None
        elif runtime_minutes < 0:
            raise ValueError
        else:
            self.__runtime_minutes = runtime_minutes

    @property
    def rating(self):
        return self.__rating
    @rating.setter
    def rating(self, rating):
        if type(rating) != float:
            self.__rating = None
        elif rating<0 or rating>10:
            self.__rating = None
        else:
            self.__rating = rating

    @property
    def votes(self):
        return self.__votes
    @votes.setter
    def votes(self, votes):
        if type(votes) != int or votes<0:
            self.__votes = None
        else:
            self.__votes = votes

    @property
    def revenue(self):
        return self.__revenue
    @revenue.setter
    def revenue(self, revenue):
        if revenue == "N/A":
            self.__revenue = "N/A"
        elif (type(revenue) == int or type(revenue) == float) and revenue >= 0:
            self.__revenue = revenue
        else:
            self.__revenue = "N/A"

    @property
    def metascore(self):
        return self.__metascore
    @metascore.setter
    def metascore(self, metascore):
        if metascore == "N/A":
            self.__metascore = "N/A"
        elif type(metascore) == int and metascore >0:
            self.__metascore = metascore
        else:
            self.__metascore = "N/A"

    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, id):
        if type(id) == int:
            self.__id = id
        else:
            self.__id = None

    def __repr__(self):
        return f'<Movie {self.__title}, {self.__release_year}>'

    def __eq__(self, other):
        if self.__title == other.title and self.__release_year == other.release_year:
            return True
        return False

    def __lt__(self, other):
        if self.__title == other.title:
            if self.__release_year < other.release_year:
                return True
            else:
                return False
        else:
            if self.__title < other.title:
                return True
            else:
                return False

    def __hash__(self):
        return hash((self.__title, self.__release_year))

    def add_actor(self, actor):
        self.__actors.append(actor)
    def remove_actor(self, actor):
        if actor in self.__actors:
            self.__actors.remove(actor)

    def add_genre(self, genre):
        self.__genres.append(genre)
    def remove_genre(self, genre):
        if genre in self.__genres:
            self.__genres.remove(genre)

    def add_review(self, review):
        self.__reviews.append(review)
    def remove_review(self, review):
        if review in self.__reviews:
            self.__reviews.remove(review)


class TestMovieMethods:
    def test_init(self):

        #repr
        movie1 = Movie("Moana", 2016)
        assert movie1.__repr__() == '<Movie Moana, 2016>'
        movie2 = Movie("", 2016)
        print(movie2)
        assert movie2.__repr__() == '<Movie None, 2016>'
        movie3 = Movie(24, 2006)
        assert movie3.__repr__() == '<Movie None, 2006>'
        movie4 = Movie("Moana", "")
        assert movie4.__repr__() == '<Movie Moana, None>'
        movie5 = Movie("Moana", 1888)
        assert movie5.__repr__() == '<Movie Moana, None>'
        movie6 = Movie("", "")
        assert movie6.__repr__() == '<Movie None, None>'

        #eq
        movie7 = Movie("Moana", 2016)
        assert movie1.__eq__(movie7) == True
        assert movie1.__eq__(movie1) == True
        assert movie1.__eq__(movie2) == False

        #lt
        movie8 = Movie("Moana", 2006)
        assert movie8.__lt__(movie1) == True
        assert movie8.__lt__(movie8) == False
        assert movie1.__lt__(movie8) == False

        #hash
        assert hash(movie8) == hash(movie8)
        assert hash(movie7) == hash(movie1)
        assert hash(movie8) != hash(movie1)
        assert hash(movie8) != hash(movie2)

        #add and remove actor and genres
        #works

        #### EXTENSION ####

        #metascore
        movie1.metascore = 210
        assert movie1.metascore == 210
        movie2.metascore = 'lsdflfaskf'
        assert movie2.metascore == "N/A"
        movie3.metascore = -123
        assert movie3.metascore == 'N/A'

        #revenue
        movie1.revenue = 333.13
        assert movie1.revenue == 333.13
        movie2.revenue = 333
        assert movie2.revenue == 333
        movie3.revenue = -123
        assert movie3.revenue == "N/A"
        movie4.revenue = 'sadhjkfasdjkfh'
        assert movie4.revenue == 'N/A'

        #votes
        movie1.votes = 132456
        assert movie1.votes == 132456
        movie2.votes = -456123
        assert movie2.votes == None
        movie3.votes = 'sadfkasdgk'
        assert movie3.votes == None

        #rating
        movie1.rating = 8.1
        assert movie1.rating == 8.1
        movie2.rating = 8.0
        assert movie2.rating == 8.0
        movie3.rating = -45
        assert movie3.rating == None
        movie4.rating = 45
        assert movie4.rating == None
        movie5.rating = 'sdjfasdgkfjgkj'
        assert movie5.rating == None
