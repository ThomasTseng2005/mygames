from random import randint
class User(object):
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.score = 0
        self.guessing_number = 0


