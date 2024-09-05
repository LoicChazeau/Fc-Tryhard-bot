# utils.py

import discord
from discord.ext import commands
import os


# Fonction pour charger les cogs automatiquement
async def load_cogs(bot):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')


# Fonction pour vérifier si un utilisateur a un rôle spécifique
def has_role(member: discord.Member, role_name: str) -> bool:
    return any(role.name == role_name for role in member.roles)


# Fonction pour formater les messages
def format_message(message: str) -> str:
    # Exemple simple d'ajout d'une ligne de signature à un message
    return f"{message}\n\n---\nEnvoyé par le bot FC-Tryhard"


# Fonction pour créer un embed standard
def create_embed(title: str,
                 description: str,
                 color=0x00ff00) -> discord.Embed:
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text="Bot FC-Tryhard")
    return embed
