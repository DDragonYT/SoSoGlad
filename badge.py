from _globalvars import *
from _ssg_utils import gen_error, target_from_message, get_userdata, set_userdata

from enum import Enum
from random import randint
import discord
import os

def badge_search(name):
    """I dunno"""
    if name in BADGE_DATA.keys():
        return name
    else:
        for key in BADGE_DATA.keys():
            badge = BADGE_DATA[key]
            if name in badge.title.lower():
                return key
    return

def badge_details(ibadge, badge):
    """Generates an embed containing all data of the inputted badge ID"""
    embed = discord.Embed(
                title=f"[{ibadge.image}] {ibadge.title}",
                description=ibadge.description,
                color= discord.Colour.green()
            )
    embed.add_field(name="Rarity", value=ibadge.rarity.name)
    embed.add_field(name="Value", value=BADGE_VALUES["badges"][badge])
    embed.add_field(name="Max Level", value=ibadge.max_level)
    embed.add_field(name="Badge ID", value=f"`{badge}`")
    embed.set_author(name="Badge Info")
    return embed

async def badge_info(self, message):
    """Checks if a badge exists, if it does generate an embed and send it"""

    command_params = message.content.split(" ")
    
    if len(command_params) > 1:
        badge = badge_search(command_params[1])
        if badge:
            ibadge:Badge = BADGE_DATA[badge]
            embed = badge_details(ibadge, badge)
            await message.reply(embed=embed)
        else:
            await message.reply(embed = gen_error("That badge doesn't exist!"))
    else:
        await message.reply(embed = gen_error("Please enter a badge name."))

async def player_badges(self, message):
    """Displays the badges of a target user"""

    target = target_from_message(self, message)
    
    userdata = get_userdata(target)
    if "badges" in userdata.keys() or "deluxe_badges" in userdata.keys():
        embed = discord.Embed(title=f"{target}'s Badges", colour=discord.Colour.green())
        userkeys = userdata.keys()
        for badgetype in BADGE_TYPES:
            if badgetype in userkeys:
                value = ""

                for badge in userdata[badgetype]:
                    badgedata = BADGE_DATA[badge]
                    leveltext = f" Tier {userdata[badgetype][badge]["lvl"]}" if userdata[badgetype][badge]["lvl"] > 1 else ""
                    value += f"\n- [{badgedata.image}] {badgedata.title}{leveltext} ({badgedata.rarity.name})"
                embed.add_field(name=badgetype.replace("_"," ").capitalize(), value=value)

        await message.reply(embed=embed)
    else:
        await message.reply(embed = gen_error(f"{target} doesn't have any badges!"))

async def add_badge(self, message, badge):
    if randint(1,300) == 1 and BADGE_DATA[badge].max_level != 1:
        badge_type = "deluxe_badges"
    else:
        badge_type = "badges"

    userdata = {}
    user = message.author
    userdata = get_userdata(user)
    if badge_type not in userdata.keys():
        userdata[badge_type] = {}
    badges = userdata[badge_type]

    if badge in badges.keys():
        if badges[badge]["lvl"] < BADGE_DATA[badge].max_level:
            badges[badge]["lvl"] += 1
            await announce_badge(self,user,badge,badge_type)


    else:
        badges[badge] = {"lvl":1}
        await announce_badge(self,user,badge, badge_type)
    set_userdata(user, userdata)


async def announce_badge(self, user, badge, badge_type):
    """Generate an embed and send it in the announcement channel"""

    channel = self.get_channel(ANNOUNCEMENT_CHANNEL) # Locate the announcement channel from the ID
    badge_info = BADGE_DATA[badge] # Load the badge data of the announced badge
    if badge_type == "deluxe_badges":
        deluxe_badge = True # If the badge is deluxe, know that
    else:
        deluxe_badge = False
    output = f"""**{user.mention} got a {"Deluxe "if deluxe_badge else ""}{badge_info.title}!{" Ain't you a lucky boy!" if deluxe_badge else ""}**""" # Generate the announcement
    ibadge:Badge = BADGE_DATA[badge] # Get badge data
    embed = badge_details(ibadge, badge) # Generate the badge details
    await channel.send(output,embed=embed) # Send the emebd


