from singleton import *

class Policy(object):
    pass

class FascistPolicy(Policy):
    __metaclass__ = Singleton
    def __str__(self):
        return "Fascist"

class LiberalPolicy(Policy):
    __metaclass__ = Singleton
    def __str__(self):
        return "Liberal"

class VetoPolicy(Policy):
    __metaclass__ = Singleton
