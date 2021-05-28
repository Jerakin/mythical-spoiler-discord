from .base import Base


class Set(Base):

    # Name
    name = ''

    # Cards
    cards = []

    # Get sets from source
    def __init__(self, name):
        Base.__init__(self)
        self.name = name
        self.cards = []

    # Set cards
    def set_cards(self, cards):
        self.cards = cards

    # Append card
    def append_card(self, card):
        self.cards.append(card)

    # Get name
    def get_name(self):
        return self.name

    # Get cards
    def get_cards(self):
        return self.cards

    # Get card urls length
    def get_cards_length(self):
        return len(self.cards)

    # Get first card
    def get_first_card(self):
        return self.cards[0]

    # Find card
    def find_card(self, card_name):
        for card in self.cards:
            if card.get_name() == card_name:
                return card

        return False

    # Get new cards
    def get_new_cards(self):
        cards = []

        for card in self.cards:
            if card.is_new():
                cards.append(card)

        return cards
