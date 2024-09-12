import asyncio
import os
import threading
from datetime import datetime
from threading import Thread

import discord
from discord.channel import TextChannel
import pytz
import requests
from discord.ext import commands
from flask import Flask, jsonify, render_template, request, send_from_directory

from config import COMMAND_PREFIX, TOKEN, UPTIME_API_KEY
from database import get_all_users, get_user, init_db, update_quest_status
from utils import load_cogs

from website.console.commands import ICommand_help, discord_database, discord_broadcast

app = Flask('')
tz = pytz.timezone('Europe/Paris')

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


@app.route('/logs')
def view_logs():
    # Logique pour la page des logs (logs.html)
    all_files = reversed(os.listdir("logs"))
    files = []
    for file in all_files:
        if file.endswith(".log"):
            files.append(file)
    return render_template("website/logs.html", files=files)


@app.route('/logs/<filename>')
def get_log(filename):
    return send_from_directory('logs', filename)


#
#
#
#
#
#
#
#
#
#
#
#
#
#


@app.route('/console')
def view_console():
    return render_template("website/console.html")


# if data.get('type') == "raw":
# (Cela fonctionne très bien, mais :)
# Replit me dis ceci : "get" is not a known member of "None" (pyright-extended)
# Même avec cette ligne avertissement, le code fonctionne, mais j'aimerais bien savoir d'où vient le problème quand mêm
# Si cela peut amémliorer mon code
@app.route('/console_log', methods=['POST'])
def console_log():

    data = request.json

    if data is not None:
        if data.get('type') == "raw":
            for message in data.get('messages'):
                with open("website/console/console.txt", 'a') as file:
                    file.write(f"{message}\n")

        if data.get('type') == "info":
            for message in data.get('messages'):
                now = datetime.now(tz)
                time = f"[{now.hour}:{now.minute}:{now.second}]"
                with open("website/console/console.txt", 'a') as file:
                    file.write(f"{time} [FcTryHard/INFO]: {message}\n")

        return jsonify({
            "status": "Success",
            "message": "Command executed successfully"
        }), 200
    else:
        return jsonify({"type": "error", "message": "No data received"})


@app.route('/console/<filename>')
def get_file(filename):
    return send_from_directory('website/console', filename)


ICommands = {
    'help': ICommand_help,
    'database': discord_database,
    'db': discord_database,
    'broadcast': discord_broadcast
}


@app.route('/console_execute_python', methods=['POST'])
def execute_python():
    data = request.json
    if data is not None:
        # method = execute_command(data)
        if data.get('command_name') in ICommands:
            method = ICommands[data.get('command_name')]
            ctx = {
                "bot": bot,
                "command": data.get('command_name'),
                "args": data.get('args')
            }
            asyncio.run_coroutine_threadsafe(method(ctx), bot.loop)
            return jsonify({
                "type": "success",
                "message": "Command executed successfully"
            })
        else:
            now = datetime.now(tz)
            time = f"[{now.hour}:{now.minute}:{now.second}]"
            with open("website/console/console.txt", 'a') as file:
                file.write(
                    f"{time} [FcTryHard/INFO]: Unknown command. Type 'help' for help.\n"
                )
            return jsonify({"type": "error", "message": "No data received"})
    else:
        return jsonify({"type": "error", "message": "No data received"})


def console_logs(type: str, messages: list):

    if type == "raw":
        for message in messages:
            with open("website/console/console.txt", 'a') as file:
                file.write(f"{message}\n")

    if type == "info":
        for message in messages:
            now = datetime.now(tz)
            time = f"[{now.hour}:{now.minute}:{now.second}]"
            with open("website/console/console.txt", 'a') as file:
                file.write(f"{time} [FcTryHard/INFO]: {message}\n")


# def example_command(args):
#     threading.Thread(target=send_message_to_discord, args=(args, )).start()

# async def _send_message(content):
#     channel_id = 1280127733157855357  # Remplace par l'ID de ton salon
#     channel = bot.get_channel(channel_id)

#     if channel and isinstance(channel, discord.TextChannel):
#         await channel.send(content)

# def send_message_to_discord(content):
#     asyncio.run_coroutine_threadsafe(_send_message(content), bot.loop)

# @app.route('/console_execute_python', methods=['POST'])
# def execute_python():
#     data = request.json
#     if data is not None:
#         method = globals().get(data.get('name'), None)
#         if method:
#             method(data.get('args'))
#         return jsonify({"type": "success", "message": "Command executed successfully"})
#     else:
#         return jsonify({"type": "error", "message": "No data received"})

# def example_command(args):
#     threading.Thread(target=send_message_to_discord, args=(args, )).start()

#
#
#
#
#
#
#
#
#
#
#
#


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

    registered_id = user_data[
        'registered_id']  # ID du message associé à l'utilisateur
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
            "🥳 - **Super ! Je reviendrai demain pour te prévenir !** ✅")


async def main():
    # Charger les cogs avec await
    await load_cogs(bot)

    # Démarrer le bot
    for i in range(1, 5):
        print(f"Tentative n°{i}...")
        try:
            await bot.start(TOKEN)
        except Exception as e:
            print(e)
            print("[ERREUR] - Nouvelle tentative dans 5 secondes")
            await asyncio.sleep(5)
    # await bot.start(TOKEN)


if __name__ == "__main__":
    # Initialiser la base de données SQLite
    init_db()

    # Démarrer le serveur Flask pour garder le bot en vie
    keep_alive()

    # Exécuter le bot avec asyncio.run()
    asyncio.run(main())
