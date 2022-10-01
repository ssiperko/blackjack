class Bank:
    DEALER = 'Dealer'

    def __init__(self):
        self.bank = {self.DEALER: 100000}
        self.bets = {}

    def construct_bank(self, players):
        try:
            for player in range(players):
                self.bank['Player' + str(player + 1)] = 20000
        except:
            raise Exception('Error occured while constructing bank')

    def place_bets(self, player, bet):
        try:
            if self.bank.get(player) >= bet:
                if self.bets.get(player):
                    player = player + '-2'
                self.bets[player] = bet
                self.bank[player] = self.bank.get(player) - bet
            else:
                return 'Sorry, you dont have enough money to for that bet'
        except:
            raise Exception("Bet could not be placed, please try again")

    def resolve_bets(self, winners):
        for winner in winners:
            if self.bets.get(winner):
                bet = self.bets.get(winner)
                self.bank[self.DEALER] = self.bank.get(self.DEALER) - bet
                self.bank[winner] = self.bank.get(winner) + (bet * 2)
                self.bets.pop(winner)

        pot = 0
        for loser, bet in self.bets.items():
            pot += bet
        self.bets.clear()

        self.bank[self.DEALER] = self.bank.get(self.DEALER) + pot

        print(self.bank, '  This is the bank')
        print(self.bets, ' These are the bets')


        
