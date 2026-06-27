import discord
from userdata import get_userdata
from embed import gen_error
from crate import open_crate

# WIP

SHOP_ITEMS = {
    "pet_crate":{
        "name":"Pet Crate",
        "id":"pet_crate",
        "coin_price":100,
        "gem_price":0,
    },
    "coin_exchange":{
        "name":"20 Coins",
        "id":"coin_exchange",
        "coin_price":0,
        "gem_price":1,
    }
}

async def show_shop(self, message):
    embed = discord.Embed(title=f"Shop", colour=discord.Colour.orange())
    await message.reply(embed = embed)

# async def make_purchase(user, item):
#     if item["type"] == "crate":



async def attempt_purchase(self,message):
    command_params = message.content.split(" ")
    if len(command_params) < 2:
        message.reply(embed = gen_error("Please enter a shop item ID."))
    elif not command_params[2].lower() in SHOP_ITEMS.keys():
        message.reply(embed = gen_error(f""" "{command_params[2]}" is not a shop item."""))
    else:
        userdata = get_userdata(message.author)
        item = SHOP_ITEMS[command_params[2].lower()]
        if userdata["coins"] >= item["coin_price"] or userdata["gems"] >= item["gem_price"]:
            await make_purchase(message.author, item)
