import re
import os
import sys
import subprocess
import importlib
import logging

import asyncio
from discord.ext import commands, tasks


from app.controllers.base import Base
from app.models.spoiler import Spoiler
from app.controllers.cache import Cache

log = logging.getLogger('bot')


class ModCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spoiler = Spoiler()
        self.cache = Cache(self.spoiler)

    async def cog_check(self, ctx):
        return ctx.message.author.server_permissions.administrator

    @tasks.loop(minutes=0.5)
    async def update_cache(self):
        pass


def setup(bot):
    bot.add_cog(ModCog(bot))
