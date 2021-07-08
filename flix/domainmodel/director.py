class Director:

    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    def __repr__(self):
        return f"<Director {self.__director_full_name}>"

    def __eq__(self, other):
        if self.__director_full_name == other.director_full_name:
            return True
        return False

    def __lt__(self, other):
        if self.__director_full_name < other.director_full_name:
            return True
        return False

    def __hash__(self):
        return hash(self.__director_full_name)


class TestDirectorMethods:

    def test_init(self):
        director1 = Director("Taika Waititi")
        assert repr(director1) == "<Director Taika Waititi>"
        director2 = Director("Cameron Lee")
        director3 = Director(42)
        assert director3.director_full_name is None

        director8 = Director("")
        assert director8.director_full_name is None

        #testing eq
        director4 = Director("Taika Waititi")
        assert director4.__eq__(director1) == True

        #testing lt
        assert director4.__lt__(director1) == False
        assert director4.__lt__(director2) == False
        assert director2.__lt__(director4) == True

        assert hash(director4) == hash(director1)