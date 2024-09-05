from datetime import datetime, timedelta

import discord
import pytz
from discord import Embed, app_commands
from discord.ext import commands, tasks
from database import add_user, user_exists, remove_user, get_all_users, update_quest_status, update_vote_status, update_pets_status

from blocaria import methods_vote

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
            if user_exists(interaction.user.id):
                await interaction.response.send_message(
                    "⚠️ - **Vous avez déjà lancé vos notifications personnelles !** ❌",
                    delete_after=5,
                    ephemeral=True)
            else:
                await interaction.response.send_message(
                    "🥳 - **Super ! Vous avez lancé vos notifications personnelles !** ✅",
                    delete_after=5,
                    ephemeral=True)
                add_user(str(interaction.user.id), None, False)
                await send_first_personnal_notifications(interaction.user)


# COMMAND '/leave' : Indicates that the player has leaved the server
class Leave(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="leave",
        description="Indicates that the player has leaved the server")
    async def leave(self, interaction: discord.Interaction):
        if user_exists(interaction.user.id):
            await interaction.response.send_message(
                "🥳 - **Super ! Vous avez stoppé vos notifications personnelles !** ✅",
                delete_after=5,
                ephemeral=True)
            remove_user(interaction.user.id)
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
        onlines = get_all_users()  # Récupérer tous les utilisateurs de la base
        for user_id, user_data in onlines.items():
            update_vote_status(user_id, {"vote1_completed": False, "vote2_completed": False})  # Remettre le statut des votes à False

    @tasks.loop(minutes=1)  # Vérifie toutes les minutes
    async def personnal_notifications(self):
        await self.bot.wait_until_ready()

        # Obtenir tous les utilisateurs de la base de données
        onlines = get_all_users()

        if len(onlines) > 0:
            for key, value in onlines.items():
                now = datetime.now(tz)
                user = await self.bot.fetch_user(int(key))
                user_id = user.id

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
                    update_pets_status(key, now.isoformat())  # Met à jour l'heure du dernier rappel des pets

                # VOTES
                pseudo = value[0]

                available_vote_data = methods_vote.get_roles_status(pseudo)
                # print(f"\nPSEUDO = {pseudo}\n{available_vote_data}\n")

                for keys in available_vote_data:
                    if keys['id'] == "serveur-prive":
                        if keys['available'] is True:
                            if not value['vote1_completed']:
                                update_vote_status(key, {"vote1_completed": True})
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
                            update_vote_status(key, {"vote1_completed": False})
                    if keys['id'] == "serveurminecraft":
                        if keys['available'] is True:
                            if not value['vote2_completed']:
                                update_vote_status(key, {"vote2_completed": True})
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
                            update_vote_status(key, {"vote2_completed": False})

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
                    update_quest_status(user_id, {"registered_id": message.id, "quest_completed": False})

                if now.hour == 15 and now.minute == 00 and value['quest_completed']:
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
                    update_quest_status(user_id, {"registered_id": message.id, "quest_completed": False})

                if now.hour == 20 and now.minute == 00 and not value['quest_completed']:
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
                    update_quest_status(user_id, {"registered_id": message.id, "quest_completed": False})



async def setup(bot):
    await bot.add_cog(PersonnalNotifications(bot))
    await bot.add_cog(Join(bot))
    await bot.add_cog(Leave(bot))
