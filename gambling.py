from _ssg_utils import *
from _globalvars import *

from badge import Badge, BADGE_DATA, add_badge, badge_search, sell_badge
from random import randint
import json
import discord
from enum import Enum
from asyncio import sleep


DIE_SIDES = ["6", "10", "20", "100", "1000"]
DEFAULT_DECK = ["AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS",
                "AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC",
                "AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD",
                "AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH"]
BLACKJACK_ACTIONS = ["hit","stand"]
blackjack_games = {

}

class BlackjackGame():
    def __init__(self):
        self.deck = DEFAULT_DECK
        self.player_hand = []
        self.dealer_hand = []
    


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
    badge = None
    if message.author.name in BUSY_USER.keys():
        if BUSY_USER[message.author.name]:
            await message.reply(embed=gen_error("You are already busy."))
            return
    bet_amt = 10
    userdata = get_userdata(message.author)
    command_params = message.content.split(" ")
    if len(command_params) > 1:
        bet_amt = int(command_params[1])
    if bet_amt > 0:
        if userdata["coins"] >= bet_amt:   
            BUSY_USER[message.author.name] = True # Let the game know that the user is busy
            multiplier = (randint(0, 2000000000000000000000000000000000000000000)) / 1000000000000000000000000000000000000000000
            jackpot_roll = randint(0,30)
            if jackpot_roll == 10:
                    multiplier += 3
            result = round(bet_amt * multiplier)
            embed = discord.Embed(
                title=f"You gamble {bet_amt} coins...",
                colour=discord.Colour.yellow(),
            )
            embed.set_thumbnail(url="https://bluemoji.io/cdn-proxy/646218c67da47160c64a84d5/66b3e99627091900881d8abc_61.png")
            await message.reply(embed=embed)
            userdata["coins"] -= bet_amt
            set_userdata(message.author, userdata)

            await sleep(3)
            BUSY_USER[message.author.name] = False # Once the user is done, make sure they can do stuff again

            userdata["coins"] += result
            embed = discord.Embed(
                title=f"You got {result} coins back!",
                colour=discord.Colour.yellow(),
            )
            if multiplier > 1:
                badge = "jackpot"
                embed = discord.Embed(
                title=f"You hit the Jackpot! 🎰 You get {result} coins back!",
                colour=discord.Colour.yellow(),
            )
                embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/88021-bluemoji-75.png")


            if result > bet_amt:   
                profit = result - bet_amt
                embed.description = f" You profited {profit} coins! That's a {round(((result)/bet_amt)*100,2)}% return rate."
                if not "biggest_win" in userdata.keys():
                    userdata["biggest_win"] = profit
                else:
                    if profit > userdata["biggest_win"]:
                        userdata["biggest_win"] = profit
                        embed.description += "\n\nThat is your new biggest win!!"

            elif bet_amt > result:
                embed.colour = discord.Colour.red()
                embed.description  =f" You lost {bet_amt - result} coins. That's a {round(((result)/bet_amt)*100,2)}% return rate." 
                if not embed.thumbnail:
                    embed.set_thumbnail(url="https://bluemoji.io/cdn-proxy/646218c67da47160c64a84d5/66b3ea739479633d9833e202_41.png")

            else:
                embed.description = f" You profit nothing and lose nothing. Impressive"
                if not embed.thumbnail:
                    embed.set_thumbnail(url="https://api.fstik.app/file/AAMCAgADFQABanknfdS_FA1jxWRKzKhZ7QY50rEAAscSAAJcDWFI4dVw6EqR6p0BAAdtAAM9BA/sticker.webp")

                if bet_amt > 9:
                    badge = "even"

            set_userdata(message.author, userdata)
            if not embed.thumbnail:
                embed.set_thumbnail(url="https://bluemoji.io/cdn-proxy/646218c67da47160c64a84d5/64fae09ea069231209494e10_90.png")
        else:
            embed_too_poor = discord.Embed(
                    title=f"You can't afford that bet.", colour=discord.Colour.red()
                )
            await message.reply(embed = embed_too_poor)
            return
        
        await message.reply(embed = embed)
    else:
        embed_bet_more_than_zero = discord.Embed(
            title=f"You must bet more than 0 coins", colour=discord.Colour.red()
        )
        await message.reply(embed = embed_bet_more_than_zero)

    if badge:
        await add_badge(self, message, badge)

# async def blackjack(self, message):
#     if not message.author in blackjack_games.keys():
#         bet_amt = 10
#         userdata = get_userdata(message.author)
#         command_params = message.content.split(" ")

#         if len(command_params) > 1:
#             try:
#                 bet_amt = int(command_params[1])
#             except:
#                 message.reply(embed = gen_error("This is not a valid gamble amount."))

#         if not userdata["coins"] >= bet_amt:
#             message.reply(embed = gen_error("You cannot afford this black man named Jack."))
#             return
#         blackjack_games[]
        
#     else:
#         command_params = message.content.split(" ")
#         if not len(command_params) > 2:
#             message.reply(embed = gen_error("Please enter an action."))
#             return
#         if not command_params[1] in BLACKJACK_ACTIONS:
#             message.reply(embed = gen_error(f"{command_params[1]} is not a valid Blackjack action."))