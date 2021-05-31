import os
import logging
import sys
import traceback
from pathlib import Path

import discord.ext.commands as commands
from dotenv import load_dotenv

app = Path(__file__).parent.parent.parent.parent.parent.as_posix()
if app not in sys.path:
    sys.path.append(app)

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
    'cogs.spoilers',
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


log.info(f"""Prefixes: {", ".join([f'"{x}"' for x in PREFIXES])}""")
bot = MythicBot(command_prefix=PREFIXES, help_command=None)


if __name__ == '__main__':
    bot.run(TOKEN)
