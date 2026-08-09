from enum import Enum
from random import randint
from userdata import *
import discord
import os
from embed import *

async def on_message(message):
    if message.author != bot.user:
        userdata = get_userdata(message.author)
        userkeys = userdata.keys()
        if not "exp" in userkeys:
                userdata["exp"] = 0
                userkeys = userdata.keys()
        if not "level" in userkeys:
                userdata["level"] = 0
                userkeys = userdata.keys()
        userdata["exp"] += randint(2,5)
        if userdata["exp"] > 100:
              userdata["level"] += 1
              userdata["exp"] -= 100
              embed = discord.Embed(title = f"Congratulations {message.author.mention} you are now level {userdata["level"]}")

