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

RECIPES:dict = json.load(open("recipes.json", "r"))

async def show_recipe(self,message):
    command_params:list = message.content.split(" ")
    if len(command_params) > 1:
        requested_item:str = command_params[1]
        requested_recipe:str = requested_item + "_recipe"
        if requested_recipe in RECIPES.keys():
            current_recipe_requested:dict = RECIPES[requested_recipe]
            required_items:dict = current_recipe_requested["items_needed"]
            embed = embed.Discord(title=f"{required_items}", colour = discord.Colour.blue)
            await message.reply(embed = embed)
        else:
            await message.reply(embed = gen_error(f"{requested_item} cannot be crafted"))
    else:
        await message.reply(embed = gen_error("Target something dumbass"))
        
    

async def craft(self, message):
    userdata:dict = get_userdata(message.author)
    user_resources:dict = userdata["resources"]
    user_inv:dict = userdata["inventory"]
    command_params:list = message.content.split(" ")
    target_amount = 1

    if len(command_params) > 1:
        target_item:str = command_params[1]
        target_recipe:str = target_item + "_recipe"
        if len(command_params) > 2:
            try:
                target_amount:int = int(command_params[2])
            except:
                message.reply(embed = gen_error("That is not a valid quantity."))
                return
        else:
            target_amount = 1

        if target_recipe in RECIPES.keys():
            current_recipe:dict = RECIPES[target_recipe]
            items_needed:dict = current_recipe["items_needed"]

            for item in items_needed.keys():
                if item in user_resources:
                    if user_resources[item]["quantity"] >= items_needed[item] * target_amount:
                        user_resources[item]["quantity"] -= items_needed[item] * target_amount
                    
                    else:
                        await message.reply(
                            embed=gen_error(
                                f"You do not have enough resources to craft {target_amount} {target_item}"
                            )
                        )
                        return
            if target_item in user_inv.keys():
                user_inv[target_item]["quantity"] += target_amount
            else:
                user_inv[target_item] = {"quantity":target_amount}
            set_userdata(message.author, userdata)
            embed = discord.Embed(
                            title=f"You succesfully crafted {target_amount} {target_item}",
                            colour=discord.Colour.green(),
                        )
            await message.reply(embed=embed)
        else:
            await message.reply(embed=gen_error("This item cannot be crafted"))
