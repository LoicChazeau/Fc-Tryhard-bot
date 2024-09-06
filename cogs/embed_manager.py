import json

from discord import Embed
from discord.ext import commands


class EmbedManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_embed(self, id: str) -> Embed:
        try:
            with open('ressources/blocaria_embed.json', 'r', encoding='utf-8') as file:
                data = json.load(file)

            title = data[id]["title"]
            description = "".join(data[id]["description"])
            color = int(data[id]["color"], 16)  # Convertir le code couleur hexadécimal en entier

            embed = Embed(
                title=title,
                description=description,
                color=color)

            return embed
        except KeyError:
            return Embed(title="Erreur", description="ID d'embed non trouvé.", color=0xFF0000)
        except Exception as e:
            return Embed(title="Erreur", description=str(e), color=0xFF0000)

# Fonction setup pour ajouter ce cog au bot
async def setup(bot):
    await bot.add_cog(EmbedManager(bot))
