from datetime import datetime, timedelta

import discord
import pytz
from discord import app_commands
from discord.ext import commands, tasks

from scripts_utils.logs_manager import logs

from blocaria import methods_vote
from database import (add_user_db, get_all_users_db, get_user_db, init_db,
                      remove_user_db, update_user_db, user_exists_db,
                      user_dont_exist_db)
from scripts_utils import embed_manager

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
            if not user_dont_exist_db(interaction.user.id):
                await interaction.response.send_message(
                    "⚠️ - **Vous avez déjà lancé vos notifications personnelles !** ❌",
                    delete_after=5,
                    ephemeral=True)
            else:
                if add_user_db(interaction.user.id, pseudo):
                    await interaction.response.send_message(
                        "🥳 - **Super ! Vous avez lancé vos notifications personnelles !** ✅",
                        delete_after=5,
                        ephemeral=True)
                    await send_first_personnal_notifications(interaction.user)
                    logs(
                        "blocaria_join", {
                            "user_name": str(interaction.user.name),
                            "user_id": str(interaction.user.id),
                            "pseudo": str(pseudo)
                        })


# COMMAND '/leave' : Indicates that the player has leaved the server
class Leave(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="leave",
        description="Indicates that the player has leaved the server")
    async def leave(self, interaction: discord.Interaction):
        if user_exists_db(interaction.user.id):
            if remove_user_db(interaction.user.id):
                await interaction.response.send_message(
                    "🥳 - **Super ! Vous avez stoppé vos notifications personnelles !** ✅",
                    delete_after=5,
                    ephemeral=True)
                logs(
                    "blocaria_leave", {
                        "user_name": str(interaction.user.name),
                        "user_id": str(interaction.user.id)
                    })
        else:
            await interaction.response.send_message(
                "⚠️ - **Vous n'avez pas lancé vos notifications personnelles !** ❌",
                delete_after=5,
                ephemeral=True)


# Send the first personnal notification
async def send_first_personnal_notifications(user):
    embed = await embed_manager.get_embed("blocaria",
                                          "first_personnal_notification")
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
        onlines = get_all_users_db()
        for user_id in onlines:
            update_user_db(user_id, {
                "vote1_completed": False,
                "vote2_completed": False
            })

    @tasks.loop(minutes=1)  # Vérifie toutes les minutes
    async def personnal_notifications(self):
        await self.bot.wait_until_ready()

        # Obtenir tous les utilisateurs de la base de données
        onlines = get_all_users_db()

        if len(onlines) > 0:
            for key, value in onlines.items():
                now = datetime.now(tz)
                user = await self.bot.fetch_user(int(key))
                user_id = user.id

                # 3h00 : PETS
                elapsed = now - datetime.fromisoformat(value["last_pets_time"])
                if elapsed >= timedelta(hours=3):
                    embed = await embed_manager.get_embed("blocaria", "pets")
                    await user.send(f"{user.mention}", embed=embed)
                    update_user_db(key, {"last_pets_time": now.isoformat()})
                    logs("blocaria_pets", {
                        "user_name": str(user.name),
                        "user_id": str(user.id)
                    })

                # VOTES
                pseudo = value["pseudo"]
                available_vote_data = methods_vote.get_roles_status(pseudo)
                print(f"Vote data for {pseudo}: {available_vote_data}")
                
                for keys in available_vote_data:
                    if keys['id'] == "serveur-prive":
                        if keys['available'] is True:
                            if not value['vote1_completed']:
                                update_user_db(key, {"vote1_completed": True})
                                embed = await embed_manager.get_embed(
                                    "blocaria", "vote1")
                                await user.send(
                                    f"{user.mention}, [vote en cliquant ici](https://blocaria.fr/vote)",
                                    embed=embed)
                                logs(
                                    "blocaria_vote", {
                                        "user_name": str(user.name),
                                        "user_id": str(user.id),
                                        "id": str(1)
                                    })
                        else:
                            if value['vote1_completed'] is not False:
                                update_user_db(key, {"vote1_completed": False})
                    if keys['id'] == "serveurminecraft":
                        if keys['available'] is True:
                            if not value['vote2_completed']:
                                update_user_db(key, {"vote2_completed": True})
                                embed = await embed_manager.get_embed(
                                    "blocaria", "vote2")
                                await user.send(
                                    f"{user.mention}, [vote en cliquant ici](https://blocaria.fr/vote)",
                                    embed=embed)
                                logs(
                                    "blocaria_vote", {
                                        "user_name": str(user.name),
                                        "user_id": str(user.id),
                                        "id": str(2)
                                    })
                        else:
                            if value['vote2_completed'] is not False:
                                update_user_db(key, {"vote2_completed": False})

                # VIP & REWARDS NOTIFICATION
                if now.hour == 23 and now.minute == 00:

                    print("[VIP & REWARDS NOTIFICATION] Vip & Rewards notif")
                    embed = await embed_manager.get_embed(
                        "blocaria", "vip_rewards")
                    await user.send(f"{user.mention}", embed=embed)
                    logs("blocaria_vip&rewards", {
                        "user_name": str(user.name),
                        "user_id": str(user.id)
                    })

                # JOBS QUEST NOTIFICATION
                if now.hour == 10 and now.minute == 00:
                    print("[JOBS QUEST NOTIFICATION] Jobs quest notif")
                    embed = await embed_manager.get_embed(
                        "blocaria", "jobs_quest")
                    message = await user.send(f"{user.mention}", embed=embed)
                    await message.add_reaction("✅")
                    update_user_db(user_id, {
                        "registered_id": message.id,
                        "quest_completed": False
                    })
                    logs("blocaria_jobs", {
                        "user_name": str(user.name),
                        "user_id": str(user.id)
                    })

                if now.hour == 15 and now.minute == 00 and value[
                        'quest_completed']:
                    print("[JOBS QUEST NOTIFICATION] Jobs quest notif")
                    embed = await embed_manager.get_embed(
                        "blocaria", "jobs_quest")
                    message = await user.send(f"{user.mention}", embed=embed)
                    await message.add_reaction("✅")
                    update_user_db(user_id, {"registered_id": message.id})
                    logs("blocaria_jobs", {
                        "user_name": str(user.name),
                        "user_id": str(user.id)
                    })

                if now.hour == 20 and now.minute == 00 and not value[
                        'quest_completed']:
                    print("[JOBS QUEST NOTIFICATION] Jobs quest notif")
                    embed = await embed_manager.get_embed(
                        "blocaria", "jobs_quest")
                    message = await user.send(f"{user.mention}", embed=embed)
                    await message.add_reaction("✅")
                    update_user_db(user_id, {"registered_id": message.id})
                    logs("blocaria_jobs", {
                        "user_name": str(user.name),
                        "user_id": str(user.id)
                    })


async def setup(bot):
    await bot.add_cog(PersonnalNotifications(bot))
    await bot.add_cog(Join(bot))
    await bot.add_cog(Leave(bot))
