from shoe import Shoe
from bank import Bank
from cards_map import CardMap
import time


class Game:
    DEALER = 'Dealer'
    PLAYERS = 'Player'

    def __init__(self):
        self.shoe = Shoe()
        self.bank = Bank()
        self.cards = {}
        self.count = 0
        self.hands = {}
        self.hand_values = {}

    def start_game(self, decks, players):
        self.shoe.fill_shoe(decks)
        card_map = CardMap()
        self.cards = card_map.get_map()
        self.bank.construct_bank(players)
        while self.shoe.shoe:
            for player in range(players):
                player = 'Player' + str(player + 1)
                bet = input(player + ', how much would you like to bet?  ')
                self.bank.place_bets(player, int(bet))
            self.deal_player_hands(players)
            hands = self.hands

            for player, hand in hands.items():
                if player == self.DEALER:
                    print(player, [hand[0], '?'])
                else:
                    print(player, hand)

            self.do_actions()

            should_show_count = input('Do you want to check the count?  Y/N  ')
            if should_show_count == 'Y':
                print("The Count is:  ", self.get_count())

            time.sleep(3)

        print("Shoe is out of cards. Let's fill it up again")

    def deal_player_hands(self, players):
        self.hands.clear()
        hands = self.hands
        r = 2
        while r > 0:
            if not self.shoe.shoe:
                break
            r -= 1
            for player in range(players):
                if not self.shoe.shoe:
                    break
                card = self.shoe.deal_card()
                self.set_count(card)
                if hands.get(self.PLAYERS + str(player + 1)):
                    hands[self.PLAYERS + str(player + 1)].append(self.cards.get(card))
                else:
                    hands[self.PLAYERS + str(player + 1)] = [self.cards.get(card)]
            if self.shoe.shoe:
                card = self.shoe.deal_card()
                self.set_count(card)
                if hands.get(self.DEALER):
                    hands[self.DEALER].append(self.cards.get(card))
                else:
                    hands[self.DEALER] = [self.cards.get(card)]

        return hands

    def do_actions(self):
        self.hand_values.clear()
        players_values = []
        for player, hand in self.hands.items():
            if player == self.DEALER:
                self.resolve_dealer_hand()
            else:
                while True:
                    action = input(player + ': 0 to hit or 1 to stand  ')
                    if action == '0':
                        self.hit(player)
                        continue
                    if action == '1':
                        value = self.evaluate_hand(self.hands.get(player))
                        if player != self.DEALER:
                            players_values.append((player, value))
                        self.hand_values[self.PLAYERS] = players_values
                        break

        self.get_winners()

    def hit(self, player):
        card = self.shoe.deal_card()
        self.set_count(card)
        self.hands[player].append(self.cards.get(card))
        print(self.hands.get(player))

    def resolve_dealer_hand(self):
        value = self.evaluate_hand(self.hands.get(self.DEALER))
        while value < 17:
            self.hit(self.DEALER)
            value = self.evaluate_hand(self.hands.get(self.DEALER))
            time.sleep(1)
        self.hand_values[self.DEALER] = value
        print(self.hands.get(self.DEALER))

    def evaluate_hand(self, hand):
        values = set()
        best_hand = -1

        def get_all_possible_hand_values(i, total):
            if i >= len(hand):
                values.add(total)
                return
            if hand[i] == 'A':
                get_all_possible_hand_values(i+1, total + 1)
                get_all_possible_hand_values(i+1, total + 11)
            elif hand[i] == 'J' or hand[i] == 'Q' or hand[i] == 'K':
                total += 10
                get_all_possible_hand_values(i+1, total)
            else:
                total += int(hand[i])
                get_all_possible_hand_values(i+1, total)
            return

        get_all_possible_hand_values(0,0)

        for value in values:
            if value <= 21:
                best_hand = max(best_hand, value)
            else:
                continue

        return best_hand

    def get_winners(self):
        winners = []
        dealer = self.hand_values.get(self.DEALER)
        for player, value in self.hand_values.get(self.PLAYERS):
            if dealer <= value <= 21:
                winners.append(player)

        print(winners)
        self.bank.resolve_bets(winners)

    def set_count(self, card):
        if card < 5:
            self.count += 1
        elif card > 7:
            self.count -= 1
        return

    def get_count(self):
        return self.count

