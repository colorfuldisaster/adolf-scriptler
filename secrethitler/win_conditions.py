class HitlerElectedWinCondition(FascistWinCondition):
    """Hitler elected chancellor
    """
    pass

class FascistPolicyWinCondition(FascistWinCondition):
    """Fascist track full with fascist policies
    """
    pass

class HitlerKilledWinCondition(LiberalWinCondition):
    """The president chooses to kill hitler
    """
    pass

class LiberalPolicyWinCondition(LiberalWinCondition):
    """Liberal track full with liberal policies
    """
    pass

class FascistWinCondition(WinCondition):
    pass

class LiberalWinCondition(WinCondition):
    pass

class WinCondition(Exception):
    pass
