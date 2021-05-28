import os
import logging
import sys
import traceback

import discord
from discord.ext import commands
from dotenv import load_dotenv

from cogs.game import playerdata
from cogs.uilts import game_strings, exceptions

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
PREFIXES = os.getenv('PREFIXES').split(",")


log_formatter = logging.Formatter('%(levelname)s:%(name)s: %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(log_formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)
log = logging.getLogger('bot')


initial_extensions = (
    'cogs.admin',
    'cogs.mod'
)


class Beans(commands.Bot):
    def __init__(self, *args, **kwargs):
        super(Beans, self).__init__(*args, **kwargs)
        emoji = game_strings.Emoji(self)
        game_strings.emoji = emoji

        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                log.error(f'Failed to load extension {extension}.')
                traceback.print_exc()

    async def close(self):
        await super().close()



bot = Beans(command_prefix=PREFIXES, help_command=None)
if __name__ == '__main__':
    playerdata.start()
    bot.run(TOKEN)