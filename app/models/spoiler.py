from typing import List

from .base import Base
from .set import Set


class Spoiler(Base):
    sets: List[Set] = []

    def __init__(self):
        Base.__init__(self)

    def append(self, set_):
        self.sets.append(set_)

    def __len__(self):
        return len(self.sets)

    def find(self, name_of_set):
        for set_ in self.sets:
            if set_.name == name_of_set:
                return set_
        return None

    @property
    def new_cards(self):
        return [card for set_ in self.sets for card in set_.new_cards]
