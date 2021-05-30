from discord.ext import commands


class ModCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.message.author.guild_permissions.administrator

    async def sub(self):
        pass


def setup(bot):
    bot.add_cog(ModCog(bot))
