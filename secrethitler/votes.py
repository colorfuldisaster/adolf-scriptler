from .singleton import *

class Vote(object, metaclass=Singleton):
    pass

class Ja(Vote):
    pass

class Nein(Vote):
    pass
