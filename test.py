from secrethitler import *

def main():
    players = HumanPlayer("Tom"), HumanPlayer("Jerry"), HumanPlayer("Bob"), HumanPlayer("Harry"), HumanPlayer("Josh")
    game = Game(players)
    game.play()

if __name__ == "__main__":
    main()
