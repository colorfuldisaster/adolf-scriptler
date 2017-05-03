from singleton import *

class FascistPolicy(Policy):
    __metaclass__ = Singleton

class LiberalPolicy(Policy):
    __metaclass__ = Singleton

class VetoPolicy(Policy):
    __metaclass__ = Singleton

class Policy(object):
    def __init__(self):
        raise NotImplementedError("This is an abstract class")
