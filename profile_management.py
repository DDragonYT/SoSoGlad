from _globalvars import *
from _ssg_utils import gen_error, target_from_message, get_userdata, set_userdata

import discord
from badge import calc_inv, BADGE_DATA
from random import randint
from datetime import date
from item import get_itemdata


async def wallet_stats(self, message, target=2):
    "Calculates a users inventory, then displays their details"

    target = target_from_message(self, message)

    calc_inv(target)
    userdata = get_userdata(target)
    userkeys = userdata.keys()
    embed = discord.Embed(title=f"{target}'s Wallet", colour=discord.Colour.yellow())
    embed.set_thumbnail(
        url="https://em-content.zobj.net/source/huawei/442/purse_1f45b.png"
    )
    if not "coins" in userkeys:
        userdata["coins"] = 0
        userkeys = userdata.keys()
    userdata["net_worth"] = userdata["badgeinvvalue"] + userdata["coins"]
    for key in WALLET_STATS.keys():
        if key in userkeys:
            embed.add_field(name=WALLET_STATS[key], value=userdata[key])
    set_userdata(target, userdata)
    await message.reply(embed=embed)


async def profile(self, message, target=2):
    """Calculates a users inventory statistics, then displays an overall profile."""

    target = target_from_message(self, message)

    if not target:
        message.reply(embed = gen_error("This is not a valid user."))
        return

    calc_inv(target)

    embed = discord.Embed(title=f"{target}'s Profile", colour=discord.Colour.yellow())
    embed.set_thumbnail(url=str(target.avatar))
    userdata = get_userdata(target)
    userkeys = userdata.keys()
    calc_inv(target)
    for key in PROFILE_STATS.keys():
        if key in userkeys:

            if key == "equipped_badge":
                badge = userdata["equipped_badge"]
                badgetype = "badges"
                badgedata = BADGE_DATA[badge]
                leveltext = (
                    f" Tier {userdata[badgetype][badge]["lvl"]}"
                    if userdata[badgetype][badge]["lvl"] > 1
                    else ""
                )
                value = f"[{badgedata.image}] {badgedata.title}{leveltext} ({badgedata.rarity.name})"
                embed.add_field(name=PROFILE_STATS[key], value=value)

            elif key == "xp_needed":
                embed.add_field(
                    name=PROFILE_STATS[key],
                    value=(int(userdata["xp_needed"]) - int(userdata["exp"])),
                )

            elif key == "equipped_pet":
                pet = userdata["equipped_pet"]
                pet_data = get_itemdata(pet)
                leveltext = f" Level {userdata["pets"][pet]["level"]}"
                value = f"[{pet_data["icon"]}] {pet_data["name"]}{leveltext} ({pet_data["rarity"].upper()})"
                embed.add_field(name=PROFILE_STATS[key], value=value)

            else:
                # If nothing else hits, just do the base information.
                embed.add_field(name=PROFILE_STATS[key], value=userdata[key])

        else:
            # If the user does not have a stat, simply respond that they do not have it.
            embed.add_field(name=PROFILE_STATS[key], value=f"No {PROFILE_STATS[key]}.")
    await message.reply(embed=embed)


def amount_for_level(level):
    """Calculates the amount of experience required to level up, based on their current level."""
    return int((level / LEVEL_DIVIDER) ** LEVEL_CURVE + LEVEL_BASE)


async def experience_check(self, message, amount: int = 1):
    """Checks and handles the addition of experience to a user."""

    if message.author != self.user:
        userdata = get_userdata(message.author)
        userkeys = userdata.keys()
        if not "exp" in userkeys:
            userdata["exp"] = 0
            userkeys = userdata.keys()
        if not "level" in userkeys:
            userdata["level"] = 1
            userkeys = userdata.keys()
        userdata["exp"] += randint(2, 5)
        userdata["xp_needed"] = amount_for_level(userdata["level"])
        set_userdata(message.author, userdata)
        if userdata["exp"] > userdata["xp_needed"]:
            userdata["level"] += 1
            userdata["exp"] -= userdata["xp_needed"]
            set_userdata(message.author, userdata)
            embed = discord.Embed(
                description=f"Congratulations {message.author.mention} you are now level {userdata["level"]}!",
                colour=discord.Colour.green(),
            )
            await message.reply(embed=embed)


async def equip_badge(self, message, target=2):
    userdata = get_userdata(message.author)
    userkeys = userdata.keys()
    command = str(message.content).split(" ")
    if not "eqipped_badge" in userkeys:
        userdata["equipped_badge"] = "none"
        userkeys = userdata.keys()

    target = command[1]
    if target in BADGE_DATA:
        if target in userdata["badges"]:
            userdata["equipped_badge"] = target
            embed = discord.Embed(
                title=f"Badge Equipped", colour=discord.Colour.green()
            )
        else:
            embed = discord.Embed(
                title=f"You do not own this badge", colour=discord.Colour.red()
            )
    else:
        embed = discord.Embed(
            title=f"Bagde does not exist", colour=discord.Colour.red()
        )
    await message.reply(embed=embed)
    set_userdata(message.author, userdata)


if __name__ == "__main__":
    for x in range(1, 500):
        print(f"Level {x} needs {amount_for_level(x)} XP to level up.")
