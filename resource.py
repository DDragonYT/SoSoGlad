import discord
from discord import app_commands
from wallet import *
from random import randint
import asyncio
from embed import *
from item import get_itemdata

action_using = {}
GATHERABLE_TYPES = {
    "stone": {
        "icon":"🪨",
        
        "common": {
            "chance": 80,
            "options": [
                {
                    "item": "stone",
                    "max_qty": 4,
                    "min_qty": 3
                }
            ],
        },

        "uncommon": {
            "chance": 19,
            "options": [
                {
                    "item": "basic_crate",
                    "max_qty": 1,
                    "min_qty": 1,
                }
            ],
        },

        "rare": {
            "chance": 1,
            "options": [
                {
                    "item": "pet_crate",
                    "max_qty": 1,
                    "min_qty": 1,
                }
            ],
        },

        "toughness": 5,
    },

    "wood": {
        "icon":"🪵",
        "drops": [
            {
                "item": "wood",
                "max_qty": 7,
                "min_qty": 5,
            }
        ],
        "toughness": 3,
    },

    "greenery": {
        "icon":"🪻",
        "drops": [
            {
                "item": "flower",
                "max_qty": 1,
                "min_qty": 1,
            },
            {
                "item": "fern",
                "max_qty": 3,
                "min_qty": 2,
            },
        ],
        "toughness": 1,
    },
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

        embed = discord.Embed(title=f"Gathering {gather_type}... {gatherdata["icon"]}", description=f"(Please wait {gatherdata["toughness"]*2} to {gatherdata["toughness"]*3} seconds)")
        await message.reply(embed=embed)
        action_using[message.author.name] = True
        sleep_time = randint(gatherdata["toughness"] * 2, gatherdata["toughness"] * 3)
        await asyncio.sleep(sleep_time)
        
        action_using[message.author.name] = False
        itemgivenpos = randint(0, len(gatherdata["drops"])-1)
        item_given = gatherdata["drops"][itemgivenpos]["item"]
        give_amount = randint(gatherdata["drops"][itemgivenpos]["min_qty"],gatherdata["drops"][itemgivenpos]["max_qty"])
        embed = discord.Embed(title=f"You finished gathering {gather_type}! {gatherdata["icon"]}", description = f"You got {item_given} x {give_amount}.")
        await message.reply(embed=embed)
        add_to_resource(message.author, item_given, give_amount)


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
            await message.reply(embed=gen_error("This player does not have any resources!"))
            return
        embed.description = output
        await message.reply(embed=embed)
    else:
        await message.reply(embed=gen_error("This player does not have any resources!"))
