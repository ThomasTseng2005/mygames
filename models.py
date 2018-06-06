from random import randint
class User(object):
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.score = 0
        self.guessing_number = 0


class NumberGuessingGame():
    def __init__(self):
        self.number = 0
        self.guesses = {}
        self.numberguessinggamesame = False

    def get_new_number(self):
        self.number = randint(0,100)

class TeamGenerator():
    def __init__(self):
        self.peoplenumber = 0
        self.groupnumber = 0
        self.everyone = {}

