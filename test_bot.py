import bot

import argparse

if __name__ == "__main__":
    # Argparse stuff
    parser = argparse.ArgumentParser()
    parser.add_argument("token", help="The OAuth2 token for our discord bot")
    args = praser.parse_args()
    # Run client
    bot.start_client(args.token)
