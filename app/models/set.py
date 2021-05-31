from .base import Base


class Set(Base):
    def __init__(self, name):
        super(Set, self).__init__()
        self.name = name
        self.cards = []

    def append(self, card):
        self.cards.append(card)

    def __len__(self):
        return len(self.cards)

    def find(self, name_of_card):
        for card in self.cards:
            if card.name == name_of_card:
                return card
        return None

    @property
    def new_cards(self):
        return [card for card in self.cards if card.new]
