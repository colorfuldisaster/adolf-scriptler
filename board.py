from presidential_powers import *
from win_conditions import *
from policies import *

import random

class SmallGameBoard(Board):
    def __init__(self):
        fascist_board = FascistTrack(3, 5, (NoPower(), NoPower(), ExamineCardsPower(), KillPower(), KillPower(), NoPower()))
        super(SmallGameBoard, self).__init__(fascist_board, LiberalTrack())


class MediumGameBoard(Board):
    def __init__(self):
        fascist_board = FascistTrack(3, 5, (NoPower(), InvestigativePower(), SurpriseElectionPower(), KillPower(), KillPower(), NoPower()))
        super(MediumGameBoard, self).__init__(fascist_board, LiberalTrack())


class LargeGameBoard(Board):
    def __init__(self):
        fascist_board = FascistTrack(3, 5, (NoPower(), NoPower(), ExamineCardsPower(), KillPower(), KillPower(), NoPower()))
        super(LargeGameBoard, self).__init__(fascist_board, LiberalTrack())


"""Define the liberal and fascist tracks
"""

class FascistTrack(Track):
    """Represents the board for the fascist policies
    We force it to have 6 presidential powers but in practice the 6th will never be played
    """
    def __init__(self, confirm_chancellor_after_x_policies, veto_after_x_policies, presidential_powers):
        if not isinstance(confirm_chancellor_after_x_policies, int):
            raise ValueError("Confirm chancellor after x policies not an integer")
        if not isinstance(veto_after_x_policies, int):
            raise ValueError("Veto after x policies not an integer")
        if len(presidential_powers) is not 6:
            raise ValueError("Fascist track must have 6 possible presidential powers")
        if any([not isinstance(power, PresidentialPower) for power in presidential_powers]):
            raise ValueError("Not all fascist track init list elements are presidential powers..")
        self.presidential_powers = iter(presidential_powers)
        self.confirm_chancellor_after_x_policies = confirm_chancellor_after_x_policies
        self.veto_after_x_policies = veto_after_x_policies
        super(FascistTrack, self).__init__(6, FascistPolicyWinCondition())

    def get_presidential_power(self):
        return presidential_powers.next()

    def is_veto_enabled(self):
        return veto_after_x_policies <= self.policies_placed

    def should_ask_if_chancellor_is_hitler(self):
        return confirm_chancellor_after_x_policies <= self.policies_placed


class LiberalTrack(Track):
    def __init__(self):
        super(LiberalTrack, self).__init__(5, LiberalPolicyWinCondition())


class Track(object):
    def __init__(self, policy_slots, track_full_event):
        self.policies_placed = 0
        self.policy_slots = policy_slots
        if not isinstance(track_full_event, Exception):
            raise ValueError("Event for track full must be an exception")
        self.track_full_event = track_full_event

    def place_policy(self):
        self.policies_placed += 1
        if self.policies_placed == self.policy_slots:
            raise track_full_event


"""Define how the policy deck works
"""

class Deck(object):
    """Actually both the deck and the discard pile, whoops
    """
    def __init__(self, cards):
        self.cards = list(cards)
        self.discard = list(())

    def reshuffle(self):
        self.cards = self.discard + self.cards
        self.discard = list(())
        random.shuffle(self.cards)

    def peek_cards(self, number_of_cards):
        if len(self.cards) < number_of_cards):
            self.reshuffle()
        # Return the last N cards, because in take_cards() we pop the last N cards
        return self.cards[-number_of_cards:]

    def take_cards(self, number_of_cards):
        if len(self.cards) < number_of_cards):
            self.reshuffle()
        cards_taken = [self.cards.pop() for i in number_of_cards]
        return cards_taken

    def discard(self, card):
        self.discard.append(card)


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
        self.new_executive_action = None

    def peek_policies(self, number_of_policies):
        return self.policies.peek_cards(number_of_policies)

    def draw_policies(self, number_of_policies):
        return self.policies.draw_cards(number_of_policies)

    def discard_policy(self, policy):
        self.policies.discard(policy)

    def place_policy(self, policy):
        if policy is FascistPolicy():
            self.reset_election_tracker()
            self.place_fascist_policy()
        elif policy is LiberalPolicy():
            self.reset_election_tracker()
            self.place_liberal_policy()
        else:
            raise ValueError("Policy is not a liberal/fascist tile..")

    def place_fascist_policy(self):
        fascist_track.place_policy()
        power = fascist_track.get_presidential_power()
        self.new_executive_action = power

    def place_liberal_policy(self):
        liberal_track.place_policy()

    def should_ask_if_chancellor_is_hitler(self):
        return fascist_track.should_ask_if_chancellor_is_hitler()

    def is_veto_enabled(self):
        return fascist_track.is_veto_enabled()

    def advance_election_tracker(self):
        """If we reach 3 failed elections in a row,
        the board draws the top policy and places it autonomously and the tracker is reset
        """
        self.failed_election_count += 1
        if self.failed_election_count == 3:
            policy = self.draw_policies(1)
            # Note that the tracker is reset every time we place a policy
            self.place_policy(policy)

    def reset_election_tracker(self):
        self.failed_election_count = 0
