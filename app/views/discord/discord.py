import os
import logging
import sys
import traceback

from discord.ext import commands
from dotenv import load_dotenv

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


class MythicBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super(MythicBot, self).__init__(*args, **kwargs)
        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                log.error(f'Failed to load extension {extension}.')
                traceback.print_exc()

    async def close(self):
        await super().close()


bot = MythicBot(command_prefix=PREFIXES, help_command=None)


if __name__ == '__main__':
    bot.run(TOKEN)
