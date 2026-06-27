import discord

def gen_error(text):
    embed = discord.Embed(
        title = text,
        color=discord.Colour.red()
    )
    return embed