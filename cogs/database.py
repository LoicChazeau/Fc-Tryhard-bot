import asyncio
import discord
from discord import Embed, app_commands
from discord.ext import commands
from database import get_all_users, get_all_users_db  # Importez la fonction pour récupérer les utilisateurs
from datetime import datetime, timedelta

admin = 866688547078668308


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

        # Vérifiez si l'utilisateur a le rôle d'admin
        if guild.get_role(admin) in member.roles:

            # Récupérer toutes les données des utilisateurs depuis la base de données
            all_users = get_all_users_db()

            # Créer une description pour chaque utilisateur
            desc = ""
            for user_id, user_data in all_users.items():
                desc += f"User ID: {user_id}\n"
                desc += f"Pseudo: {user_data['pseudo']}\n"
                desc += f"Registered ID: {user_data['registered_id']}\n"
                desc += f"Quest Completed: {user_data['quest_completed']}\n"
                desc += f"Vote1 Completed: {user_data.get('vote1_completed', False)}\n"
                desc += f"Vote2 Completed: {user_data.get('vote2_completed', False)}\n"
                desc += f"Last Pets Time: {user_data.get('last_pets_time', 'N/A')}\n"
                desc += "\n"

            # Créer un embed pour afficher les données
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
