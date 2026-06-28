import discord
from userdata import *
from embed import gen_error
from crate import open_crate
from wallet import wallet_add, add_to_inv, ITEM_ICONS, get_itemdata

# WIP

SHOP_ITEMS = {
    "pet_crate":{
        "name":"Pet Crate",
        "id":"pet_crate",
        "coin_price":100,
        "gem_price":0,
    },
    "20_coins":{
        "name":"20 Coins",
        "id":"20_coins",
        "coin_price":0,
        "gem_price":1,
    },
    "200_coins":{
        "name":"200 Coins",
        "id":"200_coins",
        "coin_price":0,
        "gem_price":10,
    }
}

async def show_shop(self, message):
    embed = discord.Embed(title=f"Shop", colour=discord.Colour.orange())
    for item in SHOP_ITEMS.keys():
        itemdata = SHOP_ITEMS[item]
        value = ""
        for key in itemdata:
            if itemdata[key] and key != "name":
                if itemdata[key] == "gem_price" or itemdata[key] == "coin_price":
                    if itemdata[key] < 0:
                        break
                value += f"""**{"ID" if key == "id" else key.replace("_"," ").capitalize()}**: {"`" if key == "id" else ""} {itemdata[key]} {"`" if key == "id" else ""} \n"""
        embed.add_field(name=f"[{ITEM_ICONS[get_itemdata(item)["type"]]}] {itemdata["name"]}", value=value)

    await message.reply(embed = embed)

async def make_purchase(user, shopitemdata, message):
    userdata = get_userdata(user)
    userdata = wallet_add(userdata, -1 * shopitemdata["coin_price"], "coins")
    userdata = wallet_add(userdata, -1 *    shopitemdata["gem_price"], "gems")
    itemdata = get_itemdata(shopitemdata["id"])
    coins_spent = shopitemdata["coin_price"]
    gems_spent = shopitemdata["gem_price"]
    if itemdata["type"] == "currency":
        userdata = wallet_add(userdata, itemdata["coin_amt"], "coins")
        userdata = wallet_add(userdata, itemdata["gem_amt"], "gems")
        set_userdata(user, userdata)
        embed = discord.Embed(title=f"""Exchanged {f"{itemdata['coin_amt']} coins" if itemdata['coin_amt'] else ""}{f"{itemdata['gem_amt']} gems" if itemdata['gem_amt'] else ""} for {f"{coins_spent} coins" if coins_spent else ""}{f"{gems_spent} gems" if gems_spent else ""}.""", colour=discord.Colour.orange(),)
        await message.reply(embed = embed)
    else:
        add_to_inv(user, userdata, shopitemdata["id"])
        embed = discord.Embed(title=f"""Purchased {itemdata["name"]} for {f"{coins_spent} coins" if coins_spent else ""}{f"{gems_spent} coins" if gems_spent else ""}.""", colour=discord.Colour.orange(),)
        await message.reply(embed = embed)


async def attempt_purchase(self,message):
    command_params = message.content.split(" ")
    if len(command_params) < 2:
        await message.reply(embed = gen_error("Please enter a shop item ID."))
    elif not command_params[1].lower() in SHOP_ITEMS.keys():
        await message.reply(embed = gen_error(f""" `{command_params[1]}` is not a shop item."""))
    else:
        userdata = get_userdata(message.author)
        item = SHOP_ITEMS[command_params[1].lower()]
        if userdata["coins"] >= item["coin_price"] and userdata["gems"] >= item["gem_price"]:
            await make_purchase(message.author, item, message)
        else:
            await message.reply(embed = gen_error(f"""You do not have enough currency to make this purchase.
Required Coins: {item["coin_price"]} → Current Coins: {userdata["coins"]}
Required Gems: {item["gem_price"]} → Current Gems: {userdata["gems"]}"""))
