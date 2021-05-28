import os
from pathlib import Path
from shutil import copyfile
import requests
import json

from .base import Base
from .scraper import Scraper
from app.utils import colored
from app.models.set import Set
from app.models.card import Card

project_root = Path(__file__).parent.parent.parent


class Cache(Base):
    # Spoiler
    spoiler = None

    # Scraper
    scraper = None

    # Cache
    cache = {}

    def __init__(self, spoiler):
        Base.__init__(self)
        self.spoiler = spoiler
        self.scraper = Scraper()
        self.folder_path = Path().home() / ".mythical-spoiler" / 'cache'
        self.cache_path = self.folder_path / 'cache.json'
        self.set_icons_path = self.folder_path / 'set_images'
        self.cards_images_path = self.folder_path / 'card_images'
        self.read_cache()
        self.start()
        self.write_cache()

    def start(self):
        # Cache set & card data
        for set_name in self.scraper.get_sets():

            # Instantiate set models
            set_ = Set(set_name)

            # Check if set exists, otherwise cache it
            if not self.has_set(set_name):
                self.cache['sets'][set_name] = {}
                self.cache_set_images(set_)

            for card_url in self.scraper.get_card_urls(set_.get_name()):
                card_name = self.scraper.get_card_name(card_url)
                new_card = True

                # Check if card exists, otherwise cache it
                if not self.has_card(set_.get_name(), card_name):
                    self.cache['sets'][set_.get_name()][self.scraper.get_card_name(card_url)] = self.scraper.get_card(set_.get_name(), card_url)

                    if not self.config['silent']:
                        print(colored('[CACHED][CARD] ' + self.scraper.get_card_name(card_name), 'blue'))
                else:
                    new_card = False

                    if not self.config['silent']:
                        print(colored('[FROM CACHE][CARD] ' + self.scraper.get_card_name(card_name), 'yellow'))

                # Instantiate card model
                card = Card(self.cache['sets'][set_.get_name()][card_name], new=new_card)
                set_.append_card(card)
                self.cache_card_images(card)

            self.spoiler.append_set(set_)

    # Check if the cache has set
    def has_set(self, set_name):
        return set_name in self.cache['sets']

    # Check if the cache has a card
    def has_card(self, set_name, card_name):
        return card_name in self.cache['sets'][set_name] if self.has_set(set_name) else False

    # Read cache
    def read_cache(self):
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

    # Cache set images
    def cache_set_images(self, set_):
        # Check if set image exists, otherwise cache it
        image_path = (self.set_icons_path / set_.get_name()).with_suffix('.png')
        if not image_path.exists():
            with image_path.open('wb') as fp:
                fp.write(requests.get(self.config['domain'] + '/' + set_.get_name()).content)

            if not self.config['silent']:
                print(colored('[CACHED][IMAGE] ' + set_.get_name() + '.png', 'blue'))

    # Cache card images
    def cache_card_images(self, card):
        # Check if card image exists, otherwise cache it
        image_path = (self.cards_images_path / card.get_image_filename()).with_suffix('.jpg')
        if not image_path.exists() and card.get_image_filename() != '':
            with image_path.open('wb') as fp:
                fp.write(requests.get(
                    self.config['domain'] + '/' + card.get_set() + '/cards/' + card.get_normalized_name() + '.jpg').content)

            if not self.config['silent']:
                print(colored('[CACHED][IMAGE] ' + card.get_image_filename() + '.jpg', 'blue'))

    # Return all new cards in the spoiler model
    def get_new_spoilers(self):
        return self.spoiler
