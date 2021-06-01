import os
import sys
import traceback
import json
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

app = Path(__file__).parent.parent.parent.parent.parent.as_posix()
if app not in sys.path:
    sys.path.append(app)

from app.models.spoiler import Spoiler
from app.controllers.cache import Cache
from app.utils import logger


load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
PREFIXES = os.getenv('PREFIXES').split(",")

initial_extensions = (
    'cogs.admin',
    'cogs.spoilers',
    'cogs.mod'
)


class MythicBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super(MythicBot, self).__init__(*args, **kwargs)
        cache = Cache()
        self._config_path = cache.folder_path.parent / "config.json"
        self.conf = dict()
        self.load_config()
        self.spoiler = Spoiler(cache)

        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                logger.error(f'Failed to load extension {extension}.')
                traceback.print_exc()

    def load_config(self):
        if self._config_path.exists():
            with self._config_path.open("r") as fp:
                self.conf = json.load(fp)
        else:
            with self._config_path.open("w") as fp:
                json.dump({"channels": []}, fp)
            self.conf = {"channels": []}

    def save_servers(self):
        with self._config_path.open("w") as fp:
            json.dump(self.conf, fp)

    async def send_image(self, channel, card):
        image_path, exists = self.spoiler.get_card_image(card)
        logger.info(f"Sending card {card.name}, Image: {exists}")
        if exists:
            with image_path.open("rb") as fp:
                picture = discord.File(fp, filename=card.name + ".jpg")
            await channel.send(file=picture)

    async def close(self):
        self.save_servers()
        await super().close()


logger.info(f"""Prefixes: {", ".join([f'"{x}"' for x in PREFIXES])}""")
bot = MythicBot(command_prefix=PREFIXES, help_command=None)


if __name__ == '__main__':
    bot.run(TOKEN)
