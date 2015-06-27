from json import dumps
from static import queries
from random import choice

db = queries.Database()

class Building:

    def __init__(self, *args, **kwargs):
        self.name = args[0]
        self.reqPopulation = args[1]
        self.requiredProfession = args[2]

    def __str__(self):
        return dumps(self.__dict__)


if __name__ == '__main__':
    t = Town(1500, 'Agricultural')
    t.get_important_businesses()
