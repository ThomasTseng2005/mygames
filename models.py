from random import randint
class User(object):
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.score = 0
        self.guessing_number = 0
        self.ngg = 100
        self.fd = 100


class NumberGuessingGame():
    def __init__(self):
        self.number = 0
        self.guesses = {}
        self.numberguessinggamesame = False

    def get_new_number(self):
        self.number = randint(1,100)

class TeamGenerator():
    def __init__(self):
        self.peoplenumber = 0
        self.groupnumber = 0
        self.everyone = {}
        self.message = ""
        self.messagetwo = ""
        self.people = []
        self.same = False
        self.first = []
        self.repick = False

    def reset(self):
        self.peoplenumber = 0
        self.groupnumber = 0
        self.everyone = {}
        self.message = ""
        self.messagetwo = ""
        self.people = []
        self.same = False

class FourDigits():
    def __init__(self):
        self.num = "0000"
        self.guesses = {}
        self.same = False
        self.repeat = False
        self.repeattwo = False
        self.a = 0
        self.b = 0









