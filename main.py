from game import Game


def black_jack(decks, players):
    game = Game()
    game.start_game(decks, players)


if __name__ == '__main__':
    black_jack(6, 2)


