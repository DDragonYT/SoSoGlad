from datetime import date
from userdata import *
from random import randint
from embed import *
from badge import calc_inv
from crate import open_crate
from item import *
from wallet import *


async def show_inventory(self, message, target=2):
    command = str(message.content).split(" ")
    if len(command) > target:
        target = command[len(command) - 1]
        if "<" in target:
            user_id = int(target.strip("<>@"))
            target = self.get_user(user_id)
    else:
        target = message.author
    userdata = get_userdata(target)
    if "inventory" in userdata.keys():
        userinv = userdata["inventory"]
        embed = discord.Embed(
            title=f"{target}'s Inventory", colour=discord.Colour.orange()
        )
        output = ""
        for item in userinv.keys():
            itemdata = get_itemdata(item)
            output += f"""- [{ITEM_ICONS[itemdata["type"]]}] {itemdata["name"]} x {userinv[item]["quantity"]} \n"""
        embed.description = output
        await message.reply(embed=embed)
    else:
        await message.reply(embed=gen_error("This player does not have an inventory!"))


async def attempt_use_item(self, message):
    userdata = get_userdata(message.author)
    command = str(message.content).split(" ")
    if len(command) < 2:
        await message.reply(
            embed=gen_error("Please enter the ID of the item you want to use.")
        )
        return
    item = command[1]
    if not item in get_itemdata().keys():
        await message.reply(embed=gen_error("Please enter a valid item ID."))
        return
    if not "inventory" in userdata.keys():
        await message.reply(
            embed=gen_error("You do not have any items in your inventory.")
        )
        return
    userinv = userdata["inventory"]
    if not item in userinv:
        await message.reply(embed=gen_error("You do not own any copies of this item."))
        return
    if get_itemdata(item)["type"] == "crate":
        await open_crate(self, message, item)
