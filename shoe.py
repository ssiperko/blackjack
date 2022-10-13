"""This class constructs a shoe of X decks of cards"""
import random


class Shoe:
    def __init__(self):
        self.shoe = {}
        self.card = None

    # fills the shoe with x deck of cards
    def fill_shoe(self, decks: int) -> dict:
        for i in range(13):
            self.shoe[i] = 4 * decks
        return self.shoe

    # randomly picks a card from the shoe and decrements it's value
    def deal_card(self) -> int:
        while True:
            self.card = random.randrange(13)
            if self.shoe.get(self.card):
                self.shoe[self.card] -= 1
                if self.shoe.get(self.card) <= 0:
                    self.shoe.pop(self.card)
                break
            else:
                continue
        return self.card

