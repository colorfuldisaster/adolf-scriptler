from policies import *
from votes import *

class HumanPlayer(object):
    """Implements UI for PvP gameplay
    """
    def __init__(self, name):
        self.name = name

    def input(self):
        """Implement user input
        """
        pass

    def output(self):
        """Implement user output
        """
        pass

    def identify_policy_from_input(self, user_input):
        user_input = lower(user_input)
        completes_to = lambda word: (word[:] for i in range(len(word))))
        if user_input in completes_to("fascist"):
            return FascistPolicy()
        elif user_input in completes_to("liberal"):
            return LiberalPolicy()
        elif user_input in completes_to("veto"):
            return VetoPolicy()
        else:
            return None

    def identify_vote_from_input(self, user_input):
        user_input = lower(user_input)
        completes_to = lambda word: (word[:] for i in range(len(word))))
        if user_input in completes_to("ja"):
            return Ja()
        elif user_input in completes_to("yea"):
            return Ja()
        elif user_input in completes_to("yes"):
            return Ja()
        elif user_input in completes_to("nein"):
            return Nein()
        elif user_input in completes_to_("no"):
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
            chosen_player = next((player for player in self.players if player.name == choice), None)
            if chosen_player is not None:
                return chosen_player
            self.input("Invalid player name.")

    def vote(self):
        while True:
            vote = self.input()
            if vote is Ja() or vote is Nein():
                return self.identify_vote_from_input(vote)
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

    def enact_policy(self, policies):
        self.output("The president passes you these policies: {} {}".format(*policies))
        while True:
            self.output("Choose a policy to enact. <Fascist/Liberal>{}".format("... or veto the legislation. <Veto>" if self.stats.is_veto_enabled else ""))
            choice = self.input()
            policy = self.identify_policy_from_input(choice)
            if self.stats.is_veto_enabled and policy is VetoPolicy():
                return policy
            if policy in policies:
                return policy
            self.output("Invalid or illegal policy to enact.")


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

    def enact_policy(self, policies):
        """As chancellor, decide which policy to enact out of the ones given to you
        """
        raise NotImplementedError("Player must implement method to enact policy as chancellor")
