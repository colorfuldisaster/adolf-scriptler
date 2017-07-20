from .policies import *
from .votes import *
from .roles import *

class HumanPlayer(object):
    """Implements UI for PvP gameplay
    """
    def __init__(self, name, input=input, output=print):
        self.name = name
        self.input = input
        self.output = output

    def identify_policy_from_input(self, user_input):
        user_input = user_input.lower()
        completes_to = lambda word: (word[:i + 1] for i in range(len(word)))
        if user_input in completes_to("fascist"):
            return FascistPolicy()
        elif user_input in completes_to("liberal"):
            return LiberalPolicy()
        elif user_input in completes_to("veto"):
            return VetoPolicy()
        else:
            return None

    def identify_vote_from_input(self, user_input):
        user_input = user_input.lower()
        completes_to = lambda word: (word[:i + 1] for i in range(len(word)))
        if user_input in completes_to("ja"):
            return Ja()
        elif user_input in completes_to("yea"):
            return Ja()
        elif user_input in completes_to("yes"):
            return Ja()
        elif user_input in completes_to("nein"):
            return Nein()
        elif user_input in completes_to("no"):
            return Nein()
        else:
            return None

    def setup(self, stats, role):
        self.stats = stats
        self.role = role
        self.output("Your role: {}".format(role))

    def find_out_teammates(self):
        fascists = [player for player in self.stats.players if isinstance(player.role, Fascist)]
        self.output("These are your allies:")
        for fascist in fascists:
            self.output("{}: {}".format(fascist.name, fascist.role))

    def nominate_chancellor(self):
        while True:
            self.output("Nominate a chancellor!")
            choice = self.input()
            chosen_player = next((player for player in self.stats.players if player.name == choice), None)
            if chosen_player is None:
                self.output("Invalid player name.")
            elif chosen_player is self:
                self.output("You can't nominate yourself!")
            elif chosen_player is self.stats.previous_president:
                self.output("{} was the previous president. Choose someone else.".format(chosen_player.name))
            elif chosen_player is self.stats.previous_chancellor:
                self.output("{} was the previous chancellor. Choose someone else.".format(chosen_player.name))
            else:
                return chosen_player

    def vote(self):
        while True:
            vote = self.input()
            vote = self.identify_vote_from_input(vote)
            if vote is Ja() or vote is Nein():
                return vote
            self.output("Invalid vote. Vote <Ja> or <Nein>.")

    def choose_policies_for_chancellor(self, policies):
        self.output("Your draw: {} {} {}".format(*policies))
        while True:
            self.output("Choose a policy to discard. <Fascist/Liberal>")
            choice = self.input()
            policy = self.identify_policy_from_input(choice)
            if policy in policies:
                return policy
            self.output("Invalid or illegal policy to discard.")

    def accept_veto(self):
        self.output("The chancellor has requested to veto these policies. Will you accept? <Ja>/<Nein>")
        while True:
            vote = self.input()
            vote = self.identify_vote_from_input(vote)
            if vote is Ja() or vote is Nein():
                return vote
            self.output("Invalid vote. Vote <Ja> or <Nein>.")

    def enact_policy(self, policies):
        self.output("The president passes you these policies: {} {}".format(*policies))
        while True:
            self.output("Choose a policy to discard. The other will be enacted. <Fascist/Liberal>{}".format("... or veto the legislation. <Veto>" if self.stats.is_veto_enabled else ""))
            choice = self.input()
            policy = self.identify_policy_from_input(choice)
            if self.stats.is_veto_enabled and policy is VetoPolicy():
                return policy
            if policy in policies:
                return policy
            self.output("Invalid or illegal policy to enact.")

    def examine_top_policies(self, policies):
        self.output("Peeked at the policy deck...")
        self.output("These are the next three policies:")
        for i, policy in enumerate(policies):
            self.output("{}) {}".format(i + 1, "Fascist" if policy is FascistPolicy() else "Liberal"))

    def investigate_player(self):
        self.output("You may now investigate another player and find out their party membership.")
        self.output("Who will you choose?")
        while True:
            name = self.input()
            target = next((player for player in self.stats.players if name == player.name), None)
            if target is None:
                self.output("Invaild player name.")
                continue
            if target.name in self.stats.past_investigations:
                self.output("Can't investigate a player who has already been investigated in the same game.")
                continue
            party = "Fascist" if target.role is Fascist() else "Liberal"
            self.output("Investigated {} and found their party membership: {}".format(target.name, party))
            return target

    def pick_next_president(self):
        self.output("You may now pick another player to be the next presidential candidate.")
        self.output("Who will you choose?")
        while True:
            name = self.input()
            target = next((player for player in self.stats.players if name == player.name), None)
            if target is None:
                self.output("Invaild player name.")
                continue
            if target is self:
                self.output("Can't nominate yourself!")
            return target


    def kill_player(self):
        self.output("You may now pick another player to be executed.")
        self.output("Who will you choose?")
        while True:
            name = self.input()
            target = next((player for player in self.stats.players if name == player.name), None)
            if target is None:
                self.output("Invaild player name.")
                continue
            if target is self:
                self.output("Nice try.")
            return target


class Player(object):
    """Players need to make informed decisions based on gameplay -
    see who's the nominated chancellor / president
    who's the current chancellor / president
    the state of the policies
    the state of the election tracker
    public knowledge such as who inspected who
    and so on..
    Knowing this, the game module stores game statistics for the player module's perusal
    """
    def __init__(self, name):
        raise NotImplementedError("Abstract class")

    def setup(self, stats, role):
        """Force player to store stats and role
        """
        raise NotImplementedError("Player must implement method to get stats & role from game module")

    def find_out_teammates(self):
        """As a fascist, learn who's Hilter & the other fascists at the start of the game
        In 5-6 player games, this method is also called for Hitler himself
        """
        raise NotImplementedError("Player must implement method to tell who are the other fascists")

    def nominate_chancellor(self):
        """As president, nominate a chancellor for government vote
        """
        raise NotImplementedError("Player must implement method to nominate chancellor as president")

    def vote(self):
        """Vote Ja or Nein for elections
        """
        raise NotImplementedError("Player must implement method to vote")

    def choose_policies_for_chancellor(self, policies):
        """As president, decide which policies to pass to the chancellor
        """
        raise NotImplementedError("Player must implement method to pass policies to chancellor as president")

    def accept_veto(self):
        """As president, accept or deny the chancellor's reqeust to veto the legislation
        """
        raise NotImplementedError("Player must implement method to accept or reject veto as president")

    def enact_policy(self, policies):
        """As chancellor, decide which policy to discard out of the ones given to you
        """
        raise NotImplementedError("Player must implement method to enact policy as chancellor")

    def examine_top_policies(self, policies):
        """As president, examine the top three policies in the policy deck and return them in order
        """
        raise NotImplementedError("Implement Policy Peek handler")

    def investigate_player(self):
        """As president, investigate a player and find out their party membership card
        """
        raise NotImplementedError("Implement Investigate Loyalty handler")

    def pick_next_president(self):
        """As president, pick the presidential candidate for the next round of legislation
        """
        raise NotImplementedError("Implement Call Special Election handler")

    def kill_player(self):
        """As president, kill a player and remove them from the game
        """
        raise NotImplementedError("Implement Execution handler")
