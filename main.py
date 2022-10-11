from game import Game
from shoe import Shoe
from bank import Bank
from cards_map import CardMap


def black_jack(decks, players):
    shoe = Shoe()
    bank = Bank()
    card_map = CardMap()
    game = Game(shoe, bank, card_map)
    game.start_game(decks, players)


if __name__ == '__main__':
    black_jack(6, 2)


