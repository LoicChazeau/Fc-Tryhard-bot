from datetime import datetime, timedelta

import discord
import pytz
from discord import Embed, app_commands
from discord.ext import commands, tasks
from replit import db

from blocaria import methods_vote

if "onlines" not in db:
    db["onlines"] = {}
# db["onlines"] = {}

tz = pytz.timezone('Europe/Paris')


# COMMAND '/join' : Indicates that the player has joined the server
class Join(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="join",
        description="Indicates that the player has joined the server")
    async def join(self, interaction: discord.Interaction, pseudo: str):
        if pseudo is not None:
            if f"{interaction.user.id}" in db["onlines"]:
                await interaction.response.send_message(
                    "⚠️ - **Vous avez déjà lancé vos notifications personnelles !** ❌",
                    delete_after=5,
                    ephemeral=True)
            else:
                await interaction.response.send_message(
                    "🥳 - **Super ! Vous avez lancé vos notifications personnelles !** ✅",
                    delete_after=5,
                    ephemeral=True)
                db["onlines"][f"{interaction.user.id}"] = (
                    pseudo, datetime.now(tz).isoformat(), False, False, None,
                    False)
                await send_first_personnal_notifications(interaction.user)
        else:
            await interaction.response.send_message(
                "⚠️ - **Vous devez spécifier un pseudo !** ❌",
                delete_after=5,
                ephemeral=True)


# COMMAND '/leave' : Indicates that the player has leaved the server
class Leave(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="leave",
        description="Indicates that the player has leaved the server")
    async def leave(self, interaction: discord.Interaction):
        if f"{interaction.user.id}" in db["onlines"]:
            await interaction.response.send_message(
                "🥳 - **Super ! Vous avez stoppé vos notifications personnelles !** ✅",
                delete_after=5,
                ephemeral=True)
            db["onlines"].pop(f"{interaction.user.id}")
        else:
            await interaction.response.send_message(
                "⚠️ - **Vous n'avez pas lancé vos notifications personnelles !** ❌",
                delete_after=5,
                ephemeral=True)


# Send the first personnal notification
async def send_first_personnal_notifications(user):
    embed = Embed(
        title="Première notification personnelle",
        description=("Salut,\n\n"
                     "Tu viens d'activer tes notifications personnelles !\n"
                     "Bonne session de jeu ! 😄\n\n"
                     "Aujourd'hui, pense bien à : \n"
                     "- Tes pets -> /pets\n"
                     "- Tes 2 votes -> /vote\n"
                     "- Tes récompenses -> /rewards\n"
                     "- Ton vip -> /vip\n"
                     "- Ta quête journalière -> /jobs\n\n"
                     "Bonne session 😘"),
        color=0x00ff00)
    await user.send(f"{user.mention}", embed=embed)


