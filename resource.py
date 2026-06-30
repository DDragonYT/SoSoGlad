import discord
from discord import app_commands
import json
from wallet import *
from random import randint

async def mine_rock(self, message):
    embed = discord.Embed(title="This is a ", description="Test to see if Luke actgually knows what hes doing")
    await message.reply(embed=embed)  

# async def chop_wood(self, message):