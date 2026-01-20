DAILY_AMOUNT = 10
from datetime import date
from userdata import *
from random import randint
WALLET_STATS = {
    "coins":"🪙",
    "gems":"💎",
    "last_daily":""
}

def wallet_add(userdata, amount, currency="coins"):
    if currency in userdata.keys():
        userdata[currency] += amount
    else:
        userdata[currency] = amount
    return userdata



async def wallet_stats(self, message, target=2):
    command = str(message.content).split(" ")
    if len(command) > target:
        target = command[len(command)-1]
        if "<" in target:
            user_id = int(target.strip("<>@"))
            target = self.get_user(user_id)
    else:
        target = message.author
    output = f"**{target}'s Wallet:**"
    userdata = get_userdata(target)
    for var in WALLET_STATS:
        if var in userdata.keys():
            output += f"\n{var.capitalize().replace("_"," ")} : {userdata[var]}"
    await message.reply(output)


async def claim_daily(self, message, userdata=None):
    gem_reward = randint(0, 1)
    wallet_add(userdata, DAILY_AMOUNT)
    wallet_add(userdata, gem_reward, "gems")
    userdata["last_daily"] = str(date.today())
    await message.reply(f"""You claimed a daily login reward of:
- ${DAILY_AMOUNT}
- {gem_reward} gems
And now have ${userdata["coins"]} and {userdata["gems"]} gems in your wallet.""")

async def wallet_daily(self,message):
    userdata = get_userdata(message.author)
    if "last_daily" in userdata.keys():
        if userdata["last_daily"] != str(date.today()):
            await claim_daily(self, message, userdata)
        else:
            await message.reply(f"You have already claimed your daily login reward today.")
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