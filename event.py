from badge import Badge, BADGE_DATA, add_badge, badge_search, sell_badge
from random import randint
import json
import discord
from embed import gen_error
from enum import Enum


datajson = json.load(open("data.json","r"))
ANNOUNCEMENT_CHANNEL = int(datajson["announcement_channel"])
DIE_SIDES = ["6","10","20","100","1000"]


class EventType(Enum):
    TEXT = 1
    TEXT_USER = 2
    ACTION = 3

class Event():
    def __init__(self, chance: int, event_type : EventType, event, badge = None):
        self.chance = chance
        self.badge = badge
        self.event = event
        self.event_type = event_type

async def stolengif(self:discord.User, message:discord.Message):
    await message.channel.send(self.stolen_gif)

ROLL_EVENTS = [
    Event(chance = 200, event_type= EventType.TEXT_USER, 
        event = "is racially motivated.",
        badge="racially_motivated"),

    Event(
        chance=300,
        event_type= EventType.ACTION,
        event = stolengif,
        ),

    Event(chance = 300, event_type = EventType.TEXT_USER, 
        event = "hates the blacks.",
        badge="maga"),

    Event(chance = 350, event_type = EventType.TEXT, 
          event = ["https://tenor.com/view/confused-stare-at-paper-gif-5257839294650729742","I'm So So Sad..."]),

    Event(chance = 650, event_type = EventType.TEXT, 
        event = ["https://tenor.com/view/fnaf-memes-gif-12046621880058457271",
                 "https://tenor.com/view/oceanmam-fnaf-jumpscare-gif-22911379",
                 "https://tenor.com/view/fnaf-freddy-fazbear-jumpscare-gif-12284636",
                 "https://tenor.com/view/fnaf-2-balloon-boy-jumpscare-gif-5074633416731518593",
                 "https://tenor.com/view/fnaf-chica-jumpscare-fnaf-4-gif-5372369601290908556",
                 "https://tenor.com/view/susto-fnaf-gif-21057159",
                 "https://tenor.com/view/toy-bonnie-jumpscare-gif-20614720",
                 "https://tenor.com/view/plushtrap-bunny-nightmare-jumpscare-fnaf-gif-13184354444220064040"
                 ],
        badge="scare_survivor"),

    Event(chance = 1100, event_type = EventType.TEXT, 
        event= "67! 67! Hahahaha! 67!",
        badge="six_seven"),

    Event(chance = 4096, event_type = EventType.TEXT, 
        event= "**A ✨SHINY✨ MESSAGE appeared! Try to catch it while you can.**",
        badge="shiny_hunter"),

    Event(chance = 40960, event_type = EventType.TEXT, 
        event= "**A ✨SHINY✨ 🔥ALPHA🔥 MESSAGE appeared! Try to catch it while you can.**",
        badge="alpha_shiny_hunter"),
]

async def bsell(self, message):
    command_params = message.content.split(" ")
    if len(command_params) > 1:
        quantity = 1
        deluxe_sell = False
        if len(command_params) > 2:
            try:
                quantity = int(command_params[2])
            except:
                await message.reply(embed=gen_error("Invalid quantity, please enter an integer. Defaulted to quantity of 1."))
        if len(command_params) > 3:
            if command_params[3] == "Deluxe":
                deluxe_sell = True
        badge_search(command_params[1])
        if command_params[1] in BADGE_DATA.keys():
            sell_response, sell_price = sell_badge(message.author, command_params[1], deluxe_sell, quantity)
            print(sell_response)
            if type(sell_response) == int:
                embed = discord.Embed(title=f"Paid {sell_price} gems to sell {quantity} {BADGE_DATA[command_params[1]].title}(s) for {sell_response} coins!",colour=discord.Colour.yellow())
                await message.reply(embed=embed)
            else:
                await message.reply(embed=gen_error(sell_response))
        else:
            await message.reply(embed=gen_error("This badge doesn't exist! Make sure you're using badges ID!"))

        

async def give_stuff(self, message):
    command_params = message.content.split(" ")
    if len(command_params) > 3:
        pass


async def help_command(self, message):
    embed = discord.Embed(title="SoSoGlad Commands", description="""
- !daily - claims your daily login reward
- !wallet [user] - shows yours or target users wallet stats
- !roll [6/10/20/100/1000] - rolls a random number from 1 to the target
- !coinflip - returns heads or tails
- !badges [user] - shows yours or target users badge collection
- !stolengif - sends the last stolen gif
- !binfo [badgename/id] - Shows info about the entered badge name
- !sell [badge ID] [quantity] - Sells the a quantity of the entered badge for half of its value. Uses 4 gems per sale.""")
    await message.reply(embed=embed)

async def tell_odds(self, message):
    embed = discord.Embed(title="Odds List", description="You don't want me to spoil this, do you?")
    await message.reply(embed=embed)  
    
async def coinflip(self, message):
    flip = randint(1,2)
    if flip == self.flip_streak["num"]:
        self.flip_streak["len"] += 1
    else:
        self.flip_streak["num"] = flip
        self.flip_streak["len"] = 1
    if self.flip_streak["len"] in [5,7,10,15,25]:
        streak_text = f"\nThats a streak of {self.flip_streak["len"]}!"
        await add_badge(self, message, f"flip_{self.flip_streak["len"]}")
    else:
        streak_text = ""
    result = "heads" if flip == 1 else "tails"
    embed = discord.Embed(title=f"🪙  It's {result}!  🪙{streak_text}", colour=discord.Colour.blue())
    await message.reply(embed=embed)

async def dieroll(self, message):
    max_roll = 6
    command_params = message.content.split(" ")
    if len(command_params) > 1:
        if command_params[1] in DIE_SIDES:
            max_roll = int(command_params[1])
    roll = randint(1,max_roll)  
    self.roll_history[str(max_roll)].append(roll)
    output = f"🎲  You rolled a {roll} on a D{max_roll}!  🎲"
    print(self.roll_history[str(max_roll)])
    if len(self.roll_history[str(max_roll)]) > 2:
        if self.roll_history[str(max_roll)][0] == self.roll_history[str(max_roll)][1] == self.roll_history[str(max_roll)][2]:
            await add_badge(self, message, f"consistent_{max_roll}")
            output += ("\nThat's three in a row!")
            add_badge(self, message, f"roll_{max_roll}")
            self.roll_history[str(max_roll)] = []
        else:
            self.roll_history[str(max_roll)].pop(0)
    embed = discord.Embed(title=output, colour=discord.Colour.blue())
    await message.reply(embed=embed)
    if roll == 1000:
        await add_badge(self, message, "high_roller")

async def roll_event(self, message):
    for ev in ROLL_EVENTS:
        if randint(1, ev.chance) == 1:
            if ev.event_type == EventType.TEXT:
                if type(ev.event) == list:
                    txt = ev.event[randint(1, len(ev.event)-1)]
                else:
                    txt = ev.event
                await message.reply(txt)
            elif ev.event_type == EventType.TEXT_USER:
                await message.reply(f"{str(message.author)} {ev.event}")
            elif ev.event_type == EventType.ACTION:
                await ev.event(self, message)
            if ev.badge:
                await add_badge(self, message, ev.badge)
            else:
                await add_badge(self, message, "thrill_seeker")