# https://github.com/dfsoeten/mtg-spoiler-bot/blob/master/app/controllers/scraper.py

import requests
from bs4 import BeautifulSoup
from app.controllers.base import Base
from app.utils import colored, slugify


class Scraper(Base):
    def __init__(self):
        super(Scraper, self).__init__()

    @staticmethod
    def get_card_name(card_url):
        return slugify(card_url.replace('cards/', '').replace('.html', ''))

    def get_sets(self):
        if not self.config['silent']:
            print(colored('[GET][SETS]', 'green'))

        soup = BeautifulSoup(requests.get(self.config['domain'] + self.config['new-sets-url']).text, 'lxml')
        sets = []

        for set_ in soup.find('tr', attrs={'align': 'center'}).findAll('td'):
            set_name = set_.find('a')['href']

            if len(set_name) < 5:
                # Map set names
                sets.append(set_name)

        return sets

    def get_card_urls(self, set_name):
        if not self.config['silent']:
            print(colored('[GET][SET] ' + set_name, 'green'))

        soup = BeautifulSoup(requests.get(self.config['domain'] + '/' + set_name).text, 'lxml')
        card_urls = []

        for card in soup.findAll('a', 'card'):
            card_urls.append(card['href'])

        return card_urls

    def get_card(self, set_name, card_url):

        if not self.config['silent']:
            print(colored('[GET][CARD] ' + self.get_card_name(card_url), 'green'))

        # Get card data
        try:
            page = BeautifulSoup(requests.get(self.config['domain'] + '/' + set_name + '/' + card_url).text, 'lxml')
            card = page \
                .find('table',
                      attrs={'valign': 'top', 'cellspacing': 0, 'cellpadding': 5, 'border': 0, 'align': 'center'}) \
                .findAll('td')

        except Exception as e:
            if not self.config['silent']:
                print(colored('[ERROR] Could not get card data from ' + self.config['domain'] + '/' + set_name + '/' + card_url, 'red'))

            if self.config['debug']['is-enabled']:
                print(colored(e, 'red'))

        # Parse card data
        try:
            types = [c.strip() for c in card[2].text.strip().split('-')]
            pwr_thg = [pt.strip() for pt in card[7].find('font').text.strip().split('/')]
            return {
                'name': card[0].text.strip(),
                'manacost': card[1].text.strip(),
                'type': types[0] if len(types) >= 1 else None,
                'sub_types': types[1].split(' ') if len(types) == 2 else None,
                'set': set_name,
                'rules_text': card[3].text.strip(),
                'flavor': card[4].text.strip(),
                'artist': card[6].find('font').text.strip(),
                'power': pwr_thg[0] if len(pwr_thg) == 2 else None,
                'toughness': pwr_thg[1] if len(pwr_thg) == 2 else None,
                'url': self.config['domain'] + '/' + set_name + '/' + card_url
            }
        except IndexError:
            # The card is probably a dual face card
            return {
                'name': self.get_card_name(card_url),
                'manacost': None,
                'type': None,
                'sub_types': None,
                'set': set_name,
                'rules_text': None,
                'flavor': None,
                'artist': None,
                'power': None,
                'toughness': None,
                'url': self.config['domain'] + '/' + set_name + '/' + card_url
            }
        except Exception as e:
            if not self.config['silent']:
                print(colored('[ERROR] Could not parse card data from ' + self.config['domain'] + '/' + set_name + '/' + card_url, 'red'))

            if self.config['debug']['is-enabled']:
                print(colored(e, 'red'))
            return None


if __name__ == '__main__':
    _card = 'cards/glasspoolmimic.html'
    _card2 = 'cards/nimbletrapfinder.html'
    scraper = Scraper()
    if _card in scraper.get_card_urls("zrs"):
        print(scraper.get_card('zrs', _card))
    if _card2 in scraper.get_card_urls("zrs"):
        print(scraper.get_card('zrs', _card2))