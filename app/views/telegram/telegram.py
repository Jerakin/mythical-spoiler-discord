import os

from dotenv import load_dotenv
import telegram

from app.controllers.base import Base
from app.models.spoiler import Spoiler
from app.controllers.cache import Cache
from app.utils import colored


class App(Base):
    # Spoiler data
    spoiler = Spoiler()

    # Cache spoiler data
    cache = Cache(spoiler)

    def __init__(self):
        super().__init__()

        print(colored('{} new cards found'.format(len(self.spoiler.new_cards)), 'yellow'))

    def start(self):
        bot = telegram.Bot(token=os.getenv('API_TOKEN'))

        print(colored('Bot with id {} and name {} connected'.format(bot.get_me()['id'], bot.get_me()['first_name']),
                      'green'))
        print(colored('Beaming spoilers to {}'.format(self.config['telegram-channel-id']), 'green'))

        for card in self.spoiler.new_cards:
            bot.send_photo(
                chat_id='@{}'.format(self.config['telegram-channel-id']),
                photo=open('./app/cache/card_images/{}.jpg' \
                           .format(card.get_image_filename()), 'rb')
            )
            print(colored('[MESSAGE] Send', 'blue'))

        print(colored('Done. {} cards spoiled'.format(len(self.spoiler.new_cards)), 'blue'))


if __name__ == '__main__':
    # Load .env variables
    load_dotenv()

    # Start app
    app = App()
    app.start()

    exit(0)