def calc_badges():
    """Calculates the value of a badge based on the amount and the base price"""
    global BADGE_VALUES
    directory = os.fsencode("users")
    badge_totals = {}
    for badge_type in ["badges", "deluxe_badges"]:
        if not badge_type in BADGE_VALUES.keys():
            BADGE_VALUES[badge_type] = {}

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json") and not "sosoglad" in filename:
            with open(f"users/{filename}") as filejson:
                fileobj = json.load(filejson)
                filekeys = fileobj.keys()
                for badge_type in ["badges", "deluxe_badges"]:
                    if badge_type in filekeys:  
                            for badge in fileobj[badge_type]:
                                if badge_type == "badges":
                                    if badge in badge_totals.keys():
                                        badge_totals[badge] += fileobj[badge_type][badge]['lvl']
                                    else:
                                        badge_totals[badge] = fileobj[badge_type][badge]['lvl']
                                else:
                                    basevalue = RARITY_VALUES[BADGE_DATA[badge].rarity]
                                    BADGE_VALUES["deluxe_badges"][badge] = basevalue * 10
    for badge in BADGE_DATA.keys():
        for badge_type in ["badges", "deluxe_badges"]:
            if badge not in BADGE_VALUES[badge_type].keys():
                BADGE_VALUES[badge_type][badge] = RARITY_VALUES[BADGE_DATA[badge].rarity]
    for badge in badge_totals.keys():
        badgeqty = badge_totals[badge]
        basevalue = RARITY_VALUES[BADGE_DATA[badge].rarity]

        if badgeqty > basevalue / 5:
            valuecurve = 0.99
        else:
            valuecurve = 0.99
        BADGE_VALUES["badges"][badge] =  round(
            (valuecurve ** (badgeqty/1)) * basevalue
            ) + 1

def sell_badge(user, badgename, deluxe = False, qty=1):
    """If user has the item, sell it based on half of it's current value"""

    if deluxe:
        badge_type = "deluxe_badges"
    else:
        badge_type = "badges"
    userdata = get_userdata(user)
    if badgename in userdata[badge_type]:
        if BADGE_DATA[badgename].max_level != 1:
            if userdata[badge_type][badgename]["lvl"] >= qty:
                if "gems" in userdata.keys():
                    if userdata["gems"] >= SELL_PRICE:
                        current_value = BADGE_VALUES[badge_type][badgename]
                        sale_amount = int(qty * current_value/2)
                        userdata["coins"] += sale_amount
                        userdata["gems"] -= SELL_PRICE
                        userdata[badge_type][badgename]["lvl"] -= qty
                        if userdata[badge_type][badgename]["lvl"] == 0:
                            del userdata[badge_type][badgename]
                    else:
                        return f"You need at least {SELL_PRICE} gems to sell a badge!", None
                else:
                    return f"You need at least {SELL_PRICE} gems to sell a badge!", None
            else:
                return f"Can't sell more than {userdata[badge_type][badgename]["lvl"]} {BADGE_DATA[badgename].title}(s)!", None
        else:
            return f"Can't sell the {BADGE_DATA[badgename].title} as it is a one time badge!", None
    else:
        return "You don't own this badge!", None
    set_userdata(user, userdata)
    return sale_amount, SELL_PRICE

def calc_inv(user):
    userdata = get_userdata(user)
    inventory_value = 0
    for badgetype in ["badges","deluxe_badges"]:
        if badgetype in userdata.keys():
            for badge in userdata[badgetype]:
                inventory_value += BADGE_VALUES[badgetype][badge] * userdata[badgetype][badge]["lvl"]
    userdata["badgeinvvalue"] = inventory_value
    userdata["net_worth"] = userdata["badgeinvvalue"] + userdata["coins"]
    set_userdata(user, userdata)
    return inventory_value
