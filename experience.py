from enum import Enum
from random import randint
from userdata import *
import discord
import os
from embed import *
from badge import add_badge
from wallet import wallet_stats

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

PROFILE_STATS = {
      "level" : "Level",
      "exp" : "XP",
      "net_worth" : "Net Worth",
      #"eqipped_pet" : "Equipped Pet",
      #"favourite_card" : "Favourite Card",
      #"favourite_badge" : "Favourite Badge",
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

              
async def profile(self, message, target=2):
      command = str(message.content).split(" ")
      if len(command) > 1:
            target = command[1]
            if "<" in target:
                  user_id = int(target.strip("<>@"))
                  target = self.get_user(user_id)
            else:
                  target = message.author
      else:
            target = message.author
      embed = discord.Embed(title=f"{target.user}'s Profile", colour=discord.Colour.yellow())
      embed.set_image(url=str(target.avatar))
      userdata = get_userdata(target)
      userkeys = userdata.keys()
      for key in PROFILE_STATS.keys():
            if key in userkeys:
                  embed.add_field(name=PROFILE_STATS[key], value=userdata[key])
            await message.reply(embed=embed)


if __name__ == "__main__":
        for x in range(1,500):
              print(f"Level {x} needs {amount_for_level(x)} XP to level up.")