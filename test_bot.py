import bot

import argparse

TOKEN = "MzEwNDQ2MzQxNDEzNDA0Njgy.DFKYJQ.TuaiytHVFq7cfVLA_50bLbZeXxo"

if __name__ == "__main__":
    # Argparse stuff
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", dest="token", help="The OAuth2 token for our discord bot", default=TOKEN)
    args = parser.parse_args()
    # Run client
    bot.start_client(args.token)
