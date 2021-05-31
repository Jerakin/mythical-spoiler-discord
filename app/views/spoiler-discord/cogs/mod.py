from discord.ext import commands, tasks


class ModCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_cache.start()

    async def cog_check(self, ctx):
        return ctx.message.author.guild_permissions.administrator

    def cog_unload(self):
        self.update_cache.cancel()

    async def spoil(self, card):
        for channel_id in self.bot.conf["channels"]:
            channel = self.bot.get_channel(channel_id)
            await self.bot.send_image(channel, card)

    @commands.command()
    async def listen(self, ctx: commands.Context):
        if ctx.channel not in self.bot.conf["channels"]:
            self.bot.conf["channels"].append(ctx.channel.id)
            self.bot.save_servers()

    @tasks.loop(minutes=5)
    async def update_cache(self):
        self.bot.spoiler.update_cache()
        for card in self.bot.spoiler.new_cards:
            card.new = False
            await self.spoil(card)


def setup(bot):
    bot.add_cog(ModCog(bot))
