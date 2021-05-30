from pathlib import Path
import json
import discord
from discord.ext import commands, tasks
from discord import client

from app.models.spoiler import Spoiler
from app.controllers.cache import Cache


class ModCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        cache = Cache()
        self._config_path = cache.folder_path.parent / "config.json"
        self.conf = dict()
        self.load_config()
        self.spoiler = Spoiler(cache)
        self.update_cache.start()

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

    async def cog_check(self, ctx):
        return ctx.message.author.guild_permissions.administrator

    def cog_unload(self):
        self.update_cache.cancel()

    @commands.command()
    async def pop(self, ctx: commands.Context):
        latest = self.spoiler.get_latest()
        if latest:
            self.spoiler.delete(latest[0])

    @commands.command()
    async def listen(self, ctx: commands.Context):
        if ctx.channel not in self.conf["channels"]:
            self.conf["channels"].append(ctx.channel.id)
            self.save_servers()

    @commands.command()
    async def latest(self, ctx: commands.Context, amount: int = 1):
        for card in self.spoiler.get_latest(amount):
            image_path, exists = self.spoiler.get_card_image(card)
            picture = discord.File(image_path)
            if exists:
                await ctx.channel.send(file=picture)

    async def spoil(self, card):
        for channel_id in self.conf["channels"]:
            image_path, exists = self.spoiler.get_card_image(card)
            if exists:
                with image_path.open("rb") as fp:
                    picture = discord.File(fp)

                channel = self.bot.get_channel(channel_id)
                await channel.send(file=picture)

    @commands.command()
    async def force(self, ctx):
        self.spoiler.update_cache()
        for card in self.spoiler.new_cards:
            image_path, exists = self.spoiler.get_card_image(card)
            if exists:
                with image_path.open("rb") as fp:
                    picture = discord.File(fp)
                await ctx.channel.send(file=picture)

    @tasks.loop(minutes=5)
    async def update_cache(self):
        self.spoiler.update_cache()
        for card in self.spoiler.new_cards:
            card.new = False
            await self.spoil(card)


def setup(bot):
    bot.add_cog(ModCog(bot))
