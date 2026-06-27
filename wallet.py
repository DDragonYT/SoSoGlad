DAILY_AMOUNT = 100
from datetime import date
from userdata import *
from random import randint
from embed import *
from badge import calc_inv

WALLET_STATS = {
    "coins":"Coins 🪙",
    "gems":"Gems 💎",
    "last_daily":"Last Daily",
    "badgeinvvalue":"Badges Value",
    "net-worth": "Net Worth",
    
}

def wallet_add(userdata, amount, currency="coins"):
    "Adds an amount of a currency to a user"
    if currency in userdata.keys():
        userdata[currency] += amount
    else:
        userdata[currency] = amount
    return userdata

async def wallet_stats(self, message, target=2):
    "Calculates a users inventory, then displays their details"
    command = str(message.content).split(" ")
    if len(command) > target:
        target = command[len(command)-1]
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
    await message.reply(embed = embed)

async def claim_daily(self, message, userdata=None):
    "If user hasn't claimed their daily today, add their daily and then set their last claimed daily"
    gem_reward = randint(0, 10)
    coin_reward = DAILY_AMOUNT
    wallet_add(userdata, coin_reward)
    wallet_add(userdata, gem_reward, "gems")
    userdata["last_daily"] = str(date.today())
    embed = discord.Embed(title="You claimed a daily login reward of:", colour=discord.Color.yellow())
    embed.add_field(name=WALLET_STATS["coins"], value=coin_reward)
    embed.add_field(name=WALLET_STATS["gems"], value=gem_reward)
    await message.reply(embed=embed)

async def wallet_daily(self,message):
    ""
    userdata = get_userdata(message.author)
    if "last_daily" in userdata.keys():
        if userdata["last_daily"] != str(date.today()):
            await claim_daily(self, message, userdata)
        else:
            await message.reply(embed = gen_error("You have already claimed your daily login reward today."))
    else:
        await claim_daily(self, message, userdata)
    set_userdata(str(message.author), userdata)

WALLET_CMDS = {
    "daily":wallet_daily,
    "view":wallet_stats
}

async def wallet(self, message):
    command_params = message.content.split(" ")
    if len(command_params) > 1:
        if command_params[1] in WALLET_CMDS.keys():
            await WALLET_CMDS[command_params[1]](self, message)
        else:
            await wallet_stats(self, message, 1)
    else:
        await wallet_stats(self, message, 1)