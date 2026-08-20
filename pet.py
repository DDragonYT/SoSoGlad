from _globalvars import *
from _ssg_utils import gen_error, get_userdata, set_userdata, target_from_message

import discord
from item import *
from random import randint

def pet_xp_required(level,rarity):
    mult = PET_RARITY_MULTIPLER[rarity]
    return int(((level / PET_LEVEL_DIVIDER) ** PET_LEVEL_CURVE + PET_LEVEL_BASE)*mult) 

async def pet_info(self, message):
    """Checks if a pet exists, if it does generate an embed and send it"""
    await item_info(self, message, "pet")

async def add_pet(message, id, qty, user, level = 0):
    shininess:bool = (randint(1,SHINY_ODDS) == 1)
    converted_to_xp = False
    userdata = get_userdata(user)
    if not "pets" in userdata.keys():
        userdata["pets"] = {}
    if not id in userdata["pets"]:
        for i in range(qty):
            userdata["pets"][id] = {
                "id":id,
                "name": get_itemdata(id)["name"],
                "level":level,
                "xp" : 0,
                "shiny":shininess
            }

        set_userdata(user, userdata)
    else:
        pet_data = get_itemdata(id)
        if userdata["pets"][id]["level"] < 101:
            converted_to_xp = True
            if shininess:
                userdata["pets"][id]["shiny"] = shininess
            await add_pet_xp(message, 10, userdata, id)
        set_userdata(user, userdata)
    return converted_to_xp, shininess

async def show_pets(self, message, target = 2):
    """Shows the pets of a target user"""

    target = target_from_message(self, message)

    userdata = get_userdata(target)
    if "pets" in userdata.keys():
        userinv = userdata["pets"]
        embed = discord.Embed(
            title=f"{target}'s Pets", colour=discord.Colour.orange()
        )
        output = ""
        for petid in userinv.keys():
            petobj = userinv[petid]
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
    if not "pets" in userkeys:
        embed.discord.Embed(
            title=f"You have no pets"
        )
        await message.reply
    else:
        target = command[1]
        pet_data = get_itemdata()
        user_pets = userdata["pets"]
        if target in pet_data.keys():
            if target in user_pets:
                userdata["equipped_pet"] = target
                embed = discord.Embed(
                    title=f"{pet_data[target]["name"]} Equipped", colour=discord.Colour.green()
                )
            else:
                embed = gen_error(f"You do not own a {pet_data[target]["name"]}")
        else:
            embed = gen_error(f"{target} does not exist")
        await message.reply(embed=embed)
        set_userdata(message.author, userdata)

async def add_pet_xp(message, amount,userdata, id):
    userdata["pets"][id]["xp"] += amount
    userdata["pets"][id]["xp_needed"] = pet_xp_required(userdata["pets"][id]["level"], get_itemdata(id)["rarity"])

    if userdata["pets"][id]["xp"] > userdata["pets"][id]["xp_needed"]:
        userdata["pets"][id]["level"] += 1
        userdata["pets"][id]["xp"] -= userdata["pets"][id]["xp_needed"]
        petdata = get_itemdata(id)
        embed = discord.Embed(
                        description=f"Congratulations {message.author.mention} your {petdata["name"]} is now level {userdata["pets"][id]["level"]}!",
                        colour=discord.Colour.green(),
                    )
        await message.reply(embed=embed)
    set_userdata(message.author, userdata)
    return userdata
    
async def pet_xp(self, message):
    if message.author != self.user:
        userdata = get_userdata(message.author)
        userkeys = userdata.keys()
        if "equipped_pet" in userkeys:
            await add_pet_xp(message, randint(2,5), userdata, userdata["equipped_pet"])

async def hunt(self, message):
    pass