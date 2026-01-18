DAILY_AMOUNT = 10
from datetime import date
from userdata import *
WALLET_STATS = [
    "coins",
    "gems",
    "last_daily"
]


def wallet_add(userdata, amount):
    if "coins" in userdata.keys():
        userdata["coins"] += amount
    else:
        userdata["coins"] = amount
    return userdata



async def wallet_stats(self, message):
    command = str(message.content).split(" ")
    if len(command) > 2:
        target = command[2]
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


        

async def wallet_daily(self,message):
    userdata = get_userdata(message.author)
    if "last_daily" in userdata.keys():
        if userdata["last_daily"] != str(date.today()):
            userdata["last_daily"] = str(date.today())
            wallet_add(userdata, DAILY_AMOUNT)
            await message.reply(f"You claimed a daily login reward of ${DAILY_AMOUNT} and now have ${userdata["coins"]} in your wallet.")
        else:
            await message.reply(f"You have already claimed your daily login reward today.")

    else:
        userdata["last_daily"] = str(date.today())
        wallet_add(userdata, DAILY_AMOUNT)
        await message.reply(f"You claimed a daily login reward of ${DAILY_AMOUNT} and now have ${userdata["coins"]} in your wallet.")
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