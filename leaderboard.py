from _ssg_utils import gen_error, set_userdata, get_userdata
from _globalvars import WALLET_STATS, BASE_LEADERBOARD

from enum import Enum
from random import randint
import discord
import os
from badge import add_badge
from profile import *
from experience import *

users_on_leaderboard = 10

LEADERBOARD_TYPES = {
    "coins": "Coins Leaderboard",
    "gems": "Gems Leaderboard",
    "badgeinvvalue": "Badges Value Leaderboard",
    "level": "Level Leaderboard",
}
BASE_LIST = []

async def leaderboard(self, message):
    command = str(message.content).split(" ")
    if len(command) > 1:
        type = command[1]
    else:
        type = "coins"


    if not type in LEADERBOARD_TYPES.keys():
        await message.reply(embed = gen_error("This is not a valid leaderboard."))
        return

    await message.reply(embed = list_for_type(BASE_LEADERBOARD, type), view = leaderboard)
    

def calc_leaderboard():
    global BASE_LEADERBOARD
    base_list = []
    for file in os.listdir("users"):
        with open("users/" + file, "r") as userjson:
            userdata = json.load(userjson)
        for key in LEADERBOARD_TYPES.keys():
            if not key in userdata.keys():
                if key == "level":
                    userdata[key] = 1
                else:
                    userdata[key] = 0
        userdata["username"] = file.split(".")[0]
        set_userdata(file.split(".")[0], userdata)
        base_list.append(userdata)
    BASE_LEADERBOARD = base_list


def list_for_type(base_list, type):
    newlist = sorted(base_list, key=lambda d: d[type], reverse=True)
    listlen = len(newlist) if len(newlist) < 10 else 10
    value = ""
    for i in range(listlen):
        userdata = newlist[i]
        value += (
            f"{i+1}. {userdata["username"]} - {userdata[type]} {WALLET_STATS[type]} \n"
        )
    print(value)
    embed = discord.Embed(title=LEADERBOARD_TYPES[type], colour=discord.Colour.yellow(), description = value)
    return embed