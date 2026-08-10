import discord
from userdata import *
from badge import calc_inv
from random import randint
from embed import gen_error
from datetime import date

WALLET_STATS = {  # What should we call these stats?
    "coins": "Coins 🪙",
    "gems": "Gems 💎",
    "last_daily": "Last Daily",
    "badgeinvvalue": "Badges Value",
    "net_worth": "Net Worth",
}

DAILY_AMOUNT = 100


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
    embed.set_thumbnail(url="https://em-content.zobj.net/source/huawei/442/purse_1f45b.png")
    if not "coins" in userkeys:
        userdata["coins"] = 0
        userkeys = userdata.keys()
    userdata["net_worth"] = userdata["badgeinvvalue"] + userdata["coins"]
    for key in WALLET_STATS.keys():
        if key in userkeys:
            embed.add_field(name=WALLET_STATS[key], value=userdata[key])
    set_userdata(target, userdata)
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


def wallet_add(userdata, amount, currency="coins"):
    "Adds an amount of a currency to a user"
    if currency in userdata.keys():
        userdata[
            currency
        ] += amount  # If the player has had this currency before, add money
    else:
        userdata[currency] = amount  # otherwise, set money
    return userdata


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


def add_to_inv(user, userdata, item, quantity):
    if not "inventory" in userdata.keys():
        userdata["inventory"] = {}
    if not item in userdata["inventory"]:
        userdata["inventory"][item] = {"quantity": 0}
    userdata["inventory"][item]["quantity"] += quantity
    set_userdata(user, userdata)

async def gift(self, message, target=2):
    command = str(message.content).split(" ")
    if message.author != self.user:
        if len(command) > 1:
            target = command[1]
            if "<" in target:
                user_id = int(target.strip("<>@"))
                target = self.get_user(user_id)
        try:
            gift_amt = int(command[2])
            sender_userdata = get_userdata(message.author)
            if gift_amt > 0:
                if sender_userdata["coins"] >= gift_amt:
                    userdata = get_userdata(target)
                    userdata["coins"] += gift_amt
                    set_userdata(target, userdata)
                    sender_userdata["coins"] -= gift_amt
                    set_userdata(message.author, sender_userdata)
                    embed = discord.Embed(title="Successful Gift",description=f"{message.author.mention} has gifted {target.mention} {gift_amt} coins!", colour=discord.Colour.green())
                    await message.reply(embed = embed)
                else:
                    await message.reply(embed=gen_error("You cannot afford this gift."))
            else: 
                await message.reply(embed=gen_error("You cant gift nothing."))
        except:
            await message.reply(embed=gen_error(f"Failed to gift to {target}"))
