from flask import Flask, request
import os
import subprocess

app = Flask(__name__)

@app.route('/git-update', methods=['POST'])
def git_update():
    if request.method == 'POST':
        # Aller dans le dossier du projet et faire un git pull
        os.system("cd /home/ec2-user/Fc-Tryhard-bot && git pull")

        # Installer les nouvelles dépendances
        os.system("pip install -r /home/ec2-user/Fc-Tryhard-bot/requirements.txt")

        # Démarrer ou redémarrer le bot
        # restart_bot()
        
        return 'Update and dependencies installation successful', 200
    else:
        return 'Invalid request', 400

def restart_bot():
    # Vérifier si le bot est déjà en cours d'exécution
    bot_running = os.system("pgrep -f main.py") == 0

    if bot_running:
        # Si le bot est en cours d'exécution, le redémarrer
        os.system("pkill -f main.py")

    # Lancer le bot dans un nouvel écran (screen session)
    #os.system("screen -dmS bot_screen python3 /home/ec2-user/Fc-Tryhard-bot/main.py")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
