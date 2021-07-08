from flix.domainmodel.movie import Movie


class WatchList:
    def __init__(self):
        self.__watchlist = []

    def add_movie(self, movie: Movie):
        if movie not in self.__watchlist:
            self.__watchlist.append(movie)

    def remove_movie(self, movie: Movie):
        if movie in self.__watchlist:
            self.__watchlist.remove(movie)

    def select_movie_to_watch(self, index: int):
        if 0 <= index < len(self.__watchlist) and len(self.__watchlist) > 0:
            return self.__watchlist[index]
        else:
            return None

    def size(self):
        return len(self.__watchlist)

    def first_movie_in_watchlist(self):
        if len(self.__watchlist) == 0:
            return None
        else:
            return self.__watchlist[0]

    def __repr__(self):
        return f'Watchlist: {self.__watchlist}'

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self.__watchlist):
            result = self.__watchlist[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration

    @property
    def watchlist(self):
        return self.__watchlist

# tests were done on coderunner, all passed
