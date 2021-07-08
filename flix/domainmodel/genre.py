class Genre:
    def __init__(self, genre: str):
        if genre == "" or type(genre) is not str:
            self.__genre = None
        else:
            self.__genre = genre.strip()

    @property
    def genre(self) -> str:
        return self.__genre

    def __repr__(self):
        return f'<Genre {self.__genre}>'

    def __eq__(self, other):
        if self.__genre == other.genre:
            return True
        return False

    def __lt__(self, other):
        if self.__genre < other.genre:
            return True
        return False

    def __hash__(self):
        return hash(self.__genre)

class TestGenreMethods:

    def test_init(self):
        genre1 = Genre('Horror')
        assert genre1.__repr__() == '<Genre Horror>'
        genre2 = Genre('Comedy')
        assert genre1.__lt__(genre2) == False
        assert genre1.__lt__(genre1) == False
        assert genre2.__lt__(genre1) == True
        genre3 = Genre(56)
        assert genre3.genre is None

        assert genre1.__eq__(genre1) == True


