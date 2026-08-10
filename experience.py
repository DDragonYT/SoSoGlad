from enum import Enum
from random import randint
from userdata import *
import discord
import os
from embed import *
from badge import add_badge

LEVEL_UP_BADGES = {
    10:"level_10",
    20:"level_20",
    30:"level_30",
    50:"level_50",
    75:"level_75",
    100:"level_100",
    150:"level_150",
    200:"level_200",
    300:"level_300",
    500:"level_500",
    500:"level_1000"
}

LEVEL_DIVIDER = 2
LEVEL_CURVE = 2
LEVEL_BASE = 100

def level_up_badge(self, message, level):
      if level in LEVEL_UP_BADGES.keys():
            add_badge(self, message, LEVEL_UP_BADGES[level])

def amount_for_level(level):
      return int((level/LEVEL_DIVIDER)**LEVEL_CURVE +
                LEVEL_BASE
                )      

async def experience_check(self, message, amount:int = 1):
    if message.author != self.user:
        userdata = get_userdata(message.author)
        userkeys = userdata.keys()
        if not "exp" in userkeys:
                userdata["exp"] = 0
                userkeys = userdata.keys()
        if not "level" in userkeys:
                userdata["level"] = 1
                userkeys = userdata.keys()                
        userdata["exp"] += randint(2,5) 
        userdata["xp_needed"] = amount_for_level(userdata["level"])
        if userdata["exp"] > userdata["xp_needed"]:
              userdata["level"] += amount
              userdata["exp"] -= userdata["xp_needed"]
              message.reply(embed=discord.Embed(title = f"Congratulations {message.author.mention} you are now level {userdata["level"]}!"))
              set_userdata(message.author, userdata)
              level_up_badge(self, message, userdata["level"])


if __name__ == "__main__":
        for x in range(1,500):
              print(f"Level {x} needs {amount_for_level(x)} XP to level up.")