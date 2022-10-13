from bank import Bank
from shoe import Shoe
from cards_map import CardMap
import time


class Game:
    DEALER = 'Dealer'
    PLAYERS = 'Player'

    def __init__(self, shoe: Shoe, bank: Bank, card_map: CardMap) -> None:
        if shoe is None:
            raise ValueError("shoe must be injected")
        if bank is None:
            raise ValueError("bank must be injected")
        if card_map is None:
            raise ValueError("card map must be injected")
        self.shoe = shoe
        self.bank = bank
        self.card_map = card_map

        self.count = 0
        self.cards = {}
        self.hands = {}
        self.hand_values = {}

    def start_game(self, decks: int, players: int) -> None:
        self.shoe.fill_shoe(decks)
        self.cards = self.card_map.get_map()
        self.bank.construct_bank(players)
        while self.shoe.shoe:
            p = 0
            while p < players:
                player = 'Player' + str(p + 1)
                bet = input(player + ', how much would you like to bet?  ')
                can_bet = self.bank.place_bets(player, int(bet))
                if can_bet:
                    print('nice bet')
                    p += 1
                else:
                    print('Sorry, you dont have enough money')

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

    def deal_player_hands(self, players: int) -> dict:
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

    def do_actions(self) -> None:
        self.hand_values.clear()
        players_values = []
        for player, hand in self.hands.items():
            if player == self.DEALER:
                self.resolve_dealer_hand()
            else:
                while True:
                    action = input(player + ': 0 to hit, 1 to stand, 2 to double down  ')
                    if action == '0':
                        self.hit(player)
                        continue
                    if action == '1':
                        evaluated_hand = self.evaluate_hand(self.hands.get(player))
                        value = evaluated_hand[0]
                        is_blackjack = evaluated_hand[1]
                        if player != self.DEALER:
                            players_values.append((player, value, is_blackjack))
                        self.hand_values[self.PLAYERS] = players_values
                        break
                    if action == '2':
                        evaluated_hand = self.evaluate_hand(self.hands.get(player))
                        value = evaluated_hand[0]
                        if value <= 11:
                            self.bank.double_down(player)
                            self.hit(player)
                            evaluated_hand = self.evaluate_hand(self.hands.get(player))
                            value = evaluated_hand[0]
                            is_blackjack = evaluated_hand[1]
                            if player != self.DEALER:
                                players_values.append((player, value, is_blackjack))
                            self.hand_values[self.PLAYERS] = players_values
                            break
                        else:
                            print('Sorry, you can only double down if card value is 11 or below.')
                            continue

        self.get_winners()

    def hit(self, player: str) -> None:
        card = self.shoe.deal_card()
        self.set_count(card)
        self.hands[player].append(self.cards.get(card))
        print(self.hands.get(player))

    def resolve_dealer_hand(self) -> None:
        evaluated_hand = self.evaluate_hand(self.hands.get(self.DEALER))
        value = evaluated_hand[0]
        if value > 21 or value == -1:
            self.hand_values[self.DEALER] = -1
            return
        while value < 17:
            self.hit(self.DEALER)
            evaluated_hand = self.evaluate_hand(self.hands.get(self.DEALER))
            value = evaluated_hand[0]
            if value > 21 or value == -1:
                self.hand_values[self.DEALER] = -1
                return
            print(self.hands.get(self.DEALER))
        self.hand_values[self.DEALER] = value
        print(self.hands.get(self.DEALER))

    def evaluate_hand(self, hand: list) -> list:
        blackjacks = set()
        blackjacks.add(('A', 10))
        blackjacks.add(('A', 'J'))
        blackjacks.add(('A', 'Q'))
        blackjacks.add(('A', 'K'))

        if len(hand) == 2:
            faces = tuple(hand)
            if faces in blackjacks:
                return [21, True]

        values = set()
        best_hand = -1

        """This method recursively builds all possible combinations of hands.
        This is necessary because Aces can have two values and we need to find the best hand of
        the available possibilities"""
        def get_all_possible_hand_values(i: int, total: int):
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

        return [best_hand, False]

    def get_winners(self) -> None:
        blackjacks = []
        winners = []
        draws = []
        dealer = self.hand_values.get(self.DEALER)
        for player, value, is_blackjack in self.hand_values.get(self.PLAYERS):

            if value > 21 or (dealer == -1 and value == -1):
                continue
            if value <= 21:
                if is_blackjack and dealer != 21:
                    blackjacks.append(player)
                    continue
                if dealer < value:
                    winners.append(player)
                elif value == dealer:
                    draws.append(player)

        print(winners, 'winners')
        print(draws, 'draws')
        print(blackjacks, 'blackjacks')
        self.bank.resolve_bets(winners, draws, blackjacks)

    def set_count(self, card: int) -> None:
        if card < 5:
            self.count += 1
        elif card > 7:
            self.count -= 1
        return

    def get_count(self) -> int:
        return self.count

