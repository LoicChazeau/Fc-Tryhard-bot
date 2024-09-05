import asyncio
import os
from threading import Thread

import discord
import requests
from discord.ext import commands
from flask import Flask, render_template

import sqlite3
from database import get_user, update_quest_status, get_all_users, init_db

from config import COMMAND_PREFIX, TOKEN, UPTIME_API_KEY
from utils import load_cogs

app = Flask('')

# URL de l'API
login_url = "https://voteapi.rivrs.io/v1/user/login"
data_url = "https://voteapi.rivrs.io/v1/vote/availableVote"
uptime_url = "https://api.uptimerobot.com/v2/getMonitors"

# Spécifiez le dossier où Flask doit chercher les templates
app = Flask(__name__,
            template_folder=os.path.dirname(os.path.abspath(__file__)))

@app.route('/')
def home():
    # Information pour la requête UPTIME
    payload = {"api_key": UPTIME_API_KEY, "format": "json"}

    response = requests.post(uptime_url, data=payload)
    monitors = response.json().get('monitors', [])

    # Informations pour la requête POST de login
    login_data = "LaPice_"
    headers = {"Content-Type": "text/plain", "Origin": "https://blocaria.fr"}

    # Faire la requête POST pour se connecter
    login_response = requests.post(login_url, data=login_data, headers=headers)

    # Vérifiez si la connexion a réussi
    if login_response.status_code == 200:
        # Si la connexion réussit, récupérez les cookies de session
        cookies = login_response.cookies

        # Utiliser les cookies pour faire la requête GET authentifiée
        response = requests.get(data_url, cookies=cookies)

        if response.status_code == 200:
            available_vote_data = response.json()
        else:
            available_vote_data = {
                "error": "Failed to retrieve data from API."
            }
    else:
        available_vote_data = {"error": "Login failed."}

    # Récupérer des informations du bot et de la base de données
    bot_info = {
        "bot_name": bot.user.name if bot.user else "Bot",
        "guild_count": len(bot.guilds) if bot.user else 0,
        "database_content": get_all_users(),
        "available_vote_data": available_vote_data
    }
    return render_template("index.html", **bot_info, monitors=monitors)


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()


intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.dm_messages = True
intents.messages = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


@bot.event
async def on_ready():
    # Synchroniser les commandes avec le serveur
    synced = await bot.tree.sync()
    print(
        f"Synchronisation des commandes réussie : {len(synced)} commandes synchronisées."
    )
    print(f"{synced}")
    print(f'{bot.user} est connecté et prêt à l\'emploi !')


@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    emoji = payload.emoji
    user_id = str(payload.user_id)

    # Récupérer les informations de l'utilisateur à partir de la base de données SQLite
    user_data = get_user(user_id)

    # Si l'utilisateur n'est pas trouvé dans la base de données, arrêter l'exécution
    if user_data is None:
        print(f"User {user_id} not found in the database.")
        return

    registered_id = user_data['registered_id']  # ID du message associé à l'utilisateur
    quest_completed = user_data['quest_completed']  # Statut de la quête

    # Vérifiez si le channel est un message privé
    if not isinstance(channel, discord.DMChannel):
        return

    # Vérifier que le message correspond
    if str(payload.message_id) != registered_id:
        print("Message ID does not match.")
        return

    # Vérifier que l'emoji est "✅"
    if emoji.name != "✅":
        return

    # Si l'utilisateur a déjà complété la quête
    if quest_completed:
        await channel.send(
            "⚠️ - **Tu as déjà réalisé ta quête journalière. Reviens demain !** ❌"
        )
    else:
        # Mettre à jour le statut de la quête dans la base de données
        update_quest_status(user_id, True)

        await channel.send(
            "🥳 - **Super ! Je reviendrai demain pour te prévenir !** ✅"
        )


async def main():
    # Charger les cogs avec await
    await load_cogs(bot)

    # Démarrer le bot
    await bot.start(TOKEN)


if __name__ == "__main__":
    # Initialiser la base de données SQLite
    init_db()

    # Démarrer le serveur Flask pour garder le bot en vie
    keep_alive()

    # Exécuter le bot avec asyncio.run()
    asyncio.run(main())
