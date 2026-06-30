DAILY_AMOUNT = 100
from datetime import date
from userdata import *
from random import randint
from embed import *
from badge import calc_inv
from crate import open_crate

WALLET_STATS = { # What should we call these stats?
    "coins": "Coins 🪙",
    "gems": "Gems 💎",
    "last_daily": "Last Daily",
    "badgeinvvalue": "Badges Value",
    "net-worth": "Net Worth",
}

ITEM_ICONS = { # Used to define what icon an item type should have
    "lolly": "🍭",
    "minion": "😈",
    "pet": "🐕",
    "booster": "🔋",
    "crate": "🎁",
    "equipment": "🗡️",
    "trinket": "📿",
    "currency": "💰",
}

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


def wallet_add(userdata, amount, currency="coins"):
    "Adds an amount of a currency to a user"

    if currency in userdata.keys():
        userdata[
            currency
        ] += amount  # If the player has had this currency before, add money
    else:
        userdata[currency] = amount  # otherwise, set money
    return userdata


async def wallet_stats(self, message, target=2):
    "Calculates a users inventory, then displays their details"

    command = str(message.content).split(" ")
    if len(command) > target:
        target = command[len(command) - 1]
        if "<" in target:
            user_id = int(target.strip("<>@"))
            target = self.get_user(user_id)
    else:
        target = message.author
    
    calc_inv(target)
    userdata = get_userdata(target)
    userkeys = userdata.keys()
    embed = discord.Embed(title=f"{target}'s Wallet", colour=discord.Colour.yellow())
    if not "coins" in userkeys:
        userdata["coins"] = 0
        userkeys = userdata.keys()
    userdata["net-worth"] = userdata["badgeinvvalue"] + userdata["coins"]

    for key in WALLET_STATS.keys():
        if key in userkeys:
            embed.add_field(name=WALLET_STATS[key], value=userdata[key])
    await message.reply(embed=embed)


async def claim_daily(self, message, userdata=None):
    """Add their daily and then set their last claimed daily"""

    gem_reward = randint(0, 10)
    coin_reward = DAILY_AMOUNT
    wallet_add(userdata, coin_reward)
    wallet_add(userdata, gem_reward, "gems")
    userdata["last_daily"] = str(date.today())
    embed = discord.Embed(
        title="You claimed a daily login reward of:", colour=discord.Color.yellow()
    )
    embed.add_field(name=WALLET_STATS["coins"], value=coin_reward)
    embed.add_field(name=WALLET_STATS["gems"], value=gem_reward)
    await message.reply(embed=embed)


async def wallet_daily(self, message):
    """Check if daily has been claimed, if it hasn't, claim_daily"""
    userdata = get_userdata(message.author)
    if "last_daily" in userdata.keys():
        if userdata["last_daily"] != str(date.today()):
            await claim_daily(self, message, userdata)
        else:
            await message.reply(
                embed=gen_error(
                    "You have already claimed your daily login reward today."
                )
            )
    else:
        await claim_daily(self, message, userdata)
    set_userdata(str(message.author), userdata)


WALLET_CMDS = {"daily": wallet_daily, "view": wallet_stats}


async def wallet(self, message):
    command_params = message.content.split(" ")
    if len(command_params) > 1:
        if command_params[1] in WALLET_CMDS.keys():
            await WALLET_CMDS[command_params[1]](self, message)
        else:
            await wallet_stats(self, message, 1)
    else:
        await wallet_stats(self, message, 1)


def add_to_inv(user, userdata, item):
    if not "inventory" in userdata.keys():
        userdata["inventory"] = {}
    if not item in userdata["inventory"]:
        userdata["inventory"][item] = {"quantity": 0}
    userdata["inventory"][item]["quantity"] += 1
    set_userdata(user, userdata)


def get_itemdata(itemname=None):
    with open("items.json", "rb") as itemjson:
        if itemname:
            return json.load(itemjson)[itemname]
        else:
            return json.load(itemjson)


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
            # embed.add_field(name=item, value=userdata[key])
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
        embed = discord.Embed(
            title=f"Opening a {get_itemdata(item)["name"]}...",
            colour=discord.Colour.orange(),
        )
        await message.reply(embed=embed)
        acquired_item, item_rarity = open_crate(item)
        if item_rarity != "common":
            embed = discord.Embed(
                title=f"Woah! It's a {item_rarity}!", colour=discord.Colour.orange()
            )
            await message.channel.send(embed=embed)
        embed = discord.Embed(title=f"Crate Result", colour=discord.Colour.orange())
        itemdata = get_itemdata(acquired_item)
        itemname = itemdata["name"]
        embed.description = f"{message.author.mention} got {itemname} from a {get_itemdata(item)["name"]}!"
        embed.add_field(name="Item Name", value=itemname)
        embed.add_field(name="Rarity", value=item_rarity.capitalize())
        embed.add_field(name="Type", value=itemdata["type"].capitalize())
        embed.set_thumbnail(url=itemdata["image"])
        await message.channel.send(embed=embed)


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


async def make_purchase(user, shopitemdata, message):
    userdata = get_userdata(user)
    userdata = wallet_add(userdata, -1 * shopitemdata["coin_price"], "coins")
    userdata = wallet_add(userdata, -1 * shopitemdata["gem_price"], "gems")
    itemdata = get_itemdata(shopitemdata["id"])
    coins_spent = shopitemdata["coin_price"]
    gems_spent = shopitemdata["gem_price"]
    if itemdata["type"] == "currency":
        userdata = wallet_add(userdata, itemdata["coin_amt"], "coins")
        userdata = wallet_add(userdata, itemdata["gem_amt"], "gems")
        set_userdata(user, userdata)
        embed = discord.Embed(
            title=f"""Exchanged {f"{itemdata['coin_amt']} coins" if itemdata['coin_amt'] else ""}{f"{itemdata['gem_amt']} gems" if itemdata['gem_amt'] else ""} for {f"{coins_spent} coins" if coins_spent else ""}{f"{gems_spent} gems" if gems_spent else ""}.""",
            colour=discord.Colour.orange(),
        )
        await message.reply(embed=embed)
    else:
        add_to_inv(user, userdata, shopitemdata["id"])
        embed = discord.Embed(
            title=f"""Purchased {itemdata["name"]} for {f"{coins_spent} coins" if coins_spent else ""}{f"{gems_spent} coins" if gems_spent else ""}.""",
            colour=discord.Colour.orange(),
        )
        await message.reply(embed=embed)


async def attempt_purchase(self, message):
    """If the user can make a purchase, """
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
        if (
            userdata["coins"] >= item["coin_price"]
            and userdata["gems"] >= item["gem_price"]
        ):
            await make_purchase(message.author, item, message)
        else:
            await message.reply(
                embed=gen_error(
                    f"""You do not have enough currency to make this purchase.
Required Coins: {item["coin_price"]} → Current Coins: {userdata["coins"]}
Required Gems: {item["gem_price"]} → Current Gems: {userdata["gems"]}"""
                )
            )
