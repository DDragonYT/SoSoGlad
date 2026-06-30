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
            if userinv[item]["quantity"] > 0:

                output += f"""- [{ITEM_ICONS[itemdata["type"]]}] {itemdata["name"]} x {userinv[item]["quantity"]} \n"""
        if len(output) == 0:
            await message.reply(embed=gen_error("This player does not have an inventory!"))
            return
        embed.description = output
        await message.reply(embed=embed)
    else:
        await message.reply(embed=gen_error("This player does not have an inventory!"))


def consume_item(item, user, userdata, qty=1):
    userdata["inventory"][item]["quantity"] -= qty
    set_userdata(user, userdata)

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
    if userinv[item]["quantity"] == 0:
        await message.reply(embed=gen_error("You do not own any copies of this item."))
        return
    if get_itemdata(item)["type"] == "crate":
        consume_item(item, message.author, userdata)
        await open_crate(self, message, item)
    else:
        await message.reply(embed = gen_error("This item is not useable"))