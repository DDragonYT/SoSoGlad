from datetime import date
from userdata import *
from random import randint
from embed import *
from badge import *
from crate import *
from item import *
from wallet import *
from enum import Enum
import discord
RECIPES = json.load(open("recipes.json","wb")) 

async def craft(self,message):
    userdata = get_userdata(message.author)
    user_rescources = userdata["resources"]
    user_items = userdata["inventory"]
    command_params = message.content.split(" ")
    target_amount = 1
    if len(command_params) > 1:
        target_item = command_params[1]
        target_recipe = target_item + "_recipe"
        target_amount = command_params[2]
        if target_recipe in RECIPES.keys():
            current_recipe = RECIPES[target_recipe]
            items_needed = current_recipe["items_needed"]
            for item in items_needed.keys():
                if item in user_rescources:
                    if user_rescources[item] >= items_needed[item]*target_amount:
                        user_rescources[item] -= items_needed[item]*target_amount
                        user_items[target_item] += target_amount
                        embed = discord.Embed(title=f"You succesfully crafted {target_amount} {target_item}", colour=discord.Colour.green())
                        await message.reply(embed=embed)
                    else:
                        await message.reply(embed=gen_error(f"You do not have enough resources to craft {target_amount} {target_item}"))
        else:
            await message.reply(embed=gen_error("This item cannot be crafted"))