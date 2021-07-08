class Actor:
    def __init__(self, actor_name : str):
        self.__actor_colleagues = []
        if actor_name == "" or type(actor_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_name.strip()

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    @property
    def actor_colleagues(self) -> list:
        return self.__actor_colleagues

    def __repr__(self):
        return f'<Actor {self.__actor_full_name}>'

    def __eq__(self, other):
        if self.__actor_full_name == other.actor_full_name:
            return True
        return False

    def __lt__(self, other):
        if self.__actor_full_name < other.actor_full_name:
            return True
        return False

    def __hash__(self):
        return hash(self.__actor_full_name)

    def add_actor_colleague(self, colleague):
        if self.__actor_full_name != colleague.actor_full_name:
            self.__actor_colleagues.append(colleague)

    def check_if_this_actor_worked_with(self, colleague):
        if colleague.actor_full_name in self.__actor_colleagues:
            return True
        else:
            return False

class TestActorMethods:

    def test_init(self):
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
