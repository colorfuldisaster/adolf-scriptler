from singleton import *

class Vote(object):
    pass

class Ja(Vote):
    __metaclass__ = Singleton

class Nein(Vote):
    __metaclass__ = Singleton
