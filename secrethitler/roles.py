from .singleton import *

class Role(object, metaclass=Singleton):
    pass

class Fascist(Role):
    def __str__(self):
        return "Fascist"

class Liberal(Role):
    def __str__(self):
        return "Liberal"

class Hitler(Fascist):
    def __str__(self):
        return "Hitler"
