from singleton import *

class Ja(Vote):
    __metaclass__ = Singleton

class Nein(Vote):
    __metaclass__ = Singleton

class Vote(object):
    pass
