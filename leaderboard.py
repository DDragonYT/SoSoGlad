from _ssg_utils import *

from enum import Enum
from random import randint
from userdata import *
import discord
import os
from badge import add_badge
from profile import *
from experience import *

users_on_leaderboard = 10

async def leaderboard(self, message):
    coin_list = []
    for file in os.listdir("users"):
        user = file.split(" ")[0]
        userdata = get_userdata(user)
        coin_list.append(user,userdata["coins"])
    sorted_coin_list = dict(sorted(coin_list.items(), key=lambda x: x[1]["coins"], reverse=True))
    embed = discord.Embed(title=f"coin list",description=f"{coin_list}")
    await message.reply(embed)
    embed = discord.Embed(title=f"Coin Leaderboard", colour=discord.Colour.yellow(),description=f"{sorted_coin_list}")
    await message.reply(embed)

def update_leaderboard_variables():
    base_list = []
    for file in os.listdir("users"):
        user = file.split(" ")[0]
        userdata = get_userdata(user)
        base_list.append(userdata)
    print('base_list')

if __name__ == "__main__":
    update_leaderboard_variables()