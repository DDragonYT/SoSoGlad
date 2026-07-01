from random import randint
from item import get_itemdata, item_details
import discord
from pet import add_pet

# All crates besides basic and pet are currently unobtainable
CRATES = {
    "pet_crate": {
        "common": {
            "chance": 72,
            "options": ["dog", "cat", "fish", "bird", "monkey", "mouse", "pig"],
        },
        "rare": {
            "chance": 21,
            "options": [
                "gorilla",
                "tiger",
                "horse",
            ],
        },
        "epic": {
            "chance": 5,
            "options": [
                "orangutan",
                "lion",
                "whale",
            ],
        },
        "legendary": {"chance": 0.9, "options": ["shark", "moose", "zebra"]},
        "mythic": {"chance": 0.09, "options": ["pheonix", "dragon", "t-rex"]},
        "godly": {"chance": 0.01, "options": ["unicorn"]},
    },

    "basic_crate": {
        "common": {
            "chance": 100,
            "options": ["pet_crate"],
        },
    }
}


def apply_luck_mult(crate, luck_mult):
    if luck_mult != 0:
        total_chance = 0
        for rarity in crate.keys():
            if rarity != "common":
                crate[rarity]["chance"] = crate[rarity]["chance"] * luck_mult
                total_chance += crate[rarity]["chance"]
        crate["common"]["chance"] = 100 - total_chance
        return crate
    else:
        return crate


def get_crate_result(crate, luck_multiplier=1):
    crate = CRATES[crate].copy()
    mod_crate = apply_luck_mult(crate, luck_multiplier)
    roll = randint(1, 1000000) / 10000
    totalraritychance = 0

    print(f"{roll=}")
    for rarity in mod_crate.keys():
        craterarity = mod_crate[rarity]
        totalraritychance += craterarity["chance"]
        if roll < totalraritychance:
            options = crate[rarity]["options"]
            rolled_item = options[randint(0, len(options) - 1)]
            return (rolled_item, rarity)


result, rarity = get_crate_result("pet_crate")
print(result)

async def open_crate(self, message, item):
    embed = discord.Embed(
        title=f"Opening a {get_itemdata(item)["name"]}...",
        colour=discord.Colour.orange(),
    )
    await message.reply(embed=embed)
    acquired_item, item_rarity = get_crate_result(item)

    itemdata = get_itemdata(acquired_item)
    itemname = itemdata["name"]
    if itemdata["type"] == "pet":
        add_pet(id = acquired_item, qty = 1, level = 1, user = message.author)
    description = ""
    if item_rarity != "common":
        description = f"Woah! It's a {item_rarity}! "
    else:
        description = ""
    description += f"{message.author.mention} got {itemname} from a {get_itemdata(item)["name"]}!"
    embed = item_details(itemid = acquired_item, title = "Crate Result", description = description)
    await message.reply(embed = embed)

    
    await message.channel.send(embed=embed)
