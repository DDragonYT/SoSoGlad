from _ssg_utils import gen_error, get_userdata, set_userdata
from _globalvars import ITEM_IMAGE, SHINY_ODDS

from random import randint
from item import get_itemdata, item_details
import discord
from pet import add_pet
from wallet import add_to_inv
from crate_calcs import *

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
    },
}


async def open_crate(self, message: discord.Message, item):
    acquired_item, item_rarity, quantity = get_crate_result(CRATES, item, 1)

    itemdata = get_itemdata(acquired_item)
    itemname = itemdata["name"]

    description = ""
    if item_rarity != "common":
        description = f"Woah! It's a {item_rarity}! "
    else:
        description = ""

    if itemdata["type"] == "pet":
        convertxp, shiny = await add_pet(
            message=message, id=acquired_item, qty=1, level=1, user=message.author
        )
    else:
        add_to_inv(
            user=message.author,
            userdata=get_userdata(message.author),
            quantity=1,
            item=acquired_item,
        )

    description += (
        f"{message.author.mention} got {itemname} from a {get_itemdata(item)["name"]}!"
    )

    if shiny:
        description += (f"\n[1/{SHINY_ODDS}] SHINY PET!")

    if convertxp:
        description += (f"\nIt was converted into xp, as it's a duplicate.")

    embed, image = item_details(
        itemid=acquired_item, title="Crate Result", description=description
    )
    crate_image = discord.File(fp=f"""{ITEM_IMAGE}/{get_itemdata(item)["image"]}.png""")
    embed.set_thumbnail(url=f"attachment://{crate_image.filename}")
    await message.reply(embed=embed, file=image)
