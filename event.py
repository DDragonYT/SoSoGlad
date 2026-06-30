from badge import Badge, BADGE_DATA, add_badge, badge_search, sell_badge
from random import randint
import json
import discord
from embed import gen_error
from enum import Enum


datajson = json.load(open("data.json","r"))
ANNOUNCEMENT_CHANNEL = int(datajson["announcement_channel"])


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
    Event(chance = 100, event_type= EventType.TEXT_USER, 
        event = "is racially motivated.",
        badge="racially_motivated"),

    Event(
        chance = 150,
        event_type= EventType.ACTION,
        event = stolengif,
        ),

    Event(chance = 200, event_type = EventType.TEXT_USER, 
        event = "hates the blacks.",
        badge="maga"),

    Event(chance = 200, event_type = EventType.TEXT, 
          event = ["https://tenor.com/view/confused-stare-at-paper-gif-5257839294650729742","I'm So So Sad..."]),

    Event(chance = 300, event_type = EventType.TEXT, 
        event = ["https://tenor.com/view/fnaf-memes-gif-12046621880058457271",
                 "https://tenor.com/view/oceanmam-fnaf-jumpscare-gif-22911379",
                 "https://tenor.com/view/fnaf-freddy-fazbear-jumpscare-gif-12284636",
                 "https://tenor.com/view/fnaf-2-balloon-boy-jumpscare-gif-5074633416731518593",
                 "https://tenor.com/view/fnaf-chica-jumpscare-fnaf-4-gif-5372369601290908556",
                 "https://tenor.com/view/susto-fnaf-gif-21057159",
                 "https://tenor.com/view/toy-bonnie-jumpscare-gif-20614720",
                 "https://tenor.com/view/plushtrap-bunny-nightmare-jumpscare-fnaf-gif-13184354444220064040",
                 "Jasper Jumpscare! https://media.discordapp.net/attachments/857987097743196202/1521359779614687403/Snapchat-1587957522.jpg?ex=6a448c34&is=6a433ab4&hm=0e8defbca4535eae968ac78e6f2403d73fbc24575098a595138fa7771ca1f23c&=&format=webp&width=481&height=856"
                 ],
        badge="scare_survivor"),

    Event(chance = 500, event_type = EventType.TEXT, 
        event= "67! 67! Hahahaha! 67!",
        badge="six_seven"),

    Event(chance = 2048, event_type = EventType.TEXT, 
        event= "**A ✨SHINY✨ MESSAGE appeared! Try to catch it while you can.**",
        badge="shiny_hunter"),

    Event(chance = 20480, event_type = EventType.TEXT, 
        event= "**A ✨SHINY✨ 🔥ALPHA🔥 MESSAGE appeared! Try to catch it while you can.**",
        badge="alpha_shiny_hunter"),
    Event(chance = 250, event_type = EventType.TEXT,
        event= ["A wild Jasper has appeared https://cdn.discordapp.com/attachments/857987097743196202/1521361281364263033/JASPER.jpg?ex=6a448d9b&is=6a433c1b&hm=d9b887103467fa8d3ec5636eda64f61bbf1a50fca5953d80ea40f83ba3585f2c&",
                "A wild Jasper has appeared https://cdn.discordapp.com/attachments/857987097743196202/1521361280882053141/FullSizeR.jpg?ex=6a448d9a&is=6a433c1a&hm=7e88f8449c21da4637f5ea6df2574be6e98a28817b55e4b0cd3aa008cf3aeb20&",
                "A wild Jasper has appeared https://cdn.discordapp.com/attachments/857987097743196202/1521359780680040629/2a60f2c0-7bdd-482d-8dfe-92a3fa08c617.jpg?ex=6a448c35&is=6a433ab5&hm=67e96bcedd0b5586fe7a7c1909f99f8f68df6d61bdf34f1bc7cb7ccc5b40ca35&",
                "A wild Jasper has appeared https://cdn.discordapp.com/attachments/857987097743196202/1521359780164145162/Snapchat-1478374357.jpg?ex=6a448c35&is=6a433ab5&hm=1f42c719cd2a0382002485bb729837def3ff1e20712d55f20a9e0d864944adc2&",
                "A wild Jasper has appeared https://cdn.discordapp.com/attachments/857987097743196202/1521359779921006713/Snapchat-948985759.jpg?ex=6a448c35&is=6a433ab5&hm=b8d594b276ba7791963a11850f792b3aa4acb183e7e07115b153b54f6e1e22f6&",
                "A wild Jasper has appeared https://cdn.discordapp.com/attachments/857987097743196202/1521359779614687403/Snapchat-1587957522.jpg?ex=6a448c34&is=6a433ab4&hm=0e8defbca4535eae968ac78e6f2403d73fbc24575098a595138fa7771ca1f23c&",
                "A wild Jasper has appeared https://cdn.discordapp.com/attachments/857987097743196202/1521359779384131746/Snapchat-1177398872.jpg?ex=6a448c34&is=6a433ab4&hm=63bfffb6a61c10888c4751b82f7554ce9cf7a38cdba3ebc591b7a8ab456e4cfb&"
                ],
        badge="jasper")
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
- !daily - Claims your daily login reward
- !wallet [user] - Displays yours or target users wallet stats
- !roll [6/10/20/100/1000] - Rolls a random number from 1 to the target
- !coinflip - Does a coinflip
- !badges [user] - Displays yours or target users badge collection
- !stolengif - Displays current stolen GIF
- !binfo [badgename/ID] - Displays infomation about target badge
- !sell [badge ID] [quantity] - Sells the a quantity of the entered badge for half of its value. Uses 4 gems per sale.
- !shop - Displays the shop
- !inventory (!inv) [user] - Displays yours or target users inventory  
- !buy [item ID] [quantity] - Purchases items from the shop
- !use [item ID] - Uses an item if usable
- !pets [user] - Displays yours or target users pet collection
- !pinfo [pet ID] - Displays information about target pet
- !gather [resource type] - Gathers target resource type
- !gamble [bet] - Gambles chosen amount of coins. Default is 10
- !gift [user] [coins] - Gifts target user chosen amount of your coins""")
    await message.reply(embed=embed)

async def tell_odds(self, message):
    embed = discord.Embed(title="Odds List", description="You don't want me to spoil this, do you?")
    await message.reply(embed=embed)  
    
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