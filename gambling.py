from badge import Badge, BADGE_DATA, add_badge, badge_search, sell_badge
from random import randint
from userdata import *
import json
import discord
from embed import gen_error
from enum import Enum
from asyncio import sleep

DIE_SIDES = ["6", "10", "20", "100", "1000"]


async def coinflip(self, message):
    flip = randint(1, 2)
    if flip == self.flip_streak["num"]:
        self.flip_streak["len"] += 1
    else:
        self.flip_streak["num"] = flip
        self.flip_streak["len"] = 1
    if self.flip_streak["len"] in [5, 7, 10, 15, 25]:
        streak_text = f"\nThats a streak of {self.flip_streak["len"]}!"
        await add_badge(self, message, f"flip_{self.flip_streak["len"]}")
    else:
        streak_text = ""
    result = "heads" if flip == 1 else "tails"
    embed = discord.Embed(
        title=f"🪙  It's {result}!  🪙{streak_text}", colour=discord.Colour.blue()
    )
    await message.reply(embed=embed)


async def dieroll(self, message):
    max_roll = 6
    command_params = message.content.split(" ")
    if len(command_params) > 1:
        if command_params[1] in DIE_SIDES:
            max_roll = int(command_params[1])
    roll = randint(1, max_roll)
    self.roll_history[str(max_roll)].append(roll)
    output = f"🎲  You rolled a {roll} on a D{max_roll}!  🎲"
    print(self.roll_history[str(max_roll)])
    if len(self.roll_history[str(max_roll)]) > 2:
        if (
            self.roll_history[str(max_roll)][0]
            == self.roll_history[str(max_roll)][1]
            == self.roll_history[str(max_roll)][2]
        ):
            await add_badge(self, message, f"consistent_{max_roll}")
            output += "\nThat's three in a row!"
            add_badge(self, message, f"roll_{max_roll}")
            self.roll_history[str(max_roll)] = []
        else:
            self.roll_history[str(max_roll)].pop(0)
    embed = discord.Embed(title=output, colour=discord.Colour.blue())
    await message.reply(embed=embed)
    if roll == 1000:
        await add_badge(self, message, "high_roller")


async def gamble(self, message):
    bet_amt = 10
    userdata = get_userdata(message.author)
    command_params = message.content.split(" ")
    if len(command_params) > 1:
        bet_amt = int(command_params[1])
    if bet_amt > 0:
        if userdata["coins"] > bet_amt:   
            multiplier = (randint(0, 2000000000000000000000000000000000000000000)) / 1000000000000000000000000000000000000000000
            jackpot_roll = randint(0,30)
            if jackpot_roll == 10:
                    multiplier += 3
            result = round(bet_amt * multiplier)
            embed = discord.Embed(
                title=f"You gamble {bet_amt} coins...",
                colour=discord.Colour.yellow(),
            )
            await message.reply(embed=embed)
            userdata["coins"] -= bet_amt
            set_userdata(message.author, userdata)

            await sleep(3)

            userdata["coins"] += result
            set_userdata(message.author, userdata)
            embed = discord.Embed(
                title=f"You got {result} coins back!",
                colour=discord.Colour.yellow(),
            )
            if multiplier > 2:
                embed = discord.Embed(
                title=f"You hit the Jackpot! 🎰 You get {result} coins back!",
                colour=discord.Colour.yellow(),
            )
                await add_badge(self, message, f"jackpot")
            if result > bet_amt:   
                embed.description +=f" You profited {result - bet_amt} coins!"
                await message.reply(embed = embed)
            elif bet_amt > result:
                embed.colour = discord.Colour.red()
                embed.description +=f" You lost {bet_amt - result} coins."
            else:
                embed.description +=f" You profit nothing and lose nothing. Impressive"
                await add_badge(self, message, f"even")
        else:
            embed_too_poor = discord.Embed(
                    title=f"You can't afford that bet.", colour=discord.Colour.red()
                )
            await message.reply(embed = embed_too_poor)

    else:
        embed_bet_more_than_zero = discord.Embed(
            title=f"You must bet more than 0 coins", colour=discord.Colour.red()
        )
        await message.reply(embed = embed_bet_more_than_zero)
