from json import dumps


class NPC:

    def __init__(self, *args, **kwargs):
        self.first = args[0]
        self.last = args[1]
        self.sex = args[2]
        self.culture = args[3]


    def __str__(self):

        return dumps(self.__dict__)



if __name__ == '__main__':
    n = NPC('Bob', 'Jones', 'Male', 'American')

    n.professions = {'name': 'job', 'pay': 'lots'}

    print n