# Send the looped personnal notifications
class PersonnalNotifications(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.personnal_notifications.start()
        self.reset_votes_timers.start()

    async def cog_unload(self):
        self.personnal_notifications.cancel()
        self.reset_votes_timers.cancel()

    @tasks.loop(minutes=30)
    async def reset_votes_timers(self):
        await self.bot.wait_until_ready()
        if len(db["onlines"]) > 0:
            for key in db["onlines"].items():
                db["onlines"][key][2] = False
                db["onlines"][key][3] = False

    @tasks.loop(minutes=1)  # Vérifie toutes les minutes
    async def personnal_notifications(self):
        await self.bot.wait_until_ready()

        if len(db["onlines"]) > 0:
            for key, value in db["onlines"].items():
                now = datetime.now(tz)
                user = await self.bot.fetch_user(int(key))

                # 3h00 : PETS
                elapsed = now - datetime.fromisoformat(value[1])
                if elapsed >= timedelta(hours=3):
                    embed = Embed(
                        title="Rappel des pets",
                        description=("Salut,\n\n"
                                     "C'est l'heure d'aller check tes pets !\n"
                                     "J'espère qu'ils sont pleins 😄\n\n"
                                     "À plus ! 😘"),
                        color=0x00ff00)
                    await user.send(f"{user.mention}", embed=embed)
                    db["onlines"][key][1] = now.isoformat()

                # VOTES
                pseudo = value[0]

                available_vote_data = methods_vote.get_roles_status(pseudo)
                # print(f"\nPSEUDO = {pseudo}\n{available_vote_data}\n")

                for keys in available_vote_data:
                    if keys['id'] == "serveur-prive":
                        if keys['available'] is True:
                            if value[2] is False:
                                db["onlines"][key][2] = True
                                embed = Embed(
                                    title="Rappel du vote #1",
                                    description=(
                                        "Salut,\n\n"
                                        "C'est l'heure d'aller voter !\n"
                                        "N'oublie pas le vote #1 😄\n\n"
                                        "À plus ! 😘"),
                                    color=0x00ff00)
                                await user.send(
                                    f"{user.mention}, [vote en cliquant ici](https://blocaria.fr/vote)",
                                    embed=embed)
                        else:
                            db["onlines"][key][2] = False
                    if keys['id'] == "serveurminecraft":
                        if keys['available'] is True:
                            if value[3] is False:
                                db["onlines"][key][3] = True
                                embed = Embed(
                                    title="Rappel du vote #2",
                                    description=(
                                        "Salut,\n\n"
                                        "C'est l'heure d'aller voter !\n"
                                        "N'oublie pas le vote #2 😄\n\n"
                                        "À plus ! 😘"),
                                    color=0x00ff00)
                                await user.send(
                                    f"{user.mention}, [vote en cliquant ici](https://blocaria.fr/vote)",
                                    embed=embed)
                        else:
                            db["onlines"][key][3] = False

                # VIP & REWARDS NOTIFICATION
                if now.hour == 23 and now.minute == 00:

                    print("[VIP & REWARDS NOTIFICATION] Vip & Rewards notif")
                    embed = Embed(
                        title="Notification vip & rewards 23:00",
                        description=("Salut,\n\n"
                                     "Il est 23:00 ! (et oui déjà...)\n"
                                     "Bientôt la fin de journée 😄\n\n"
                                     "Donc pense bien à : \n"
                                     "- Tes récompenses -> /rewards\n"
                                     "- Ton vip -> /vip\n\n"
                                     "Bonne soirée 😘"),
                        color=0x00ff00)
                    await user.send(f"{user.mention}", embed=embed)

                # JOBS QUEST NOTIFICATION
                if now.hour == 10 and now.minute == 00:
                    print("[JOBS QUEST NOTIFICATION] Jobs quest notif")
                    embed = Embed(
                        title="Notification métier : quête journalière",
                        description=("Salut,\n\n"
                                     "Il est 10:00 !\n"
                                     "J'espère que ça va 😄\n\n"
                                     "Si ce n'est pas fait, pense bien à : \n"
                                     "- faire ta quête journalière de métier\n"
                                     "-> /jobs\n\n"
                                     "Une fois ta quête journalière terminée,"
                                     "**réagis avec l'emoji prédéfini !**"
                                     "Bon jeu 😘"),
                        color=0x00ff00)
                    message = await user.send(f"{user.mention}", embed=embed)
                    await message.add_reaction("✅")
                    db["onlines"][key][4] = f"{message.id}"
                    if db["onlines"][key][5]:
                        db["onlines"][key][5] = False

                if now.hour == 15 and now.minute == 00 and not db["onlines"][
                        key][5]:
                    print("[JOBS QUEST NOTIFICATION] Jobs quest notif")
                    embed = Embed(
                        title="Notification métier : quête journalière",
                        description=("Salut,\n\n"
                                     "Il est 15:00 !\n"
                                     "J'espère que ça va 😄\n\n"
                                     "Si ce n'est pas fait, pense bien à : \n"
                                     "- faire ta quête journalière de métier\n"
                                     "-> /jobs\n\n"
                                     "Une fois ta quête journalière terminée,"
                                     "**réagis avec l'emoji prédéfini !**"
                                     "Bon jeu 😘"),
                        color=0x00ff00)
                    message = await user.send(f"{user.mention}", embed=embed)
                    await message.add_reaction("✅")
                    db["onlines"][key][4] = f"{message.id}"

                if now.hour == 20 and now.minute == 00 and not db["onlines"][
                        key][5]:
                    print("[JOBS QUEST NOTIFICATION] Jobs quest notif")
                    embed = Embed(
                        title="Notification métier : quête journalière",
                        description=("Salut,\n\n"
                                     "Il est 20:00 !\n"
                                     "J'espère que ça va 😄\n\n"
                                     "Si ce n'est pas fait, pense bien à : \n"
                                     "- faire ta quête journalière de métier\n"
                                     "-> /jobs\n\n"
                                     "Une fois ta quête journalière terminée,"
                                     "**réagis avec l'emoji prédéfini !**"
                                     "Bon jeu 😘"),
                        color=0x00ff00)
                    message = await user.send(f"{user.mention}", embed=embed)
                    await message.add_reaction("✅")
                    db["onlines"][key][4] = f"{message.id}"


async def setup(bot):
    await bot.add_cog(PersonnalNotifications(bot))
    await bot.add_cog(Join(bot))
    await bot.add_cog(Leave(bot))
