import discord
from discord import app_commands
from wallet import *
from random import randint
import asyncio
from embed import *

action_using = {

}

async def gather(self, message):
    command_params = message.content.split(" ")
    if message.author.name in action_using.keys():
        if action_using[message.author.name]:
            await message.reply(embed = gen_error("😡 You're Already Busy! 😡"))
            return
    if command_params[1] == "rock":
        embed = discord.Embed(title="🪨 Mining Rock... 🪨")
        await message.reply(embed = embed)
        action_using[message.author.name] = True
        await asyncio.sleep(10)
        action_using[message.author.name] = False
        embed.title="🪨 You Mined a Rock! 🪨"
        await message.reply(embed = embed)
        add_to_resource(message.author, "stone")
    elif command_params[1] == "wood":
        embed = discord.Embed(color = discord.Colour.dark_orange(), title="🪵 Chopping Wood... 🪵")
        await message.reply(embed = embed)
        action_using[message.author.name] = True
        await asyncio.sleep(10)
        action_using[message.author.name] = False
        embed.title="🪵 You Chopped some Wood! 🪵"
        await message.reply(embed = embed)
        add_to_resource(message.author, "wood")

def add_to_resource(user, resource, quantity = 1):
    userdata = get_userdata(user)
    if not "inventory" in userdata.keys():
        userdata["inventory"] = {}
    if not resource in userdata["inventory"]:
        userdata["inventory"][resource] = {"quantity": 0}
    userdata["inventory"][resource]["quantity"] += quantity
    set_userdata(user, userdata)