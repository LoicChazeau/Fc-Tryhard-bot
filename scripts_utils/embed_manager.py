import json

from discord import Embed


async def get_embed(category: str, id: str) -> Embed:
    with open('ressources/embed.json', 'r', encoding='utf-8') as file:
        data = json.load(file)[category]
    try:
        embed = Embed(title=data[id]["title"],
                      description="".join(data[id]["description"]),
                      color=int(data[id]["color"], 16))
    except Exception as e:
        print("")
        print(f"> {e} <")
        print(
            f"[ERROR] > scripts_manager.embed_manager.py -> get_embed({category}, {id}))"
        )
        print("")
        return None
    print("")
    print(
        f"[SUCCESS] > scripts_manager.embed_manager.py -> get_embed({category}, {id}))"
    )
    print(f"-> {embed}")
    print("")
    return embed
