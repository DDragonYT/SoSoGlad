from badge import Badge
from user import add_badge, badgedata
from random import randint
import json
import discord

from enum import Enum

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

roll_events = [
    Event(chance = 75, event_type= EventType.TEXT_USER, 
        event = "is racially motivated.",
        badge="racially_motivated"),

    Event(chance = 100, event_type = EventType.TEXT_USER, 
        event = "hates the blacks.",
        badge="maga"),

    Event(chance = 150, event_type = EventType.TEXT, 
          event = f"https://tenor.com/view/confused-stare-at-paper-gif-5257839294650729742"),

    Event(chance = 300, event_type = EventType.TEXT, 
        event = f"https://tenor.com/view/fnaf-memes-gif-12046621880058457271"),

    Event(chance = 670, event_type = EventType.TEXT, 
        event= "‼️**6     7**‼️",
        badge="six_seven"),

    Event(chance = 4096, event_type = EventType.TEXT, 
        event= "‼️**A ✨SHINY✨ MESSAGE appeared! Try to catch it while you can.**",
        badge="shiny_hunter"),

    Event(chance = 40960, event_type = EventType.TEXT, 
        event= "‼️**A ✨SHINY✨ 🔥ALPHA🔥 MESSAGE appeared! Try to catch it while you can.**",
        badge="alpha_shiny_hunter"),
]
    
   
async def tell_odds(self, message):
        await message.reply(

        """There is a:
- 1/75 chance of being racially motivated
- 1/100 chance of hating the blacks
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
    await message.reply(f"🎲 You rolled a {randint(1,6)}! 🎲")

async def player_badges(self, message):
    command = str(message.content).split(" ")
    if len(command) > 1:
        target = command[1]
        print(target)
        if "<" in target:
            user_id = int(target.strip("<>@"))
            print(f"{user_id=}")
            target = self.get_user(user_id)
            print(target)
    else:
        target = message.author
        

    output = ""
    try:
        with open(f"users/{target}.json", "rb") as userjson:
            userdata = json.load(userjson)
        output += f"**{target}'s Badges:**"
        user_badges = userdata["badges"]
        for badge in user_badges.keys():
            badgeinfo = badgedata[badge]
            badge_level = user_badges[badge]["lvl"]
            level_text = f" Level {badge_level}" if badge_level > 1 else ""
            output += f"\n- {badgeinfo.image} *{badgeinfo.title}{level_text}* ({badgeinfo.rarity.name})"
    except:
        output += f"{target} doesn't have any badges!"
    await message.reply(output)



async def roll_event(self, message):
    for ev in roll_events:
        if randint(1, ev.chance) == 1:
            if ev.event_type == EventType.TEXT:
                await message.reply(ev.event)
            elif ev.event_type == EventType.TEXT_USER:
                await message.reply(f"‼️**{str(message.author)} {ev.event}**‼️")
            elif ev.event_type == EventType.ACTION:
                ev.event()
            await add_badge(self, message.author, "thrill_seeker")
            if ev.badge:
                await add_badge(self, message.author, ev.badge)
                
