from .base import Base


class Spoiler(Base):
    def __init__(self, cache):
        super(Spoiler, self).__init__()
        self.cache = cache

    def update_cache(self):
        self.cache.update_cache()

    def __len__(self):
        return len(self.cache.sets)

    def find(self, name_of_set):
        for set_ in self.cache.sets:
            if set_.name == name_of_set:
                return set_
        return None

    @property
    def new_cards(self):
        return [card for set_ in self.cache.sets for card in set_.new_cards]

    def get_card_image(self, card):
        return self.cache.card_image_path(card)

    def get_latest(self, amount=1) -> []:
        return self.cache.get_latest(amount)

    def delete(self, card):
        self.cache.delete(card)
