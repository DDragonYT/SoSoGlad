from json import load
from embed import gen_error
from userdata import get_userdata
import discord

ITEM_ICONS = {  # Used to define what icon an item type should have
    "lolly": "🍭",
    "minion": "😈",
    "pet": "🐕",
    "booster": "🔋",
    "crate": "🎁",
    "equipment": "🗡️",
    "trinket": "📿",
    "currency": "💰",
    "resource":"🪵"
}

def get_itemdata(itemname=None):
    with open("items.json", "rb") as itemjson:
        if itemname:
            return load(itemjson)[itemname]
        else:
            return load(itemjson)

def item_details(itemid, show_type = True, title = ""):
    embed = discord.Embed(title=title, colour=discord.Colour.orange())
    itemdata = get_itemdata(itemid)
    embed.add_field(name="Item Name", value=itemdata["name"])
    embed.add_field(name="Rarity", value=itemdata["rarity"].capitalize())
    if show_type:
        embed.add_field(name="Type", value=itemdata["type"].capitalize())
        
    if "image" in itemdata.keys():
        embed.set_thumbnail(url=itemdata["image"])
    return embed
