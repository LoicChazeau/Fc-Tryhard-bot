import discord
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def hello(self, ctx):
        await ctx.send("Pong from the Ping!")

async def setup(bot):
    await bot.add_cog(Ping(bot))
