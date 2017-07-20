import secrethitler

def main():
    players = []
    players.append(secrethitler.HumanPlayer("Tom"))
    players.append(secrethitler.HumanPlayer("Jerry"))
    players.append(secrethitler.HumanPlayer("Bob"))
    players.append(secrethitler.HumanPlayer("Harry"))
    players.append(secrethitler.HumanPlayer("Josh"))
    game = secrethitler.Game(players)
    game.play()

if __name__ == "__main__":
    main()
