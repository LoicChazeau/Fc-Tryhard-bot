from datetime import datetime
from database import get_all_users_db
import pytz

tz = pytz.timezone('Europe/Paris')


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


async def ICommand_help(ctx):
    console_logs("info", [
        "-------------------- HELP --------------------",
        "? 'help': send this help message",
        "-------------------- HELP --------------------"
    ])


async def discord_database(ctx):
    bot = ctx["bot"]
    all_users = get_all_users_db()

    desc = ""
    for user_id, user_data in all_users.items():
        desc += f"User ID: {user_id}\n"
        desc += f"Pseudo: {user_data['pseudo']}\n"
        desc += f"Registered ID: {user_data['registered_id']}\n"
        desc += f"Quest Completed: {user_data['quest_completed']}\n"
        desc += f"Vote1 Completed: {user_data.get('vote1_completed', False)}\n"
        desc += f"Vote2 Completed: {user_data.get('vote2_completed', False)}\n"
        desc += f"Last Pets Time: {user_data.get('last_pets_time', 'N/A')}\n"
        desc += "\n"

    if desc != "":
        sections = desc.split("\n")
        for section in sections:
            if section != "":
                console_logs("info", [f"{section}"])
    else:
        console_logs("info", ["Nobody found in the database"])


async def discord_broadcast(ctx):
    bot = ctx["bot"]
    args = ctx["args"]
    message = " ".join(args)
    if len(args) > 0:
        channel = bot.get_channel(1280127733157855357)
        if channel:
            await channel.send(f"@everyone, {message}")
            console_logs("info", [
                f"Message '{message}' envoyé sur le salon '{channel}'",
            ])
        else:
            console_logs("info", ["No channel was found"])
    else:
        console_logs("info", [
            "Incomplete command. See below for error",
            "broadcast [message] <=="
        ])
