from json import load
from _ssg_utils import gen_error, get_userdata
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
    "resource": "🪵",
}


def item_search(name, type=False):
    """I dunno"""
    item_data = get_itemdata()
    if name in item_data.keys():
        if type == "item":
            return name
        if item_data[name]["type"] == type:
            return name
    else:
        for key in item_data.keys():
            item = item_data[key]
            if name in item["name"].lower():
                if item_data[item["name"].lower()]["type"] == type:
                    return name
    return


def gen_item_list(itemdata):
    item_displ = ""
    for item in itemdata.keys():
        item_qty = itemdata[item]
        iteminfo = get_itemdata(item)
        item_displ += f"- [{iteminfo["icon"]}] {iteminfo["name"]} x {item_qty}\n"
    return item_displ


def get_itemdata(itemname=None):
    with open("resources/data/items.json", "rb") as itemjson:
        if itemname:
            return load(itemjson)[itemname]
        else:
            return load(itemjson)


def get_recipedata(itemname=None):
    itemrecipe = itemname = itemname + "_recipe"
    with open("resources/data/recipes.json", "rb") as itemjson:
        itemjson = load(itemjson)

        print(itemjson)
        print(itemname)

        if itemname:
            if itemrecipe in itemjson.keys():
                return itemjson[itemrecipe]
            else:
                return None
        else:
            return itemjson


def item_details(itemid, show_type=True, title="", description=""):
    embed = discord.Embed(
        title=title, colour=discord.Colour.orange(), description=description
    )
    itemdata = get_itemdata(itemid)
    recipedata = get_recipedata(itemid)
    embed.add_field(name="Item Name", value=itemdata["name"])
    embed.add_field(name="Rarity", value=itemdata["rarity"].capitalize())
    if show_type:
        embed.add_field(name="Type", value=itemdata["type"].capitalize())
    if "image" in itemdata.keys():
        embed.set_thumbnail(url=itemdata["image"])
    if recipedata:
        embed.add_field(name="Recipe", value=gen_item_list(recipedata["items_needed"]))
    return embed


async def item_info(self, message, type="item"):
    """Checks if an item exists, if it does generate an embed and send it"""
    command_params = message.content.split(" ")

    if len(command_params) > 1:
        item = item_search(command_params[1], type=type)
        if item:
            ipet = item
            embed = item_details(ipet)
            await message.reply(embed=embed)
        else:
            await message.reply(embed=gen_error(f"That {type} doesn't exist!"))
    else:
        await message.reply(embed=gen_error(f"Please a valid {type} name."))
