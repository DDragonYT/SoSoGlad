from userdata import *
import discord
from item import *

async def pet_info(self, message):
    """Checks if a pet exists, if it does generate an embed and send it"""
    await item_info(self, message, "pet")

def add_pet(id, qty, user, level = 0):
    userdata = get_userdata(user)
    if not "pets" in userdata.keys():
        userdata["pets"] = []
    if not id in userdata["pets"]:
        for i in range(qty):
            userdata["pets"].append(
            {
                "id":id,
                "name": get_itemdata(id)["name"],
                "level":level
                "xp" : 0
            }
            )
        set_userdata(user, userdata)
    else:
        pet_data = get_itemdata(id)
        if userdata["pets"][id]["level"] < pet_data[id].max_level:
            userdata["pets"][id]["xp"] += 10
            
        set_userdata(user, userdata)

async def show_pets(self, message, target = 2):
    command = str(message.content).split(" ")
    if len(command) > target:
        target = command[len(command) - 1]
        if "<" in target:
            user_id = int(target.strip("<>@"))
            target = self.get_user(user_id)
    else:
        target = message.author
    userdata = get_userdata(target)
    if "pets" in userdata.keys():
        userinv = userdata["pets"]
        embed = discord.Embed(
            title=f"{target}'s Pets", colour=discord.Colour.orange()
        )
        output = ""
        for petobj in userinv:
            pet = petobj["id"]
            itemdata = get_itemdata(pet)
            output += f"""- [{itemdata["icon"]}] {itemdata["name"]} (Level {petobj["level"]})\n"""
        if len(output) == 0:
            await message.reply(embed=gen_error("This player does not have any pets!"))
            return
        embed.description = output
        await message.reply(embed=embed)
    else:
        await message.reply(embed=gen_error("This player does not have any pets!"))

async def equip_pet(self, message, target=2):
    userdata = get_userdata(message.author)
    userkeys = userdata.keys()
    command = str(message.content).split(" ")
    if not "eqipped_pet" in userkeys:
        userdata["equipped_pet"] = "none"

    target = command[1]
    pet_data = get_itemdata()
    if target in pet_data():
        if target in userdata["pets"]:
            userdata["equipped_pet"] = target
            embed = discord.Embed(
                title=f"{pet_data[target]["name"]} Equipped", colour=discord.Colour.green()
            )
        else:
            embed = discord.Embed(
                title=f"You do not own a {pet_data[target]["name"]}", colour=discord.Colour.red()
            )
    else:
        embed = discord.Embed(
            title=f"{target} does not exist", colour=discord.Colour.red()
        )
    await message.reply(embed=embed)
    set_userdata(message.author, userdata)