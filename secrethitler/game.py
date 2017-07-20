from .board import *
from .roles import *
from .win_conditions import *
from .statemachine import *
from .votes import *

import itertools
import random


class Statistics(object):
    """Logically bundle the public game stats for the player class
    """
    def __init__(self, board, players, roles):
        self.board = board
        self.players = players
        self.roles = roles
        self.previous_president = None
        self.previous_chancellor = None
        self.wincon = None
        self.nominations = []
        self.legislative_session_records = []
        self.past_investigations = []

    @property
    def fascist_policies(self):
        """Number of fascist policies in law
        """
        return self.board.fascist_track.policies

    @property
    def liberal_policies(self):
        """Number of liberal policies in law
        """
        return self.board.liberal_track.policies

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

    @election_tracker.setter
    def election_tracker(self, value):
        self.board.failed_election_count = value

    @property
    def presidential_powers(self):
        """Returns a dict
        """
        return self.board.fascist_track.presidential_powers

    @property
    def current_presidential_power(self):
        return self.board.fascist_track.check_current_power()

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
        return self.board.is_veto_enabled()

    @property
    def is_chancellor_asked_if_hitler(self):
        return self.board.should_ask_if_chancellor_is_hitler()

    @property
    def shuffle_counter(self):
        return self.board.policies.shuffle_counter


