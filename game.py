from board import *
from wincon import *

class Game(object):
    def __init__(self):
        self.previous_president = None
        self.previous_chancellor = None
        # TODO
        self.player_rotation = itertools.cycle(players)

    def play(self):
        """Main game flow loop
        """
        try:
            while True:
                self.pass_presidency()
                self.nominate_chancellor()
                self.vote_on_the_government()
                self.legislative_session()
                self.executive_action()
        except Wincon as wc:
            pass

    def pass_presidency(self):
        self.presidential_candidate = self.player_rotation.next()

    def nominate_chancellor(self):
        while True:
            self.presidential_candidate.message("Nominate a chancellor!")
            choice = self.presidential_candidate.receive()
            chosen_player = next((player for player in self.players if player.name == choice), None)
            if chosen_player is not None:
                break
            else:
                self.presidential_candidate.message("Invalid player name...")
        self.nominated_chancellor = chosen_player

    def vote_on_the_government(self):
        # TODO
        # Keep the president & chancellor who were last elected for eligibility reasons
        self.previous_president = self.current_president
        self.previous_chancellor = self.current_chancellor

    def legislative_session(self):
        policies = self.board.draw_policies(3)
        # Pass three policies to the president
        self.current_president.message("Your draw: {} {} {}".format(*policies))
        self.current_president.message("Choose a policy to discard.")
        choice = self.current_president.receive()
        policy = FascistPolicy() if choice == "Fascist" else LiberalPolicy()
        # Discard the president's choice and keep the rest
        self.board.discard_policy(policy)
        policies.remove(policy)
        # Pass the two policies to the chancellor, and maybe offer a veto
        self.current_chancellor.message("The president passes you these policies: {} {}".format(*policies))
        self.current_chancellor.message("Choose a policy to enact{}.".format("... or veto the legislation" if self.board.is_veto_enabled() else ""))
        choice = self.current_chancellor.receive()
        if choice == "Veto":
            # Discard the remaining two policies
            self.board.discard_policy(policies.pop())
            self.board.discard_policy(policies.pop())
            self.board.advance_election_tracker()
        else:
            # Discard the remaining policy and enact the one chosen by the chancellor
            policy = FascistPolicy() if choice == "Fascist" else LiberalPolicy()
            policies.remove(policy)
            self.board.discard_policy(policies.pop())
            self.board.place_policy(policy)

    def executive_action(self):
        if self.board.new_executive_action is not None:
            self.board.new_executive_action(self.current_president)
        # Reset the executive action in case next round of legislation doesn't place a policy at all
        self.board.new_executive_action = None
