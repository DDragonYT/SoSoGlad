import discord
from discord import app_commands
import json
from event import *
from wallet import *
from badge import player_badges, add_badge
from badge import Badge
from random import randint

datajson = json.load(open("data.json","r"))
REFERENCES = datajson["references"] 
ODDS_REFERENCES = datajson["odds_references"]
COMMANDS = {
        "!odds":tell_odds,
        "!stolengif":stolengif,
        "so so coinflip":coinflip,
        "so so roll":dieroll,
        "!coinflip":coinflip,
        "!roll":dieroll,
        "!badges":player_badges,
        "!wallet":wallet,
        "!daily":wallet_daily,
        "!help":help_command,
    }

with open("secret.key", "r") as keysecret:
    api_key = keysecret.readline()


class MyClient(discord.Client):
    user: discord.ClientUser

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = MyClient(intents=intents)       

@bot.event
async def on_ready():
        print(f'Logged on as {bot.user}!')      
        with open("stolengif.txt", "r") as stolen:
            bot.stolen_gif = stolen.readline()
        bot.roll_history = {
        "6":[],
        "10":[],
        "20":[],
        "100":[],
        "1000":[]
        }
            

@bot.event    
async def on_message(message):
    print(f'Message from {message.author}: {message.content}')

    await roll_event(bot, message)

    if message.content.split(" ")[0].lower() in COMMANDS.keys():
        await COMMANDS[message.content.split(" ")[0].lower()](bot, message)
        await add_badge(bot, message, "hacker")
    elif message.content.lower() in COMMANDS.keys():
        await COMMANDS[message.content.lower()](bot, message)       
        await add_badge(bot, message, "hacker")

    if message.author != bot.user:
        for key in REFERENCES.keys():
            if key in message.content.lower():
                await message.reply(REFERENCES[key])
                await add_badge(bot, message, "trigger")
                break  
        if randint(1,7) == 1:
            for key in ODDS_REFERENCES.keys():
                if key in message.content.lower():
                    await message.reply(ODDS_REFERENCES[key])
                    await add_badge(bot, message, "trigger")
                    break     

    if (".gif" in message.content or ".mp4" in message.content or "tenor.com" in message.content or "giphy.com" in message.content) and randint(1,25) == 1:
        await message.reply(f"Nice gif you got there, mind if I steal it? Okay, cool. Thanks.")
        bot.stolen_gif = message.content   
        with open("stolengif.txt", "w+") as stolen:
            stolen.write(bot.stolen_gif)
        for x in range(3):
            await message.channel.send(bot.stolen_gif)

    if str(message.author) == ".sawyadalawya":
        await message.add_reaction("🫃")

    if str(message.author) == "awenshock" and randint(1,20) == 1:
        await message.reply("https://tenor.com/view/sheppy-shisha-shisha-sheppy-husky-maid-gif-21097707")
        
bot.run(api_key)