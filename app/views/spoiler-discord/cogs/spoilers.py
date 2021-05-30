import re
import os
import sys
import subprocess
import importlib
import logging

import asyncio
import discord
from discord.ext import commands, tasks


from app.controllers.base import Base
from app.models.spoiler import Spoiler
from app.controllers.cache import Cache

log = logging.getLogger('bot')


class ModCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        cache = Cache()
        self.spoiler = Spoiler(cache)
        self.spoiler.update_cache()
        self.channels = list()
        self.update_cache.start()

    async def cog_check(self, ctx):
        return ctx.message.author.guild_permissions.administrator

    def cog_unload(self):
        self.update_cache.cancel()

    @commands.command()
    async def listen(self, ctx: commands.Context):
        if ctx.channel not in self.channels:
            self.channels.append(ctx.channel)

    @commands.command()
    async def latest(self, ctx: commands.Context):
        image_path, exists = self.spoiler.get_card_image(self.spoiler.get_latest())
        picture = discord.File(image_path)
        if exists:
            await ctx.channel.send(file=picture)

    async def spoil(self, card):
        for channel in self.channels:
            image_path, exists = self.spoiler.get_card_image(card)
            picture, exists = discord.File(image_path)
            if exists:
                await channel.send(file=picture)

    @tasks.loop(minutes=0.5)
    async def update_cache(self):
        self.spoiler.update_cache()
        for card in self.spoiler.new_cards:
            card.new = False
            await self.spoil(card)


def setup(bot):
    bot.add_cog(ModCog(bot))
