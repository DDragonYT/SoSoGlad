from _globalvars import *
from _ssg_utils import gen_error


from PIL import Image
import os
import json
import scrython
from random import randint
from userdata import *
import discord

def display_binder(set_name):
    cards = os.listdir(f"{CARD_IMAGE}/{set_name}/")
    print(cards)

    columns = 20
    rows = int(len(cards) / columns)

    card = cards[(0)]
    new_im = Image.open(f"{CARD_IMAGE}/{set_name}/{card}")
    im_w = new_im.width
    im_h = new_im.height
    full_height = im_h * rows
    full_width = im_w * columns

    new_im = Image.new("RGB", (full_width, full_height))
    c = 0
    for i in range(0, columns):
        for j in range(0, rows):

            card = cards[c]
            c += 1
            im = Image.open(f"{CARD_IMAGE}/{set_name}/{card}")
            new_im.paste(im, (i * im_w, j * im_h))

    return new_im


def get_set_data(set: MTGPack):
    with open("resources/data/cards.json", "r") as cardj:
        return json.load(cardj)[set]


def get_card_image(cardname, set_name):
    new_im = f"""{CARD_IMAGE}/{set_name}/{cardname}.full.jpg"""
    return new_im


def get_card_list():
    sets = os.listdir(f"{CARD_IMAGE}/")
    if os.path.isfile("cards.json"):
        with open("resources/data/cards.json", "r") as cards:
            card_json = json.load(cards)
    else:
        card_json = {}
    for mtg_set in sets:

        if not mtg_set in card_json.keys():
            card_json[mtg_set] = {}
            for rarity in RARITIES:
                try:
                    search_results = scrython.cards.Search(
                        q=f"set:{mtg_set} rarity:{rarity}"
                    )
                    card_json[mtg_set][rarity] = []
                    for cardinfo in search_results.iter_all():
                        print(cardinfo)
                        card_json[mtg_set][cardinfo.name] = {
                            "rarity": cardinfo.rarity,
                            "color_identity": cardinfo.color_identity,
                            "mana_cost": cardinfo.mana_cost,
                            "artist": cardinfo.artist,
                            "type_line": cardinfo.type_line,
                            "oracle_text": cardinfo.oracle_text,
                        }
                        card_json[mtg_set][rarity].append(cardinfo.name)
                except:
                    print(f"there are no {rarity} from this set")
    with open("cards.json", "w") as f:
        json.dump(card_json, f)


def get_random_card(rarity, mtg_pack):
    raritydata = get_set_data(mtg_pack)[rarity]
    card_amt = len(raritydata)
    card = raritydata[randint(0, card_amt - 1)]
    return card


def get_rarity(weight, pack: MTGPack):
    roll: float = (randint(1, 1000000) / 10000) + weight
    value = 0
    print(pack.rarity_chances)
    for rarityroll in pack.rarity_chances[0]:
        if roll > rarityroll:
            print(RARITIES[value])
            return RARITIES[value]
        value += 1


def open_pack(pack, user: str, weight: float = 0):
    packobj = PACKS[pack]
    rarity = get_rarity(weight, packobj)
    card = get_random_card(rarity, pack)
    return card, rarity


async def attempt_open_pack(self, message):
    user = message.author
    command_params = message.content.split(" ")

    if len(command_params) < 2:
        await message.reply(embed=gen_error("Please supply a pack ID."))
        return
    else:
        pack = command_params[1].upper()
    if not pack in PACKS.keys():
        await message.reply(embed=gen_error("That is not a valid pack ID."))
        return
    else:
        packobj = PACKS[pack]
        userdata = get_userdata(user)
    if userdata["coins"] < packobj.price:
        await message.reply(
            embed=gen_error(
                f"You do not have the {packobj.price} coins required to make this purchase. (You have: {userdata["coins"]})"
            )
        )
        return
    else:
        cardname, cardrarity = open_pack(pack, message.author, 0)
        embed = discord.Embed(
            title=f"{message.author} opened a {packobj.name} Pack!",
            color=discord.Colour.orange(),
            description=f"They got a {cardname}, it's a {cardrarity}!",
        )
        card_image = "!sososad.png"
        card_image = get_card_image(cardname, pack)
        embed.set_thumbnail(
            url=f"attachment://{discord.File(fp=packobj.image).filename}"
        )
        embed.set_image(
                    url=f"attachment://{discord.File(fp=get_card_image(cardname, pack)).filename}"
                )
        await message.reply(
            embed=embed, file=discord.File(card_image), 
        )


async def show_packs(self, message):
    embed = discord.Embed(title=f"Pack Shop", colour=discord.Colour.orange())
    for pack in PACKS.keys():
        packdata: MTGPack = PACKS[pack]
        value = f"""Cost: {packdata.price} 🪙
ID: `{packdata.id}`
DESCRIPTION: `{packdata.description}`
"""
        embed.add_field(
            name=f"[{packdata.id}] {packdata.name} Pack",
            value=value,
        )
    embed.set_thumbnail(
        url="https://static.wikia.nocookie.net/mtgsalvation_gamepedia/images/6/6d/Unlimited_booster.jpg/revision/latest?cb=20131109150010"
    )
    await message.reply(embed=embed)


if __name__ == "__main__":
    print(open_pack("2ED", "ddragonyt"))
