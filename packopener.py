import discord
from discord import app_commands
import json
from random import randint
import time

from economy import *
from gambling import *

datajson = json.load(open("data.json", "r"))
REFERENCES = datajson["references"]
ODDS_REFERENCES = datajson["odds_references"]
COMMANDS = {  # Defines what to enter to run a command
    "!wallet": wallet,
    "!daily": wallet_daily,
    "!help": pack_help,
    "!sell": card_sell,
    "!gift":card_gift,
    "!gamble" : gamble,

}

message_counts = {}
last_price_update = -1

with open("pack_secret.key", "r") as keysecret:
    api_key = keysecret.readline()


class MyClient(discord.Client):
    user: discord.ClientUser


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = MyClient(intents=intents)


@bot.event
async def on_ready():
    print(f"Logged on as {bot.user}!")


async def add_msgcount(user):
    """Ups the message count dictionary of the user who sent a message"""
    global message_counts
    if user in message_counts:
        message_counts[user] += 1
    else:
        message_counts[user] = 1

    if message_counts[user] % 1000 == 0:
        await add_badge(user, "yapper")


@bot.event
async def on_message(message):
    """Triggers every time a message is sent"""
    global last_price_update
    print(f"Message from {message.author}: {message.content}")
    await add_msgcount(message.author)
    curtime = int(time.localtime().tm_min / 10)
    if curtime != last_price_update:
        last_price_update = curtime
        calc_badges()
        # channel = bot.get_channel(ANNOUNCEMENT_CHANNEL)
        # embed = discord.Embed(title="Badge prices have updated!", colour=discord.Colour.green())
        # await channel.send(embed = embed)

    if message.content.split(" ")[0].lower() in COMMANDS.keys():
        await COMMANDS[message.content.split(" ")[0].lower()](bot, message)
        await add_badge(bot, message, "hacker")

    elif message.content.lower() in COMMANDS.keys():
        await COMMANDS[message.content.lower()](bot, message)
        await add_badge(bot, message, "hacker")

    elif message.author != bot.user:
        for key in REFERENCES.keys():
            if key in message.content.lower():
                reference = REFERENCES[key]
                if type(REFERENCES[key]) == list:
                    reference_text = reference[randint(0, len(reference) - 1)]
                else:
                    reference_text = reference
                await message.reply(reference_text)
                await add_badge(bot, message, "trigger")
                break
        if randint(1, 7) == 1:
            for key in ODDS_REFERENCES.keys():
                if key in message.content.lower():
                    await message.reply(ODDS_REFERENCES[key])
                    await add_badge(bot, message, "trigger")
                    break

    else:
        await roll_event(bot, message)

    if (
        ".gif" in message.content
        or ".mp4" in message.content
        or "tenor.com" in message.content
        or "giphy.com" in message.content
    ) and randint(1, 25) == 1:
        await message.reply(
            f"Nice gif you got there, mind if I steal it? Okay, cool. Thanks."
        )
        bot.stolen_gif = message.content
        await add_badge(bot, message, "victim")
        with open("stolengif.txt", "w+") as stolen:
            stolen.write(bot.stolen_gif)
        for x in range(3):
            await message.channel.send(bot.stolen_gif)

    if str(message.author) == ".sawyadalawya":
        await message.add_reaction("🫃")
    if str(message.author) == "awenshock" and randint(1, 20) == 1:
        await message.reply(
            "https://tenor.com/view/sheppy-shisha-shisha-sheppy-husky-maid-gif-21097707"
        )


bot.run(api_key)
