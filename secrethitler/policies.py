from .singleton import *

class Policy(object, metaclass=Singleton):
    pass

class FascistPolicy(Policy):
    def __str__(self):
        return "Fascist"

class LiberalPolicy(Policy):
    def __str__(self):
        return "Liberal"

class VetoPolicy(Policy):
    def __str__(self):
        return "Veto"
