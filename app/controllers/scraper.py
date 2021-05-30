import requests
from bs4 import BeautifulSoup
from app.controllers.base import Base
from app.utils import slugify, logger


class Scraper(Base):
    def __init__(self):
        super(Scraper, self).__init__()

    @staticmethod
    def get_card_name(card_url):
        return slugify(card_url.replace('cards/', '').replace('.html', ''))

    def get_latest(self, amount=1):
        soup = BeautifulSoup(requests.get(self.config['domain'] + self.config['new-sets-url']).text, 'lxml')

        ordered = []
        for card in soup.find_all('div', {"class": "grid-container"}):
            card_ref = card.find('a')['href']
            set_, *url_ = card_ref.split("/")
            latest = self.get_card(set_.strip(), "/".join(url_).strip())
            if latest:
                ordered.append(latest)
                logger.info(f"Latest: {latest['name']}")
            else:
                logger.debug("Could not find latest card")

            if amount >= len(ordered):
                return ordered
        return ordered

    def get_sets(self):
        logger.info("Available Sets")

        soup = BeautifulSoup(requests.get(self.config['domain'] + self.config['new-sets-url']).text, 'lxml')
        sets = []

        for set_ in soup.find('tr', attrs={'align': 'center'}).findAll('td'):
            set_name = set_.find('a')['href']

            if len(set_name) < 5:
                logger.info(f"-- {set_name}")
                sets.append(set_name)
        return sets

    def get_card_urls(self, set_name):
        soup = BeautifulSoup(requests.get(f"{self.config['domain']}/{set_name}").text, 'lxml')
        card_urls = []
        card = soup.find('a', 'card')
        while card:
            try:
                card_url = card["href"]
                if card_url.startswith("cards/"):
                    card_urls.append(card_url)
            except KeyError:
                pass

            card = card.find_next()

        return card_urls

    def get_card(self, set_name, card_url):
        # Get card data
        try:
            page = BeautifulSoup(requests.get(f"{self.config['domain']}/{set_name}/{card_url}").text, 'lxml')
            card = page \
                .find('table',
                      attrs={'valign': 'top', 'cellspacing': 0, 'cellpadding': 5, 'border': 0, 'align': 'center'}) \
                .findAll('td')

        except Exception as e:
            logger.info(f"Could not get card data from {self.config['domain']}/{set_name}/{card_url}")
            logger.debug(e)

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
                'url': f"{self.config['domain']}/{set_name}/{card_url}"
            }
        except Exception as e:
            logger.info(f"Could not parse card data from {self.config['domain']}/{set_name}/{card_url}")
            logger.debug(e)
        return None


if __name__ == '__main__':
    _card = 'cards/glasspoolmimic.html'
    _card2 = 'cards/nimbletrapfinder.html'
    scraper = Scraper()
    if _card in scraper.get_card_urls("zrs"):
        print(scraper.get_card('zrs', _card))
    if _card2 in scraper.get_card_urls("zrs"):
        print(scraper.get_card('zrs', _card2))