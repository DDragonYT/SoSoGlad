from badge import Badge, badgedata, add_badge
from random import randint
import json
import discord
from enum import Enum

ANNOUNCEMENT_CHANNEL = 1461155461075042465
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

ROLL_EVENTS = [
    Event(chance = 150, event_type= EventType.TEXT_USER, 
        event = "is racially motivated.",
        badge="racially_motivated"),

    Event(chance = 200, event_type = EventType.TEXT_USER, 
        event = "hates the blacks.",
        badge="maga"),

    Event(chance = 300, event_type = EventType.TEXT, 
          event = f"https://tenor.com/view/confused-stare-at-paper-gif-5257839294650729742"),

    Event(chance = 600, event_type = EventType.TEXT, 
        event = f"https://tenor.com/view/fnaf-memes-gif-12046621880058457271",
        badge="scare_survivor"),

    Event(chance = 1000, event_type = EventType.TEXT, 
        event= "‼️**6     7**‼️",
        badge="six_seven"),

    Event(chance = 4096, event_type = EventType.TEXT, 
        event= "‼️**A ✨SHINY✨ MESSAGE appeared! Try to catch it while you can.**",
        badge="shiny_hunter"),

    Event(chance = 40960, event_type = EventType.TEXT, 
        event= "‼️**A ✨SHINY✨ 🔥ALPHA🔥 MESSAGE appeared! Try to catch it while you can.**",
        badge="alpha_shiny_hunter"),
]
    
async def help_command(self, message):
    await message.reply("""**SoSoGlad Commands:**
- !daily - claims your daily login reward
- !wallet [user] - shows yours or target users wallet stats
- !roll [6/10/20/100/1000] - rolls a random number from 1 to the target
- !coinflip - returns heads or tails
- !badges [user] - shows yours or target users badge collection
- !stolengif - sends the last stolen gif""")   

async def tell_odds(self, message):
        await message.reply(

        """There is a:
- 1/150 chance of being racially motivated
- 1/200 chance of hating the blacks
- 1/670 chance of me wanting to kill myself
- 1/4096 chance of a shiny message appearing
- 1/40960 chance of a shalpha message appearing
There are more events to look forward to, just you wait!""")    

async def stolengif(self, message):
    await message.reply(self.stolen_gif)
    
async def coinflip(self, message):
    if randint(1,2) == 1:
        await message.reply("🪙 It's heads!")
    else:
        await message.reply("It's tails! 🪙 ")

async def dieroll(self, message):
    max_roll = 6
    command_params = message.content.split(" ")
    if len(command_params) > 1:
        if command_params[1] in DIE_SIDES:
            max_roll = int(command_params[1])
    roll = randint(1,max_roll)
    self.roll_history[str(max_roll)].append(roll)
    output = f"🎲 You rolled a {roll} on a D{max_roll}! 🎲"
    print(self.roll_history[str(max_roll)])
    if len(self.roll_history[str(max_roll)]) > 2:
        if self.roll_history[str(max_roll)][0] == self.roll_history[str(max_roll)][1] == self.roll_history[str(max_roll)][2]:
            await add_badge(self, message, f"consistent_{max_roll}")
            output += ("\nThat's three in a row!")
            self.roll_history[str(max_roll)] = []
        else:
            self.roll_history[str(max_roll)].pop(0)
    await message.command(output)      

async def roll_event(self, message):
    # roll = randint(0,len(ROLL_EVENTS)-1)
    # ev = ROLL_EVENTS[roll]
    for ev in ROLL_EVENTS:
        if randint(1, ev.chance) == 1:
            if ev.event_type == EventType.TEXT:
                await message.reply(ev.event)
            elif ev.event_type == EventType.TEXT_USER:
                await message.reply(f"‼️**{str(message.author)} {ev.event}**‼️")
            elif ev.event_type == EventType.ACTION:
                ev.event()
            if ev.badge:
                await add_badge(self, message, ev.badge)
            await add_badge(self, message, "thrill_seeker")
