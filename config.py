# config.py

import os
from dotenv import load_dotenv

# Charger le fichier .env
load_dotenv()

discord_token = os.getenv('DISCORD_TOKEN')
uptime_api_key = os.getenv('UPTIME_API_KEY')

# Le token d'authentification de votre bot
TOKEN = discord_token

# Le token d'authentification de l'API Uptime Robot
UPTIME_API_KEY = uptime_api_key

# Préfixe pour les commandes du bot
COMMAND_PREFIX = '!'
