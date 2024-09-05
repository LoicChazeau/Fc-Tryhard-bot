import asyncio

import discord
from discord import Embed, app_commands
from discord.ext import commands
from replit import db
from datetime import datetime, timedelta

admin = 1280234769573216389


# Database admin commande
class Database(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="database",
                          description="Envoie la base de donnée.")
    async def database(self, interaction: discord.Interaction):
        guild = interaction.guild
        assert guild is not None
        member = await guild.fetch_member(interaction.user.id)
        assert member is not None

        if guild.get_role(admin) in member.roles:

            desc = ""
            for item in db.items():
                desc += f"{item}\n"

            embed = Embed(title="DATABASE",
                          description=(f"{desc}"),
                          color=0x00ff00)

            await interaction.response.send_message(embed=embed,
                                                    ephemeral=True)
        else:
            await interaction.response.send_message(
                "⚠️ - **Vous n'avez pas accès à cette commande !** ❌",
                ephemeral=True)


async def setup(bot):
    await bot.add_cog(Database(bot))
