from discord.ext import commands, tasks
from app.utils import logger


class ModCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_spoilers.start()

    async def cog_check(self, ctx):
        return ctx.message.author.guild_permissions.administrator

    def cog_unload(self):
        self.check_spoilers.cancel()

    async def spoil(self, card):
        for channel_id in self.bot.conf["channels"]:
            channel = self.bot.get_channel(channel_id)
            if channel is None:
                logger.warning(f"Can not find channel with id '{channel_id}'")
                return
            await self.bot.send_image(channel, card)

    @commands.command()
    async def subscribe(self, ctx: commands.Context):
        logger.info(f"Server '{ctx.guild.name}' with id '{ctx.guild.id}' subscribed")
        if ctx.channel not in self.bot.conf["channels"]:
            self.bot.conf["channels"].append(ctx.channel.id)
            self.bot.save_servers()
            await ctx.channel.send("You will now get Spoiler images sent here")

    @tasks.loop(minutes=5)
    async def check_spoilers(self):
        logger.info("Updating Cache")
        self.bot.spoiler.update_cache()
        for card in self.bot.spoiler.new_cards:
            card.new = False
            await self.spoil(card)


def setup(bot):
    bot.add_cog(ModCog(bot))
