from singleton import *

class Hitler(Fascist):
    __metaclass__ = Singleton

class Fascist(Role):
    __metaclass__ = Singleton

class Liberal(Role):
    __metaclass__ = Singleton

class Role(object):
    pass
