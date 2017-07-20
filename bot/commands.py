import functools
import asyncio

from .discord_interface import client
import secrethitler

"""Define channel commands
"""

class ChannelCommand(object):
    """An easy way to define command types and what each one does
    """
    @staticmethod
    def execute(channel):
        raise NotImplementedError("Abstract class")


class ParseFail(ChannelCommand):
    @staticmethod
    def execute(channel):
        client.send_message(channel, "No such command.")


class PrintHelp(ChannelCommand):
    @staticmethod
    def execute(channel):
        client.send_message(channel, "List of commands:")
        client.send_message(channel, "start hitler: start a game of secret hitler")


class RunSecretHitler(ChannelCommand):
    game_channels = []
    # Time between each "join" message when starting a game
    signup_timeout = 60

    @staticmethod
    def is_signup_message(message):
        # The command's only word is "join" (ignore case)
        return message.content.replace(client.user.mention, "").strip().lower() == "join"

    @staticmethod
    def execute(channel):
        def announce(message):
            client.send_message(channel, "{message}".format(message=message))
        if channel in RunSecretHitler.game_channels:
            announce("Can't create a game when there's a game on this channel already.")
            return
        RunSecretHitler.game_channels.append(channel)
        # Receive all signups (until timeout or until 10 players sign up)
        announce("A game of Secret Hitler (5-10 players) has started!")
        announce("Mention me with \"join\" to join the game. (timeout between signups is {ts}s)".format(ts=RunSecretHitler.signup_timeout))
        players = []
        return
        while len(players) < 10:
            message = asyncio.wait_for(asyncio.ensure_future(client.wait_for_message(check=RunSecretHitler.is_signup_message)), None)
            if message is None:
                # Timeout
                break
            # Setup player I/O via private messages (message.author)
            def player_input():
                return asyncio.wait_for(asyncio.ensure_future(client.wait_for_message(author=message.author)), None)
            def player_output(text):
                client.send_message(message.author, text)
            players.append(secrethitler.HumanPlayer(message.author, input=player_input, output=player_output))
        # Start the game
        if len(players) < 5:
            announce("Can't start the game with less than 5 players...")
            RunSecretHitler.game_channels.remove(channel)
            return
        game = secrethitler.Game(players, announce=announce)
        games.setdefault(channel, []).append(game)
        game.play()


"""Logic from parsing to execution
"""
def execute_channel_command(message):
    command = parse_channel_command(message.content)
    command.execute(message.channel)

def parse_channel_command(content):
    if "start hitler" in content.lower():
        return RunSecretHitler
    elif "help" in content.lower():
        return PrintHelp
    else:
        return ParseFail
