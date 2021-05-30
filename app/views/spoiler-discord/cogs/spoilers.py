from pathlib import Path
import json
import discord
from discord.ext import commands, tasks

from app.models.spoiler import Spoiler
from app.controllers.cache import Cache


class ModCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conf = dict()
        self.load_config()

        cache = Cache()
        self.spoiler = Spoiler(cache)
        self.update_cache.start()

    def load_config(self):
        config = Path().home() / ".mythical-spoiler" / "config.json"
        if config.exists():
            with config.open() as fp:
                self.conf = json.load(fp)
        else:
            self.conf = {"channels": []}

    def save_servers(self):
        config = Path().home() / ".mythical-spoiler" / "config.json"
        with config.open("r") as fp:
            json.dump(self.conf, fp)

    async def cog_check(self, ctx):
        return ctx.message.author.guild_permissions.administrator

    def cog_unload(self):
        self.update_cache.cancel()

    @commands.command()
    async def listen(self, ctx: commands.Context):
        if ctx.channel not in self.conf["channels"]:
            self.conf["channels"].append(ctx.channel)

    @commands.command()
    async def latest(self, ctx: commands.Context, amount: int = 1):
        for card in self.spoiler.get_latest(amount):
            image_path, exists = self.spoiler.get_card_image(card)
            picture = discord.File(image_path)
            if exists:
                await ctx.channel.send(file=picture)

    async def spoil(self, card):
        for channel in self.conf["channels"]:
            image_path, exists = self.spoiler.get_card_image(card)
            picture, exists = discord.File(image_path)
            if exists:
                await channel.send(file=picture)

    @tasks.loop(minutes=5)
    async def update_cache(self):
        self.spoiler.update_cache()
        for card in self.spoiler.new_cards:
            card.new = False
            await self.spoil(card)


def setup(bot):
    bot.add_cog(ModCog(bot))
