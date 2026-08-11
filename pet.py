from userdata import *
import discord
from item import *
from random import randint

LEVEL_DIVIDER = 2
LEVEL_CURVE = 2
LEVEL_BASE = 100

def pet_xp_required(level):
    return int((level / LEVEL_DIVIDER) ** LEVEL_CURVE + LEVEL_BASE)

async def pet_info(self, message):
    """Checks if a pet exists, if it does generate an embed and send it"""
    await item_info(self, message, "pet")

def add_xp(amount,userdata, id):
    userdata["pets"][id]["xp"] += amount

def add_pet(id, qty, user, level = 0):
    userdata = get_userdata(user)
    if not "pets" in userdata.keys():
        userdata["pets"] = {}
    if not id in userdata["pets"]:
        for i in range(qty):
            userdata["pets"][id] = {
                "id":id,
                "name": get_itemdata(id)["name"],
                "level":level,
                "xp" : 0
            }

        set_userdata(user, userdata)
    else:
        pet_data = get_itemdata(id)
        if userdata["pets"][id]["level"] < 101:
            userdata = add_xp(10, userdata)
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

async def pet_xp(self, message):
    if message.author != self.user:
        userdata = get_userdata(message.author)
        userkeys = userdata.keys()
        if "equipped_pet" in userkeys:
            equipped_pet = "equipped_pet"
            for equipped_pet in userdata["pets"]:
                equipped_pet_data = userdata["pets"][equipped_pet]
                equipped_pet_data["xp"] += randint(2,5)
                equipped_pet_data["xp_needed"] = pet_xp_required(equipped_pet_data["level"])
            if equipped_pet_data["xp"] > equipped_pet_data["xp_needed"]:
                equipped_pet_data["level"] += 1
                equipped_pet_data["xp"] - equipped_pet_data["xp_needed"]
                equipped_pet_data
                embed = discord.Embed(
                                description=f"Congratulations {message.author.mention} your {"eqiupped_pet"} is now level {equipped_pet_data["level"]}!", colour=discord.Colour.green()
                            )
            userdata["pets"][equipped_pet] = equipped_pet_data
            set_userdata(message.author, userdata)
            await message.reply(embed)

