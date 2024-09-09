from datetime import datetime
import json
import pytz

tz = pytz.timezone('Europe/Paris')


def get_logs_path() -> str:
  now = datetime.now(tz)
  return f"logs/{now.day}-{now.month}-{now.year}.txt"


# query
# values


def logs(id: str):
  now = datetime.now(tz)
  path = f"logs/{now.day}-{now.month}-{now.year}.txt"
  time = f"[{now.hour}:{now.minute}:{now.second}]"

  with open('ressources/logs.json', 'r', encoding='utf-8') as file:
    data = json.load(file)[id]

  with open(path, "a") as file:
    file.write(f"{time} - [{data['type']}] > {' '.join(data['content'])}\n")
