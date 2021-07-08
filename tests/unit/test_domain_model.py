from flix.domainmodel.review import Review
from flix.domainmodel.movie import Movie
from flix.domainmodel.actor import Actor
from flix.domainmodel.genre import Genre
from flix.domainmodel.director import Director
from flix.domainmodel.user import User


def test_actor_methods():
    actor1 = Actor("Angelina Jolie")
    assert actor1.__repr__() == "<Actor Angelina Jolie>"
    actor2 = Actor("")
    assert actor2.actor_full_name == None
    actor3 = Actor(324)
    assert actor3.actor_full_name == None
    actor4 = Actor("Dylan Yates")
    assert actor4.__eq__(actor1) == False
    assert actor4.__eq__(actor4) == True
    assert actor1.__lt__(actor4) == True
    assert actor1.__lt__(actor1) == False
    assert actor4.__lt__(actor1) == False
    assert hash(actor4) == hash(actor4)
    assert hash(actor1) != hash(actor4)

def test_director_methods():
    director1 = Director("Taika Waititi")
    assert repr(director1) == "<Director Taika Waititi>"
    director2 = Director("Cameron Lee")
    director3 = Director(42)
    assert director3.director_full_name is None

    director5 = Director("")
    assert director5.director_full_name is None

    director4 = Director("Taika Waititi")
    assert director4.__eq__(director1) == True
    assert director4.__lt__(director1) == False
    assert director4.__lt__(director2) == False
    assert director2.__lt__(director4) == True

    assert hash(director4) == hash(director1)

def test_genre_methods():
    genre1 = Genre('Horror')
    assert genre1.__repr__() == '<Genre Horror>'
    genre2 = Genre('Comedy')
    assert genre1.__lt__(genre2) == False
    assert genre1.__lt__(genre1) == False
    assert genre2.__lt__(genre1) == True
    genre3 = Genre(56)
    assert genre3.genre is None

    assert genre1.__eq__(genre1) == True

def test_movie_methods():

    #repr
    movie1 = Movie("Moana", 2016)
    assert movie1.__repr__() == '<Movie Moana, 2016>'
    movie2 = Movie("", 2016)
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

def test_review_methods():
    user1 = "user1"
    user2 = "user2"
    movie = Movie("Moana", 2016)
    review_text = "This movie was very enjoyable."
    rating = 8
    review1 = Review(user1, movie, review_text, rating)

    movie = Movie("Moana", 2016)
    review_text = "This movie was very enjoyable."
    rating = 8
    review2 = Review(user1, movie, review_text, rating)

    movie = Movie("Cats", 2016)
    review_text = "This movie was very lame."
    rating = 4
    review3 = Review(user2, movie, review_text, rating)

    assert review1.__eq__(review2) == True
    assert review1.__eq__(review1) == True
    assert review1.__eq__(review3) == False

def test_user_methods():
    user1 = User('Martin', 'pw12345')
    user2 = User('Ian', 'pw67890')
    user3 = User('Daniel', 'pw87465')
    user4 = User('Martin', 'pw1255')
    assert user1.__eq__(user2) == False
    assert user1.__eq__(user1) == True
    assert user1.__eq__(user4) == True
    assert user3.__lt__(user1) == True
    assert user3.__lt__(user3) == False
    assert user1.__lt__(user3) == False
