import json
from datetime import datetime

import pytz
import contextlib

tz = pytz.timezone('Europe/Paris')


def get_logs_path() -> str:
  now = datetime.now(tz)
  return f"logs/{now.day}-{now.month}-{now.year}.log"


def get_logs_time() -> str:
  now = datetime.now(tz)
  return f"[{now.hour}:{now.minute}:{now.second}]"


# query
# values


def logs(id: str, values: dict = None):
  path = get_logs_path()
  time = get_logs_time()

  with open('ressources/logs.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

  content = ' '.join(data[id]['content'])
  with contextlib.suppress(Exception):
    content = content.format(**values)
  with open(path, "a") as file:
    file.write("‎\n")
    file.write(f"‎{time} - [{data[id]['type']}] > {content}\n")
