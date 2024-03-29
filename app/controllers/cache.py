from pathlib import Path
from shutil import copyfile
import json
import os

import requests

from app.utils import logger, slugify
from typing import Tuple, List
from .base import Base
from .scraper import Scraper
from app.models.set import Set
from app.models.card import Card

project_root = Path(__file__).parent.parent.parent


class Cache(Base):
    def __init__(self):
        Base.__init__(self)
        self.cache = dict()
        self.sets: List[Set] = list()
        self.scraper = Scraper()
        self.folder_path = Path().home() / ".mythical-spoiler" / 'cache'
        self.cache_path = self.folder_path / 'cache.json'
        self.set_icons_path = self.folder_path / 'set_images'
        self.cards_images_path = self.folder_path / 'card_images'
        self.load_cache()

    def update_cache(self):
        # Cache set & card data
        for card_data in self.scraper.latest():
            card_name = self.scraper.get_pretty_name(card_data)
            if not card_name:
                continue
            set_name = card_data["set"]
            # Instantiate set models
            set_ = Set(set_name)

            # Check if set exists, otherwise cache it
            if not self.has_set(set_name):
                self.cache['sets'][set_name] = {}
            card_name = self.scraper.get_pretty_name(card_data)
            new_card = True

            # Check if card exists, otherwise cache it
            if not self.has_card(set_.name, card_name):
                logger.debug(f"Card from website: {card_name}")
                self.cache['sets'][set_.name][card_name] = card_data
            else:
                logger.debug(f"Card from cache: {card_name}")
                new_card = False

            # Instantiate card model
            _card = self.cache['sets'][set_.name][card_name]
            if _card:
                card = Card(_card, new=new_card)
                set_.append(card)
                self.download_card_images(card)
            else:
                logger.warning(f"Can't find card [{set_.name}] - {card_name}")
            self.sets.append(set_)
        self.write_cache()

    # Check if the cache has set
    def has_set(self, set_name):
        return set_name in self.cache['sets']

    # Check if the cache has a card
    def has_card(self, set_name, card_name):
        return card_name in self.cache['sets'][set_name] if self.has_set(set_name) else False

    # Read cache
    def load_cache(self):
        if not self.folder_path.exists():
            self.folder_path.mkdir(parents=True)
        if not self.set_icons_path.exists():
            self.set_icons_path.mkdir(parents=True)
        if not self.cards_images_path.exists():
            self.cards_images_path.mkdir(parents=True)

        if not self.cache_path.exists():
            copyfile(project_root / 'app' / 'cache.default.json', self.cache_path)

        with self.cache_path.open() as file:
            self.cache = json.load(file)

    # Write cache
    def write_cache(self):
        with self.cache_path.open('w+') as file:
            json.dump(self.cache, file, indent=2)

    # Download set images
    def download_set_images(self, set_: Set):
        # Check if set image exists, otherwise download it
        image_path, exists = self.set_image_path(set_)
        if not exists:
            logger.debug(f"Downloaded Set image: {set_.name}.png")
            with image_path.open('wb') as fp:
                fp.write(requests.get(self.config['domain'] + '/' + set_.name).content)

    # Download card images
    def download_card_images(self, card: Card):
        # Check if card image exists, otherwise download it
        image_path, exists = self.card_image_path(card)
        if not exists:
            logger.debug(f"Downloaded Card image: {card.get_image_filename()}.jpg")
            with image_path.open('wb') as fp:
                fp.write(requests.get(
                    self.config['domain'] + '/' + card.set + '/cards/' + card.normalized_name + '.jpg').content)

    def card_image_path(self, card: Card) -> Tuple[Path, bool]:
        """:returns path to the Card image if the image exists else returns None"""
        image_path = (self.cards_images_path / card.get_image_filename()).with_suffix('.jpg')
        if not image_path.exists():
            image_path = image_path.with_name(image_path.stem + "90").with_suffix(".jpg")
        return image_path, image_path.exists()

    def set_image_path(self, set_: Set) -> Tuple[Path, bool]:
        """:returns path to the Set image if the image exists else returns None"""
        image_path = (self.set_icons_path / set_.name).with_suffix('.png')
        if not image_path.exists():
            image_path = image_path.with_name(image_path.stem + "90").with_suffix(".jpg")
        return image_path, image_path.exists()

    def get_latest(self, amount=1) -> List:
        latest = self.scraper.get_latest(amount)
        return [Card(card, new=False) for card in latest]

    def delete(self, card):
        del self.cache['sets'][card.set][slugify(card.name)]
        image, exists = self.card_image_path(card)
        if exists:
            os.remove(image)
