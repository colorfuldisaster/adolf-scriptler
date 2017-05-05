from singleton import *

class Role(object):
    pass

class Fascist(Role):
    __metaclass__ = Singleton
    def __str__(self):
        return "Fascist"

class Liberal(Role):
    __metaclass__ = Singleton
    def __str__(self):
        return "Liberal"

class Hitler(Fascist):
    __metaclass__ = Singleton
    def __str__(self):
        return "Hitler"
