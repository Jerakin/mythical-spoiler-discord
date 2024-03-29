from discord.ext import commands


class ModCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def latest(self, ctx: commands.Context, amount: int = 1):
        for card in self.bot.spoiler.get_latest(amount):
            await self.bot.send_image(ctx.channel, card)


def setup(bot):
    bot.add_cog(ModCog(bot))
