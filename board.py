from presidential_powers import *
from win_conditions import *


class SmallGameBoard(Board):
    def __init__(self):
        fascist_board = FascistHalfBoard((NoPower(), NoPower(), ExamineCardsPower(), KillPower(), KillPower(), NoPower()))
        super(SmallGameBoard, self).__init__(fascist_board, LiberalHalfBoard())


class MediumGameBoard(Board):
    def __init__(self):
        fascist_board = FascistHalfBoard((NoPower(), InvestigativePower(), SurpriseElectionPower(), KillPower(), KillPower(), NoPower()))
        super(MediumGameBoard, self).__init__(fascist_board, LiberalHalfBoard())


class BigGameBoard(Board):
    def __init__(self):
        fascist_board = FascistHalfBoard((NoPower(), NoPower(), ExamineCardsPower(), KillPower(), KillPower(), NoPower()))
        super(BigGameBoard, self).__init__(fascist_board, LiberalHalfBoard())


"""Define the liberal and fascist half-boards
"""

class FascistHalfBoard(HalfBoard):
    """Represents the board for the fascist policies
    We force it to have 6 presidential powers but in practice the 6th will never be played
    """
    def __init__(self, veto_after_x_policies, presidential_powers):
        if not isinstance(veto_after_x_policies, int) or veto_after_x_policies < 0:
            raise ValueError("Veto after x policies not an integer")
        if len(presidential_powers) is not 6:
            raise ValueError("Fascist half-board must have 5 possible presidential powers")
        if any([not isinstance(power, PresidentialPower) for power in presidential_powers]):
            raise ValueError("Not all fascist half-board init list elements are presidential powers..")
        self.presidential_powers = list(presidential_powers)
        self.veto_after_x_policies = veto_after_x_policies
        super(FascistHalfBoard, self).__init__(6, FascistBoardFullWincon())

    def get_presidential_power(self):
        return presidential_powers.pop()

    def is_veto_enabled(self):
        return veto_after_x_policies <= self.policies_placed


class LiberalHalfBoard(HalfBoard):
    def __init__(self):
        super(LiberalHalfBoard, self).__init__(5, LiberalBoardFullWincon())


class HalfBoard(object):
    def __init__(self, policy_slots, half_board_full_event):
        self.policies_placed = 0
        self.policy_slots = policy_slots
        if not isinstance(half_board_full_event, Exception):
            raise ValueError("Event for half-board full must be an exception")
        self.half_board_full_event = half_board_full_event

    def place_policy(self):
        self.policies_placed += 1
        if self.policies_placed == self.policy_slots:
            raise half_board_full_event


"""Define the full board type
"""

class Board(object):
    """The game board features a deck of policy cards (11 fascist & 8 liberal),
    a liberal and fascist board and also the election tracker
    """
    class FascistPolicy(Policy):
        pass
    class LiberalPolicy(Policy):
        pass
    class Policy(object):
        pass

    def __init__(self, fascist_half_board, liberal_half_board):
        self.policies = Deck([FascistPolicy() * 11] + [LiberalPolicy() * 8])
        if not isinstance(fascist_half_board, FascistHalfBoard):
            raise ValueError("Board init param needs to be fascist half-baord")
        if not isinstance(liberal_half_board, LiberalHalfBoard):
            raise ValueError("Board init param needs to be liberal half-baord")
        self.fascist_half_board = fascist_half_board
        self.liberal_half_board = liberal_half_board

    def place_fascist_policy(self):
        fascist_half_board.place_policy()
        power = fascist_half_board.get_presidential_power()
        return power.method

    def place_liberal_policy(self):
        liberal_half_board.place_policy()
