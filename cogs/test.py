import json
from discord import Embed

async def get_embed(id: str) -> Embed:
    with open('ressources/blocaria_embed.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    title = data[id]["title"]
    description = "".join(data[id]["description"])
    color = data[id]["color"]
    
    embed = Embed(
        title=title,
        description=description,
        color=color)

    return embed