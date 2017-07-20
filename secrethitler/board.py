from .presidential_powers import *
from .win_conditions import *
from .policies import *

import random


"""Define the liberal and fascist tracks
"""

class Track(object):
    """A glorified counter, but it makes sense for there to be a track base-class like this, sooo
    """
    def __init__(self, policy_slots):
        self.policies = 0
        self.policy_slots = policy_slots

    def place_policy(self):
        self.policies += 1

    def is_full(self):
        return self.policies == self.policy_slots


class FascistTrack(Track):
    """Represents the board for the fascist policies
    """
    def __init__(self, presidential_powers, policies=6, confirm_chancellor_after_x_policies=3, veto_after_x_policies=5):
        if not isinstance(confirm_chancellor_after_x_policies, int):
            raise ValueError("Confirm chancellor after x policies not an integer")
        if not isinstance(veto_after_x_policies, int):
            raise ValueError("Veto after x policies not an integer")
        if not isinstance(presidential_powers, dict):
            raise ValueError("Presidential powers should come as a dict- policy_num: Power()")
        if any([not isinstance(power, PresidentialPower) for power in presidential_powers.values()]):
            raise ValueError("Not all fascist track init list elements are presidential powers..")
        self.presidential_powers = presidential_powers
        self.confirm_chancellor_after_x_policies = confirm_chancellor_after_x_policies
        self.veto_after_x_policies = veto_after_x_policies
        super(FascistTrack, self).__init__(policies)

    def check_power(self, number_of_policies):
        """Checks what power is activated after N policies
        """
        return self.presidential_powers.get(number_of_policies, NoPower())

    def check_current_power(self):
        return self.check_power(self.policies)

    def is_veto_enabled(self):
        return self.policies >= self.veto_after_x_policies

    def should_ask_if_chancellor_is_hitler(self):
        return self.policies >= self.confirm_chancellor_after_x_policies


class LiberalTrack(Track):
    """Represents the board for the liberal policies
    """
    def __init__(self, policies=5):
        super(LiberalTrack, self).__init__(policies)


"""Define how the policy deck works
"""

class Deck(object):
    """Actually both the deck and the discard pile, whoops
    This class reshuffles the deck for us when it's empty pretty much
    """
    def __init__(self, cards):
        self.cards = list(cards)
        self.used = list(()) # Why this syntax and not []? Because why not. These two lines look great together
        random.shuffle(self.cards)
        self.shuffle_counter = 0

    def reshuffle(self):
        self.cards.extend(self.used)
        self.used = list(())
        random.shuffle(self.cards)
        self.shuffle_counter += 1

    def peek(self, number_of_cards):
        if len(self.cards) < number_of_cards:
            self.reshuffle()
        # Return the last N cards, because draw() is LIFO (pop)
        return self.cards[::-1][:number_of_cards]

    def draw(self, number_of_cards):
        if len(self.cards) < number_of_cards:
            self.reshuffle()
        # Remove N cards from the top
        return [self.cards.pop() for i in range(number_of_cards)]

    def discard(self, card):
        self.used.append(card)


"""Define the full board type
"""

class Board(object):
    """The game board features a deck of policy cards (11 fascist & 8 liberal),
    a liberal and fascist board and also the election tracker
    """
    def __init__(self, fascist_track, liberal_track):
        self.all_policies = [FascistPolicy()] * 11 + [LiberalPolicy()] * 8
        self.policies = Deck(self.all_policies)
        if not isinstance(fascist_track, FascistTrack):
            raise ValueError("Board init param needs to be fascist track")
        if not isinstance(liberal_track, LiberalTrack):
            raise ValueError("Board init param needs to be liberal track")
        self.fascist_track = fascist_track
        self.liberal_track = liberal_track
        self.failed_election_count = 0

    def peek_policies(self, number_of_policies):
        return self.policies.peek(number_of_policies)

    def draw_policies(self, number_of_policies):
        return self.policies.draw(number_of_policies)

    def discard_policy(self, policy):
        self.policies.discard(policy)

    def place_policy(self, policy):
        if policy is FascistPolicy():
            self.fascist_track.place_policy()
        elif policy is LiberalPolicy():
            self.liberal_track.place_policy()
        else:
            raise ValueError("Policy is not a liberal/fascist tile..")

    def should_ask_if_chancellor_is_hitler(self):
        return self.fascist_track.should_ask_if_chancellor_is_hitler()

    def is_veto_enabled(self):
        return self.fascist_track.is_veto_enabled()


class SmallGameBoard(Board):
    def __init__(self):
        powers = {3: ExamineCardsPower(),
                  4: KillPower(),
                  5: KillPower()}
        super(SmallGameBoard, self).__init__(FascistTrack(powers), LiberalTrack())


class MediumGameBoard(Board):
    def __init__(self):
        powers = {2: InvestigativePower(),
                  3: SurpriseElectionPower(),
                  4: KillPower(),
                  5: KillPower()}
        super(MediumGameBoard, self).__init__(FascistTrack(powers), LiberalTrack())


class LargeGameBoard(Board):
    def __init__(self):
        powers = {1: InvestigativePower(),
                  2: InvestigativePower(),
                  3: SurpriseElectionPower(),
                  4: KillPower(),
                  5: KillPower()}
        super(LargeGameBoard, self).__init__(FascistTrack(powers), LiberalTrack())
