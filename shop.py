import discord
from userdata import get_userdata
from wallet import *
from item import *
from userdata import *

SHOP_ITEMS = {
    "pet_crate": {
        "id": "pet_crate",
        "coin_price": 100,
        "gem_price": 0,
    },
    "luck_booster": {
        "id": "luck_booster",
        "coin_price": 500,
        "gem_price": 0,
    },
    "20_coins": {
        "id": "20_coins",
        "coin_price": 0,
        "gem_price": 1,
    },
    "200_coins": {
        "id": "200_coins",
        "coin_price": 0,
        "gem_price": 10,
    },
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
        embed.add_field(
            name=f"[{ITEM_ICONS[get_itemdata(item)["type"]]}] {get_itemdata(item)["name"]}",
            value=value,
        )

    await message.reply(embed=embed)


async def make_purchase(user, shopitemdata, message, quantity):

    userdata = get_userdata(user)  # Load the userdata
    itemdata = get_itemdata(shopitemdata["id"])

    coins_spent = (
        shopitemdata["coin_price"] * quantity
    )  # How much have I spent in coins?
    gems_spent = shopitemdata["gem_price"] * quantity  # How much have I spent in gems?

    userdata = wallet_add(
        userdata, -1 * coins_spent, "coins"
    )  # Remove the amount spent by multiplying by -1 and adding that negative value
    userdata = wallet_add(userdata, -1 * gems_spent, "gems")

    if itemdata["type"] == "currency":
        coins_got = (
            itemdata["coin_amt"] * quantity
        )  # Use the item data to figure out how much I wanna add
        gems_got = itemdata["gem_amt"] * quantity

        userdata = wallet_add(userdata, coins_got, "coins")
        userdata = wallet_add(userdata, gems_got, "gems")
        set_userdata(user, userdata)
        embed = discord.Embed(
            title=f"""Exchanged {f"{coins_got} coins" if coins_got else ""}{f"{gems_got} gems" if gems_got else ""} for {f"{coins_spent} coins" if coins_spent else ""}{f"{gems_spent} gems" if gems_spent else ""}.""",
            colour=discord.Colour.orange(),
        )
        await message.reply(embed=embed)
    else:

        add_to_inv(user, userdata, shopitemdata["id"], quantity)
        embed = discord.Embed(
            title=f"""Purchased {str(quantity)+" " if quantity else ""}{itemdata["name"]}(s) for {f"{coins_spent} coins" if coins_spent else ""}{f"{gems_spent} coins" if gems_spent else ""}.""",
            colour=discord.Colour.orange(),
        )
        await message.reply(embed=embed)


async def attempt_purchase(self, message):
    """If the user can make a purchase,"""
    command_params = message.content.split(" ")
    if len(command_params) < 2:
        await message.reply(embed=gen_error("Please enter a shop item ID."))
    elif not command_params[1].lower() in SHOP_ITEMS.keys():
        await message.reply(
            embed=gen_error(f""" `{command_params[1]}` is not a shop item.""")
        )
    else:
        userdata = get_userdata(message.author)
        item = SHOP_ITEMS[command_params[1].lower()]
        if len(command_params) > 2:
            try:
                purchase_qty = int(command_params[2])
            except:
                await message.reply(embed=gen_error("That is not a valid quantity."))
        else:
            purchase_qty = 1
        if (
            userdata["coins"] >= item["coin_price"] * purchase_qty
            and userdata["gems"] >= item["gem_price"] * purchase_qty
        ):
            await make_purchase(message.author, item, message, purchase_qty)
        else:
            await message.reply(
                embed=gen_error(
                    f"""You do not have enough currency to make this purchase.
Required Coins: {item["coin_price"]} → Current Coins: {userdata["coins"]}
Required Gems: {item["gem_price"]} → Current Gems: {userdata["gems"]}"""
                )
            )
