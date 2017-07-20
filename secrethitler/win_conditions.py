from .singleton import *

class WinCondition(object, metaclass=Singleton):
    pass

class FascistWinCondition(WinCondition):
    pass

class LiberalWinCondition(WinCondition):
    pass

class HitlerElectedWinCondition(FascistWinCondition):
    """Hitler elected chancellor
    """
    def __str__(self):
        return "Hitler was elected as chancellor."

class FascistPolicyWinCondition(FascistWinCondition):
    """Fascist track full with fascist policies
    """
    def __str__(self):
        return "Enacted enough fascist policies."

class HitlerKilledWinCondition(LiberalWinCondition):
    """The president chooses to kill hitler
    """
    def __str__(self):
        return "Killed Hitler."

class LiberalPolicyWinCondition(LiberalWinCondition):
    """Liberal track full with liberal policies
    """
    def __str__(self):
        return "Enacted enough liberal policies."
