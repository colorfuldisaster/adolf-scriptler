import discord
import asyncio
import secrethitler

from commands import *

client = discord.Client()

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

    if isinstance(message.author, User):
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
        # Treat all highlights as commands for the bot
        on_channel_command(message)

def start_client(token):
    client.run(args.token)
