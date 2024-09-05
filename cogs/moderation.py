import asyncio
import discord
from discord import app_commands
from discord.ext import commands


# Commande de clear
class Clear(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="clear", description="Supprime un certain nombre de messages.")
    async def clear(self, interaction: discord.Interaction, amount: int):
        if amount >= 1:
            if isinstance(interaction.channel, discord.TextChannel):
                try:
                    await interaction.response.defer(ephemeral=True)
                    
                    deleted = await interaction.channel.purge(limit=amount)
                    followup_message = await interaction.followup.send(f"{len(deleted)} messages ont été supprimés.", ephemeral=True)
                    await asyncio.sleep(3)
                    await followup_message.delete()
                except Exception as e:
                    await interaction.followup.send(f"{e}", delete_after=3, ephemeral=True)
        else:
            await interaction.response.send_message(
                "Vous devez supprimer au moins un message.", delete_after=3, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Clear(bot))