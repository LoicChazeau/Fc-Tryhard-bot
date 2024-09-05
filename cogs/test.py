import discord
from discord.ext import commands

class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def hello(self, ctx):
        await ctx.send("Pong from the TestCog!")

async def setup(bot):
    await bot.add_cog(TestCog(bot))
