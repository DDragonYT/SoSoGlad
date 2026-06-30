import discord
from discord import app_commands
import json
from wallet import *
from random import randint
import time
import asyncio

def add_to_resource(user, resource, quantity = 1):
    userdata = get_userdata(user)
    if not "inventory" in userdata.keys():
        userdata["inventory"] = {}
    if not resource in userdata["inventory"]:
        userdata["inventory"][resource] = {"quantity": 0}
    userdata["inventory"][resource]["quantity"] += quantity
    set_userdata(user, userdata)

async def gather(self, message):
    command_params = message.content.split(" ")
    if command_params[1] == "rock":
        embed = discord.Embed(title="🪨 Mining Rock... 🪨")
        message.reply(embed == embed)
        asyncio.sleep(1000)
        embed = discord.Embed(title="🪨 You Mined a Rock! 🪨")
        message.reply(embed == embed)
        add_to_resource(message.author, "rock")

# async def chop_wood(self, message):