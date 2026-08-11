import discord
from discord import app_commands
from profile import *
from random import randint
import asyncio
from embed import *
from item import get_itemdata
from crate_calcs import *

action_using = {}
GATHERABLE_TYPES = {
    "stone": {
        "toughness":5,
        "icon":"🪨",
        "common": {
            "chance": 69,
            "options": [{"item":"stone","min_qty":2,"max_qty":4}],
        },
        "uncommon": {
            "chance": 28,
            "options": [
                {"item":"crystal","min_qty":1,"max_qty":3}
            ],
        },
        "epic": {
            "chance": 3,
            "options": [
                {"item":"artifact","min_qty":1,"max_qty":1}
            ],
        }
    },
    "greenery": {
        "toughness": 3,
        "icon":"🪴",
        "common": {
            "chance": 65,
            "options": [{"item":"fern","min_qty":3,"max_qty":5}],
        },
        "uncommon": {
            "chance": 25,
            "options": [
                {"item":"flower","min_qty":1,"max_qty":3},
                {"item":"cotton","min_qty":2,"max_qty":4}
            ],
        },
        "rare": {
            "chance": 10,
            "options": [
                {"item":"basic_crate","min_qty":1,"max_qty":2}
            ],
        }
    }
}


async def gather(self, message):
    command_params = message.content.split(" ")
    if message.author.name in action_using.keys():
        if action_using[message.author.name]:
            await message.reply(embed=gen_error("You are already busy."))
            return
    if command_params[1].lower() in GATHERABLE_TYPES.keys():

        gather_type = command_params[1].lower()
        gatherdata = GATHERABLE_TYPES[gather_type]
        rolled_item, rarity, quantity = get_crate_result(
            GATHERABLE_TYPES, gather_type, 1
        )

        embed = discord.Embed(
            title=f"Gathering {gather_type}... {gatherdata["icon"]}",
            description=f"(Please wait {gatherdata["toughness"]*1} to {gatherdata["toughness"]*2} seconds)",
        )
        await message.reply(embed=embed)
        action_using[message.author.name] = True
        sleep_time = randint(gatherdata["toughness"] * 2, gatherdata["toughness"] * 3)
        await asyncio.sleep(sleep_time)

        action_using[message.author.name] = False

        if rarity != "common":
            rarity_dialogue = f"{rarity.capitalize()} DROP. "
        else:
            rarity_dialogue = None
        embed = discord.Embed(
            title=f"You finished gathering {gather_type}! {gatherdata["icon"]}",
            description=f"{rarity_dialogue if rarity_dialogue else ""}You got {rolled_item} x {quantity}.",
        )
        await message.reply(embed=embed)
        if get_itemdata(rolled_item)["type"] == "resource":
            add_to_resource(message.author, rolled_item, quantity)
        if get_itemdata(rolled_item)["type"] == "crate":
            add_to_inv(message.author, get_userdata(message.author), rolled_item, quantity)




def add_to_resource(user, resource, quantity=1):
    userdata = get_userdata(user)
    if not "resources" in userdata.keys():
        userdata["resources"] = {}
    if not resource in userdata["resources"]:
        userdata["resources"][resource] = {"quantity": 0}
    userdata["resources"][resource]["quantity"] += quantity
    set_userdata(user, userdata)


async def show_resources(self, message, target=1):
    command = str(message.content).split(" ")
    if len(command) > target:
        target = command[1]
        if "<" in target:
            user_id = int(target.strip("<>@"))
            target = self.get_user(user_id)
    else:
        target = message.author

    userdata = get_userdata(target)
    if "resources" in userdata.keys():
        userinv = userdata["resources"]
        embed = discord.Embed(
            title=f"{target}'s Resources", colour=discord.Colour.orange()
        )
        output = ""
        for item in userinv.keys():
            itemdata = get_itemdata(item)
            if userinv[item]["quantity"] > 0:

                output += f"""- [{itemdata["icon"]}] {itemdata["name"]} x {userinv[item]["quantity"]} \n"""
        if len(output) == 0:
            await message.reply(
                embed=gen_error("This player does not have any resources!")
            )
            return
        embed.description = output
        await message.reply(embed=embed)
    else:
        await message.reply(embed=gen_error("This player does not have any resources!"))

