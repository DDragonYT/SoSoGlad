from badge import Badge
from random import randint

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
    Event(chance = 100, event_type = EventType.TEXT_USER, event = "hates the blacks."),
    Event(chance = 75, event_type= EventType.TEXT_USER, event = "is racially motivated."),
    Event(chance = 150, event_type = EventType.TEXT, event = f"https://tenor.com/view/confused-stare-at-paper-gif-5257839294650729742"),
    Event(chance = 300, event_type = EventType.TEXT, event = f"https://tenor.com/view/fnaf-memes-gif-12046621880058457271"),
    Event(chance = 670, event_type = EventType.TEXT, event= "‼️**6     7**‼️"),
    Event(chance = 4096, event_type = EventType.TEXT, event= "‼️**A ✨SHINY✨ MESSAGE appeared! Try to catch it while you can.**"),
    Event(chance = 40960, event_type = EventType.TEXT, event= "‼️**A ✨SHINY✨ 🔥ALPHA🔥 MESSAGE appeared! Try to catch it while you can.**"),
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

async def roll_event(self, message):
    for ev in roll_events:
        if randint(1, ev.chance) == 1:
            if ev.event_type == EventType.TEXT:
                await message.reply(ev.event)
            elif ev.event_type == EventType.TEXT_USER:
                await message.reply(f"‼️**{str(message.author)} {ev.event}**‼️")
            elif ev.event_type == EventType.ACTION:
                ev.event()
