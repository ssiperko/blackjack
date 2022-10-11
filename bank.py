class Bank:
    DEALER = 'Dealer'

    def __init__(self):
        self.bank = {self.DEALER: 100000}
        self.bets = {}


    """creates the bank, adds an account for each player and provides them a default amount of money"""
    def construct_bank(self, players):
        try:
            for player in range(players):
                self.bank['Player' + str(player + 1)] = 20000
        except:
            raise Exception('Error occurred while constructing bank')

    """Removes the amount of money wagered by each player from their account and placed it in temp structure for remained or hand"""
    def place_bets(self, player, bet):
        try:
            if self.bank.get(player) >= bet:
                if self.bets.get(player):
                    player = player + '-2'
                self.bets[player] = bet
                self.bank[player] = self.bank.get(player) - bet
                return 1
            else:
                return 0
        except:
            raise Exception("Bet could not be placed, please try again")

    """Calls appropriate handler to distribute funds based on outcome of hand"""
    def resolve_bets(self, winners, draws):
        print('hello from resolver', self.bets.items())
        if winners:
            self.handle_win(winners)
        if draws:
            self.handle_draw(draws)
        self.handle_lose()
        self.bets.clear()
        print(self.bank, '  This is the bank')

    """Removes winnings from houses bank account, adds it to original bet, deposits the sum in player account and removes bet from bets object"""
    def handle_win(self, winners):
        for winner in winners:
            print('hello', winner, 'you are a winner')
            if self.bets.get(winner):
                bet = self.bets.get(winner)
                self.bank[self.DEALER] = self.bank.get(self.DEALER) - bet
                self.bank[winner] = self.bank.get(winner) + (bet * 2)
                self.bets.pop(winner)

    """Transfers money from bet object to the houses account for each loser"""
    def handle_lose(self):
        pot = 0
        for loser, bet in self.bets.items():
            pot += bet
        self.bank[self.DEALER] = self.bank.get(self.DEALER) + pot

    """Returns original bet amount to players account"""
    def handle_draw(self, draws):
        for draw in draws:
            bet_value = self.bets.get(draw)
            print(self.bets.items())
            print('hello', draw, bet_value)
            self.bank[draw] = self.bank.get(draw) + bet_value
            self.bets.pop(draw)
