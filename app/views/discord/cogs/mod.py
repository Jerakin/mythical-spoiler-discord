import re
import os
import sys
import subprocess
import importlib
import logging

import asyncio
from discord.ext import commands

log = logging.getLogger('bot')


class ModCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.message.author.server_permissions.administrator

    async def sub(self):
        pass


def setup(bot):
    bot.add_cog(ModCog(bot))