class Game(StateMachine):
    class SettingUp(State):
        @staticmethod
        def run(game):
            #game.setup_board
            game.distribute_roles()
            #game.setup_gamestate
            game.opening_sequence()

        @staticmethod
        def next(game):
            return Game.AssigningPresident


    class AssigningPresident(State):
        @staticmethod
        def run(game):
            game.pass_presidency()

        @staticmethod
        def next(game):
            return Game.ElectingGovernment


    class ElectingGovernment(State):
        @staticmethod
        def run(game):
            game.nominate_chancellor()
            game.vote_on_the_government()
            if game.stats.current_president is None:
                return
            if game.stats.is_chancellor_asked_if_hitler:
                game.ask_chancellor_if_hitler()

        @staticmethod
        def next(game):
            if game.stats.current_president is None:
                return Game.AdvancingElectionTracker
            if game.stats.wincon is HitlerElectedWinCondition():
                return Game.AnnouncingWinners
            else:
                return Game.PassingLegislation


    class PassingLegislation(State):
        @staticmethod
        def run(game):
            game.legislative_session()

        @staticmethod
        def next(game):
            if game.enacted_policy is None:
                # Must have been a Veto
                return Game.AdvancingElectionTracker
            else:
                return Game.EnactingPolicy


    class AdvancingElectionTracker(State):
        @staticmethod
        def run(game):
            game.advance_election_tracker()

        @staticmethod
        def next(game):
            if game.stats.election_tracker == 3:
                return Game.EnactingPolicy
            else:
                return Game.AssigningPresident


    class EnactingPolicy(State):
        @staticmethod
        def run(game):
            game.enact_policy()
            game.check_policy_tracks()
            game.executive_action()

        @staticmethod
        def next(game):
            if game.stats.wincon in (FascistPolicyWinCondition(), LiberalPolicyWinCondition(), HitlerKilledWinCondition()):
                return Game.AnnouncingWinners
            elif game.stats.current_president is None:
                # CHAOS
                return Game.AssigningPresident
            elif game.stats.current_president is not game.stats.presidential_candidate:
                # The current president chose a new candidate: surprise elections!
                return Game.ElectingGovernment
            else:
                return Game.AssigningPresident


    class AnnouncingWinners(State):
        @staticmethod
        def run(game):
            game.announce_winners()

        @staticmethod
        def next(game):
            # End statemachine
            return


    def __init__(self, players, announce=print):
        """Accept an announce method and a list of Player objects
        """
        self.players = list(players)
        self.announce = announce
        # Choose board and roles based on number of players
        based_on_players = {5:     (SmallGameBoard, [Hitler()] + [Fascist()] * 1 + [Liberal()] * 3),
                            6:     (SmallGameBoard, [Hitler()] + [Fascist()] * 1 + [Liberal()] * 4),
                            7:     (MediumGameBoard, [Hitler()] + [Fascist()] * 2 + [Liberal()] * 4),
                            8:     (MediumGameBoard, [Hitler()] + [Fascist()] * 2 + [Liberal()] * 5),
                            9:     (LargeGameBoard, [Hitler()] + [Fascist()] * 3 + [Liberal()] * 5),
                            10:    (LargeGameBoard, [Hitler()] + [Fascist()] * 3 + [Liberal()] * 6)}
        try :
            self.board, self.roles = based_on_players[len(players)]
        except KeyError:
            raise KeyError("Invalid number of players: {}".format(len(players)))
        # Other preparations
        self.board = self.board()
        random.shuffle(self.players)
        random.shuffle(self.roles)
        self.stats = Statistics(self.board, self.players, self.roles)
        self.player_rotation = itertools.cycle(self.players)
        # Statemachine setup
        super(Game, self).__init__(Game.SettingUp)

    def play(self):
        """Activate the statemachine template method
        """
        self.announce("Let's begin.")
        self.run_all()

    def distribute_roles(self):
        for player, role in zip(self.players, self.roles):
            player.setup(self.stats, role)

    def opening_sequence(self):
        should_hitler_know_teammates = 5 <= len(self.players) <= 6
        for player in self.players:
            if isinstance(player.role, Fascist):
                # Hitler himself does not know his teammates unless this is a 5- or 6-player game
                if player.role is Hitler() and not should_hitler_know_teammates:
                    continue
                player.find_out_teammates()
        self.announce("Fascists, look in PM for your allies.")
        self.announce("You too, Hitler!" if should_hitler_know_teammates else "Hitler, YOU don't get a PM. Good luck.")

    def pass_presidency(self):
        self.stats.presidential_candidate = next(self.player_rotation)
        while self.stats.presidential_candidate not in self.players:
            # Can't remove dead players from the cycle(), so we do this instead
            self.stats.presidential_candidate = next(self.player_rotation)

    def nominate_chancellor(self):
        self.announce("The presidential candidate is {}. Who do you nominate as chancellor?".format(self.stats.presidential_candidate.name))
        self.stats.nominated_chancellor = self.stats.presidential_candidate.nominate_chancellor()
        if self.stats.nominated_chancellor is self.stats.presidential_candidate:
            raise ValueError("The president can't elect themselves!")
        if self.stats.nominated_chancellor in (self.stats.previous_president, self.stats.previous_chancellor):
            raise ValueError("Can't elect as chancellor the previous president/chancellor")
        self.announce("President {} nominated {} to be chancellor.".format(self.stats.presidential_candidate.name, self.stats.nominated_chancellor.name))
        self.stats.nominations.append((self.stats.presidential_candidate, self.stats.nominated_chancellor))

    def vote_on_the_government(self):
        """Returns true if a government was elected
        """
        self.announce("President {}, Chancellor {}. Ja or Nein?".format(self.stats.presidential_candidate.name, self.stats.nominated_chancellor.name))
        votes = []
        for player in self.players:
            vote = player.vote()
            self.announce("{}: {}".format(player.name, "Ja" if vote is Ja() else "Nein"))
            votes.append(vote)
        self.announce("The results are in!")
        self.announce("Ja: {}, Nein: {}".format(votes.count(Ja()), votes.count(Nein())))
        if votes.count(Ja()) > votes.count(Nein()):
            self.stats.current_president = self.stats.presidential_candidate
            self.stats.current_chancellor = self.stats.nominated_chancellor
            # Keep the president & chancellor who were last elected for eligibility reasons
            self.stats.previous_president = self.stats.current_president
            self.stats.previous_chancellor = self.stats.current_chancellor
        else:
            self.stats.current_president = None

    def ask_chancellor_if_hitler(self):
        self.announce("{}, are you Hitler?".format(self.stats.current_chancellor.name))
        self.announce("...")
        if self.stats.current_chancellor.role is Hitler():
            self.announce("{} is Hitler!".format(self.stats.current_chancellor.name))
            self.stats.wincon = HitlerElectedWinCondition()
        else:
            self.announce("{} is not Hitler. Phew.".format(self.stats.current_chancellor.name))

    def legislative_session(self):
        # Pass three policies to the president
        policies = self.board.draw_policies(3)
        policy = self.stats.current_president.choose_policies_for_chancellor(policies)
        # Discard the president's choice and keep the rest
        self.board.discard_policy(policy)
        policies.remove(policy)
        # Pass the two policies to the chancellor, and maybe offer a veto
        while True:
            policy = self.stats.current_chancellor.enact_policy(policies)
            if policy is VetoPolicy():
                if not self.stats.is_veto_enabled:
                    raise ValueError("Can't veto yet!!")
                # Will the president veto as well?
                self.announce("Chancellor requests to veto legislasion. Waiting for president...")
                response = self.stats.current_president.accept_veto()
                if response is Ja():
                    # VETO! Discard the remaining policy
                    self.announce("President agrees to veto. All policies discarded.")
                    self.board.discard_policy(policies.pop())
                    self.board.discard_policy(policies.pop())
                    policy = VetoPolicy() # Bug-proof
                    break
                else:
                    self.announce("President rejects veto!")
            else:
                # Discard a policy chosen by the chancellor and enact the remaining policy
                self.board.discard_policy(policy)
                policies.remove(policy)
                policy = policies.pop()
                break
        self.enacted_policy = policy
        self.stats.legislative_session_records.append((self.stats.current_president, self.stats.current_chancellor, self.enacted_policy))

    def advance_election_tracker(self):
        self.announce("Advancing election tracker...")
        self.stats.election_tracker += 1
        if self.stats.election_tracker == 3:
            self.announce("Chaos! The first policy in the deck will be enacted.")
            self.stats.previous_president = None
            self.stats.previous_chancellor = None
            (self.enacted_policy,) = self.board.draw_policies(1)

    def enact_policy(self):
        self.board.place_policy(self.enacted_policy)
        number_of_policies = self.stats.fascist_policies if self.enacted_policy is FascistPolicy() else self.stats.liberal_policies
        self.announce("Policy on the board: {type} #{number}".format(type=self.enacted_policy, number=number_of_policies))
        self.stats.election_tracker = 0

    def check_policy_tracks(self):
        if self.stats.fascist_slots_remaining == 0:
            self.stats.wincon = FascistPolicyWinCondition()
        elif self.stats.liberal_slots_remaining == 0:
            self.stats.wincon = LiberalPolicyWinCondition()

    def executive_action(self):
        president = self.stats.current_president
        #power = self.stats.current_presidential_power if self.enacted_policy is Fascist() else NoPower()
        if self.enacted_policy is FascistPolicy():
            power = self.stats.current_presidential_power
        else:
            power = NoPower()
        if power is NoPower():
            return
        elif power is ExamineCardsPower():
            policies = self.board.peek_policies(3)
            self.announce("{} uses Policy Peek to look at the top three tiles in the policy deck.".format(president.name))
            self.stats.current_president.examine_top_policies(policies)
        elif power is InvestigativePower():
            target = self.stats.current_president.investigate_player()
            if target in self.stats.past_investigations:
                raise ValueError("Can't investigate the same player twice in the same game.")
            self.announce("{} uses Investigate Loyalty to check the Party Membership card of {}!".format(president.name, target.name))
            self.stats.past_investigations.append(target)
        elif power is SurpriseElectionPower():
            target = self.stats.current_president.pick_next_president()
            if target is president:
                raise ValueError("Can't name yourself as the next president!")
            self.announce("{} uses Call Special Election to choose {} as the next presidential candidate!".format(president.name, target.name))
            self.stats.presidential_candidate = target
        elif power is KillPower():
            target = self.stats.current_president.kill_player()
            self.announce("{} uses Execution to kill {}!".format(president.name, target.name))
            self.announce("{}, are you Hitler?".format(target.name))
            self.announce("...")
            if target.role is Hitler():
                self.announce("{} is Hitler! Die, Hitler!".format(target.name))
                self.stats.wincon = HitlerKilledWinCondition()
            else:
                self.announce("{} is not Hitler. {} died!".format(target.name, target.name))
                self.players.remove(target)
        else:
            raise ValueError("Got a bad presidential power object from the board!")

    def announce_winners(self):
        if isinstance(self.stats.wincon, FascistWinCondition):
            self.announce("The fascists win! They were:")
            for player in (player for player in self.players if isinstance(player.role, Fascist)):
                self.announce("{}: {}".format(player.name, player.role))
            self.announce("Thanks for playing!")
        elif isinstance(self.stats.wincon, LiberalWinCondition):
            self.announce("The liberals win! They were:")
            for player in (player for player in self.players if isinstance(player.role, Liberal)):
                self.announce("{}: {}".format(player.name, player.role))
            self.announce("Thanks for playing!")
