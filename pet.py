from userdata import *
import discord
from item import *

def pet_search(name):
    """I dunno"""
    pet_data = get_itemdata()
    if name in pet_data.keys():
        if pet_data[name]["type"] == "pet":
            return name
    else:
        for key in pet_data.keys():
            pet = pet_data[key]
            if name in pet["name"].lower():
                if pet_data[name]["type"] == "pet":
                    return name
    return

# async def badge_info(self, message):
#     """Checks if a badge exists, if it does generate an embed and send it"""
#     command_params = message.content.split(" ")
#     if len(command_params) > 1:
#         pet = pet_search(command_params[1])
#         if pet:
#             ibadge:Badge = BADGE_DATA[badge]
#             embed = badge_details(ibadge, badge)
#             await message.reply(embed=embed)
#         else:
#             await message.reply(embed = gen_error("That badge doesn't exist!"))
#     else:
#         await message.reply(embed = gen_error("Please enter a badge name."))

def add_pet(id, qty, user, level = 0):
    userdata = get_userdata(user)
    if not "pets" in userdata.keys():
        userdata["pets"] = []
    for i in range(qty):
        userdata["pets"].append(
        {
            "id":id,
            "name":    get_itemdata(id)["name"],
            "level":level
        }
        )
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