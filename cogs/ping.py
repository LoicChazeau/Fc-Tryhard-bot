from discord.ext import commands

from scripts_utils import logs_manager


class Ping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def hello(self, ctx):
        # await ctx.send("Pong from the Ping!")

        await ctx.send("Pong!")
        logs_manager.logs("test")


async def setup(bot):
    await bot.add_cog(Ping(bot))
