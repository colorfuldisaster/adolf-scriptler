import discord
import asyncio
import secrethitler

client = discord.Client()

from .commands import *

@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.is_private:
        on_personal_message(message)
    else:
        on_channel_message(message)

def on_personal_message(message):
    # TODO
    #connections_with_author = [game for game in list_of_games if message.author in [name for name in game.players]]
    #for connection in connections_with_author:
    #    pass
    pass

def on_channel_message(message):
    if client.user.mentioned_in(message):
        #print("Hi {user}!".format(user=message.author))
        # Treat all highlights as commands for the bot
        execute_channel_command(message)

def start_client(token):
    client.run(token)
