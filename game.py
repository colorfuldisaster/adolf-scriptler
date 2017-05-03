from board import *
from win_conditions import *

import random

class Game(object):
    class Statistics(object):
        """Logically bundle the public game stats for the player class
        """
        def __init__(self, board, roles):
            self.board = board
            self.roles = roles
            self.previous_president = None
            self.previous_chancellor = None
            self.nominations = []
            self.legislative_session_records = []

        @property
        def fascist_policies(self):
            """Number of fascist policies in law
            """
            return self.board.fascist_track.policies_placed

        @property
        def liberal_policies(self):
            """Number of liberal policies in law
            """
            return self.board.liberal_track.policies_placed

        @property
        def fascist_slots_remaining(self):
            """Remaining nubmer of fascist policies to enact before fascists win
            """
            return self.board.fascist_track.policy_slots - self.fascist_policies

        @property
        def liberal_slots_remaining(self):
            """Remaining number of liberal policies to enact before liberals win
            """
            return self.board.liberal_track.policy_slots - self.liberal_policies

        @property
        def election_tracker(self):
            return self.board.failed_election_count

        @property
        def persidential_powers(self):
            return list(self.board.fascist_track.presidential_powers)

        @property
        def all_policies(self):
            """Policy deck at the start of the game
            """
            return self.board.all_policies

        @property
        def all_roles(self):
            """List of roles at the start of the game
            """
            return self.roles

        @property
        def is_veto_enabled(self):
            return self.board.is_veto_enabled

        @property
        def is_chancellor_asked_if_hitler(self):
            return self.board.should_ask_if_chancellor_is_hitler()

    def __init__(self, players):
        # Choose board and roles based on number of players
        based_on_players = {5:     SmallGameBoard, [Hitler()] + [Fascist()] * 1 + [Liberal()] * 3
                            6:     SmallGameBoard, [Hitler()] + [Fascist()] * 1 + [Liberal()] * 4
                            7:     MediumGameBoard, [Hitler()] + [Fascist()] * 2 + [Liberal()] * 4
                            8:     MediumGameBoard, [Hitler()] + [Fascist()] * 2 + [Liberal()] * 5
                            9:     LargeGameBoard, [Hitler()] + [Fascist()] * 3 + [Liberal()] * 5
                            10:    LargeGameBoard, [Hitler()] + [Fascist()] * 3 + [Liberal()] * 6}
        try :
            self.board, self.roles = based_on_players[len(players)]
        except KeyError:
            raise KeyError("Invalid number of players: {}".format(len(players)))
        # Initialize other stuff
        self.stats = Statistics(self.board, self.roles)
        self.players = players
        random.shuffle(self.players)
        self.player_rotation = itertools.cycle(players)

    def play(self):
        self.distribute_roles()
        self.game_loop()

    def distribute_roles(self):
        roles = iter(self.roles)
        for player in self.players:
            player.setup(self.stats, roles.next())

    def game_loop(self):
        """Main game flow loop
        """
        try:
            while True:
                # Try to elect a government
                self.pass_presidency()
                self.nominate_chancellor()
                if self.vote_on_the_government()
                    # Government does stuff
                    self.legislative_session()
                    self.executive_action()
        except WinCondition as wc:
            pass # TODO

    def pass_presidency(self):
        self.stats.presidential_candidate = self.player_rotation.next()

    def nominate_chancellor(self):
        self.stats.nominated_chancellor = self.stats.presidential_candidate.nominate_chancellor()
        self.stats.nominations.append((self.stats.presidential_candidate, self.stats.nominated_chancellor))

    def vote_on_the_government(self):
        """Returns true if a government was elected
        """
        votes = [player.vote() for player in self.players]
        if votes.count(Ja()) > votes.count(Nein()):
            self.stats.current_president = self.stats.presidential_candidate
            self.stats.current_chancellor = self.stats.nominated_chancellor
            # Keep the president & chancellor who were last elected for eligibility reasons
            self.stats.previous_president = self.stats.current_president
            self.stats.previous_chancellor = self.stats.current_chancellor
            return True
        else:
            self.stats.current_president = None
            self.stats.current_chancellor = None
            self.board.advance_election_tracker()
            return False

    def legislative_session(self):
        if self.stats.current_president is None or self.stats.current_chancellor is None:
            return
        policies = self.board.draw_policies(3)
        # Pass three policies to the president
        policy = self.stats.current_president.choose_policies_for_chancellor(policies)
        # Discard the president's choice and keep the rest
        self.board.discard_policy(policy)
        policies.remove(policy)
        # Pass the two policies to the chancellor, and maybe offer a veto
        choice = self.current_chancellor.enact_policy()
        if choice is VetoPolicy() and not self.stats.is_veto_enabled:
            raise ValueError("Can't veto yet!!")
        elif choice is VetoPolicy():
            # Discard the remaining two policies
            self.board.discard_policy(policies.pop())
            self.board.discard_policy(policies.pop())
            self.board.advance_election_tracker()
        else:
            # Discard the remaining policy and enact the one chosen by the chancellor
            policies.remove(policy)
            self.board.discard_policy(policies.pop())
            self.board.place_policy(policy)

    def executive_action(self):
        if self.board.new_executive_action is not None:
            self.board.new_executive_action(self.current_president)
        # Reset the executive action in case next round of legislation doesn't place a policy at all
        self.board.new_executive_action = None
