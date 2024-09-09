import datetime

import discord
import pytz
from discord import Embed
from discord.ext import commands, tasks

global_notification_channel_id = 1280142397988405349


class GlobalNotifications(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.global_notifications.start()

    async def cog_unload(self):
        self.global_notifications.cancel()

    @tasks.loop(minutes=1)
    async def global_notifications(self):
        tz = pytz.timezone('Europe/Paris')
        now = datetime.datetime.now(tz)

        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(global_notification_channel_id)
        if channel is None:
            print("Le canal n'a pas été trouvé.")
            return
        role = discord.utils.get(channel.guild.roles,
                                 name="🔔 • Notif - Blocaria")
        if role is None:
            print("Le rôle n'a pas été trouvé.")
            return

        # SUNDAY NOTIFICATION (CAPS REWARDS + VOTE REWARDS)
        if now.weekday() == 6 and now.hour == 20 and now.minute == 0:

            print("[SUNDAY NOTIFICATION] Dimanche 20H notification")
            embed = Embed(
                title="Notification dimanche 20h",
                description=("Salut,\n\n"
                             "Nous sommes dimanche soir ! (et oui déjà...)\n"
                             "C'est le début d'une nouvelle semaine 😄\n\n"
                             "Donc pensez bien à vérifier avant 00h : \n"
                             "- Vos capsules -> /caps\n"
                             "- Vos paliers de vote -> /vote\n\n"
                             "Bonne semaine 😘"),
                color=0x00ff00)
            await channel.send(f"{role.mention}", embed=embed)

        # ANTIQUAIRE NOTIFICATION
        if now.hour == 23 and now.minute == 55:

            print("[ANTIQUAIRE NOTIFICATION] Antiquaire notif")
            embed = Embed(
                title="Notification antiquaire 23:55",
                description=(
                    "Salut,\n\n"
                    "Il est 23:55 ! (et oui déjà...)\n"
                    "Bientôt la fin de journée 😄\n\n"
                    "Donc pensez bien à guetter l'antiquaire pour 00h00 ! \n"
                    "Bonne soirée 😘"),
                color=0x00ff00)
            await channel.send(f"{role.mention}", embed=embed)

        # EVENTS
        # - Tournoi de farm (solo)
        if (now.weekday()
                in (0, 1, 4, 5)) and now.hour == 20 and now.minute == 55:

            print("[EVENT] - Tournoi de farm (solo)")
            embed = Embed(
                title="[EVENT] - Tournoi de farm (solo)",
                description=(
                    "Salut,\n\n"
                    "Il est 20:55 ! Tournoi de farm (solo) dans 5 min !\n"
                    "J'espère que vous serez de la partie 😄\n\n"
                    "**ᴏʙᴊᴇᴄᴛɪꜰ**\n"
                    "Une culture, une créature ou\n"
                    "un bloc est choisi, vous avez\n"
                    "30 minutes pour en récolter.\n\n"
                    "**ʀᴇᴄᴏᴍᴘᴇɴꜱᴇꜱ**\n"
                    ":first_place: ⮞ 500,000 :coin: + 50 :gem:\n"
                    ":second_place: ⮞ 250,000 :coin: + 25 :gem:\n"
                    ":third_place: ⮞ 100,000 :coin: + 5 :gem:\n\n"
                    "Bon farm 😘"),
                color=0x00ff00)
            await channel.send(f"{role.mention}", embed=embed)

        # - Tournoi de farm coop (communautaire)
        if (now.weekday() in (2, 6)) and now.hour == 19 and now.minute == 55:

            print("[EVENT] - Tournoi de farm coop (communautaire)")
            embed = Embed(
                title="[EVENT] - Tournoi de farm coop (communautaire)",
                description=(
                    "Salut,\n\n"
                    "Il est 19:55 ! Tournoi de farm coop (commu) dans 5 min !\n"
                    "J'espère que vous serez de la partie 😄\n\n"
                    "**ᴏʙᴊᴇᴄᴛɪꜰ**\n"
                    "Une culture, une créature ou\n"
                    "un bloc est choisi, vous avez\n"
                    "30 minutes pour en récolter.\n\n"
                    "**ʀᴇᴄᴏᴍᴘᴇɴꜱᴇꜱ**\n"
                    ":first_place: ⮞ 1,000,000 :coin: + 100 :gem:\n"
                    ":second_place: ⮞ 500,000 :coin: + 50 :gem:\n"
                    ":third_place: ⮞ 200,000 :coin: + 10 :gem:\n\n"
                    "Bon farm 😘"),
                color=0x00ff00)
            await channel.send(f"{role.mention}", embed=embed)

        # - Mascotte folle (communautaire)
        if (now.weekday() == 5) and now.hour == 16 and now.minute == 55:

            print("[EVENT] - Mascotte folle (communautaire)")
            embed = Embed(
                title="[EVENT] - Mascotte folle (communautaire)",
                description=(
                    "Salut,\n\n"
                    "Il est 16:55 ! Mascotte folle (commu) dans 5 min !\n"
                    "J'espère que vous serez de la partie 😄\n\n"
                    "**ᴏʙᴊᴇᴄᴛɪꜰ**\n"
                    "Une mascotte apparaît sur la\n"
                    "place centrale, en la tapant\n"
                    "vouc obtiendrez des récompenses.\n\n"
                    "**ʀᴇᴄᴏᴍᴘᴇɴꜱᴇꜱ ᴘᴏꜱꜱɪʙʟᴇꜱ**\n"
                    "⮞ 2,500 :coin:\n"
                    "⮞ Spawner à vache (x1)\n"
                    "⮞ Clé épique (x1)\n"
                    "⮞ Rituel rare (x1)\n"
                    "Et bien plus...\n\n"
                    "Bon farm 😘"),
                color=0x00ff00)
            await channel.send(f"{role.mention}", embed=embed)

        # - Pêche folle (solo)
        if (now.weekday() == 1) and now.hour == 19 and now.minute == 25:

            print("[EVENT] - Pêche folle (solo)")
            embed = Embed(
                title="[EVENT] - Pêche folle (solo)",
                description=("Salut,\n\n"
                             "Il est 19:25 ! Pêche folle (solo) dans 5 min !\n"
                             "J'espère que vous serez de la partie 😄\n\n"
                             "**ᴏʙᴊᴇᴄᴛɪꜰ**\n"
                             "Pendant 15 minutes vous pêchez\n"
                             "des récompenses customisées au\n"
                             "spawn sur la plage.\n\n"
                             "**ʀᴇᴄᴏᴍᴘᴇɴꜱᴇꜱ ᴘᴏꜱꜱɪʙʟᴇꜱ**\n"
                             "⮞ Spawner à vache (x1)\n"
                             "⮞ Clé épique (x1)\n"
                             "⮞ Rituel épique (x1)\n"
                             "⮞ 50,000 :coin:\n"
                             "Et 49 autres...\n\n"
                             "Bon farm 😘"),
                color=0x00ff00)
            await channel.send(f"{role.mention}", embed=embed)
        if (now.weekday() == 6) and now.hour == 16 and now.minute == 25:

            print("[EVENT] - Pêche folle (solo)")
            embed = Embed(
                title="[EVENT] - Pêche folle (solo)",
                description=("Salut,\n\n"
                             "Il est 16:25 ! Pêche folle (solo) dans 5 min !\n"
                             "J'espère que vous serez de la partie 😄\n\n"
                             "**ᴏʙᴊᴇᴄᴛɪꜰ**\n"
                             "Pendant 15 minutes vous pêchez\n"
                             "des récompenses customisées au\n"
                             "spawn sur la plage.\n\n"
                             "**ʀᴇᴄᴏᴍᴘᴇɴꜱᴇꜱ ᴘᴏꜱꜱɪʙʟᴇꜱ**\n"
                             "⮞ Spawner à vache (x1)\n"
                             "⮞ Clé épique (x1)\n"
                             "⮞ Rituel épique (x1)\n"
                             "⮞ 50,000 :coin:\n"
                             "Et 49 autres...\n\n"
                             "Bon farm 😘"),
                color=0x00ff00)
            await channel.send(f"{role.mention}", embed=embed)

        # - Largage (solo)
        if now.hour == 18 and now.minute == 25:

            print("[EVENT] - Largage (solo)")
            embed = Embed(
                title="[EVENT] - Largage (solo)",
                description=("Salut,\n\n"
                             "Il est 18:25 ! Largage (solo) dans 5 min !\n"
                             "J'espère que vous serez de la partie 😄\n\n"
                             "**ᴏʙᴊᴇᴄᴛɪꜰ**\n"
                             "Un total de 25 largages tombent\n"
                             "dans le spawn et vous devrez être\n"
                             "le premier à les récupérer.\n\n"
                             "**ʀᴇᴄᴏᴍᴘᴇɴꜱᴇꜱ ᴘᴏꜱꜱɪʙʟᴇꜱ**\n"
                             "⮞ Rituel épique (x1)\n"
                             "⮞ Clé épique (x1)\n"
                             "⮞ 5 :gem:\n"
                             "Et 21 autres...\n\n"
                             "Bon farm 😘"),
                color=0x00ff00)
            await channel.send(f"{role.mention}", embed=embed)

        # - Evénement communautaire (communautaire)
        if (now.weekday() in (3, 6)) and now.hour == 20 and now.minute == 55:

            print("[EVENT] - Evénement communautaire (communautaire)")
            embed = Embed(
                title="[EVENT] - Evénement communautaire (communautaire)",
                description=(
                    "Salut,\n\n"
                    "Il est 20:55 ! Event communautaire (commu) dans 5 min !\n"
                    "J'espère que vous serez de la partie 😄\n\n"
                    "**ᴏʙᴊᴇᴄᴛɪꜰ**\n"
                    "Une culture, une créature ou\n"
                    "un bloc est choisi ainsi qu'un\n"
                    "montant de récolte et vous devez\n"
                    "le compléter dans le temps imparti.\n\n"
                    "**ʀᴇᴄᴏᴍᴘᴇɴꜱᴇ**\n"
                    "⮞ 250,000 :coin: + 75 :gem:\n\n"
                    "Bon farm 😘"),
                color=0x00ff00)
            await channel.send(f"{role.mention}", embed=embed)

        # - Enchères (communautaire)
        if (now.weekday() in (3, 5)) and now.hour == 18 and now.minute == 55:

            print("[EVENT] - Enchères (communautaire)")
            embed = Embed(
                title="[EVENT] - Enchères (communautaire)",
                description=("Salut,\n\n"
                             "Il est 18:55 ! Enchères (commu) dans 5 min !\n"
                             "J'espère que vous serez de la partie 😄\n\n"
                             "**ᴏʙᴊᴇᴄᴛɪꜰ**\n"
                             "Des objets sont proposés et vous\n"
                             "pouvez enchérir dessus, la meilleure\n"
                             "offre repartira avec.\n\n"
                             "**ʀᴇᴄᴏᴍᴘᴇɴꜱᴇꜱ ᴘᴏꜱꜱɪʙʟᴇꜱ**\n"
                             "⮞ Spawner à vache (x1)\n"
                             "⮞ Clé épique (x1)\n"
                             "⮞ Rituel épique (x1)\n"
                             "⮞ 50,000 :coin:\n"
                             "Et 49 plus...\n\n"
                             "Bon farm 😘"),
                color=0x00ff00)
            await channel.send(f"{role.mention}", embed=embed)

    @global_notifications.before_loop
    async def before_global_notifications(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(GlobalNotifications(bot))
