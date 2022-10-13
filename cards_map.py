"""This class creates a mapping between the numeric card alias and the actual face value of each card"""


class CardMap:
    def __init__(self):
        self.card_map = {}
        self.card_values = {}

    def get_map(self) -> dict:
        card_map = self.card_map
        card_map[0] = '2'
        card_map[1] = '3'
        card_map[2] = '4'
        card_map[3] = '5'
        card_map[4] = '6'
        card_map[5] = '7'
        card_map[6] = '8'
        card_map[7] = '9'
        card_map[8] = '10'
        card_map[9] = 'J'
        card_map[10] = 'Q'
        card_map[11] = 'K'
        card_map[12] = 'A'
        return card_map

