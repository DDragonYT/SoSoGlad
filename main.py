import discord
import json
from event import *
from badge import Badge
from random import randint

references, odds_references = {}, {}

datajson = json.load(open("data.json","r"))
references = datajson["references"]
odds_references = datajson["odds_references"]


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        with open("stolengif.txt", "r") as stolen:
            self.stolen_gif = stolen.readline()

        self.events = {
        "!odds":tell_odds,
        "!stolengif":stolengif,
        "so so coinflip":coinflip,
        "so so roll":dieroll,
        "!coinflip":coinflip,
        "!roll":dieroll,
    }
        
        self.rngevents = [
        ]
        
    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

        await roll_event(self, message)

        if message.author != self.user:
            for key in references.keys():
                if key in message.content.lower():
                    await message.reply(references[key])
                    break  
            if randint(1,7) == 1:
                for key in odds_references.keys():
                    if key in message.content.lower():
                        await message.reply(odds_references[key])
                        break

        

        if (".gif" in message.content or ".mp4" in message.content or "tenor.com" in message.content or "giphy.com" in message.content) and randint(1,25) == 1:
            await message.reply(f"Nice gif you got there, mind if I steal it? Okay, cool. Thanks.")
            self.stolen_gif = message.content
            with open("stolengif.txt", "w+") as stolen:
                stolen.write(self.stolen_gif)
            for x in range(3):
                await message.channel.send(self.stolen_gif)





        if str(message.author) == ".sawyadalawya":
            await message.add_reaction("🫃")

        if str(message.author) == "awenshock" and randint(1,4) == 1:
            await message.reply("https://tenor.com/view/sheppy-shisha-shisha-sheppy-husky-maid-gif-21097707")
            
        if message.content in self.events.keys():
            await self.events[message.content](self, message)


    


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('MTA1NjI5NTc1NjE0MDY1ODc3OA.GHiBFv.wkusdFBNnvWeLq2DDHOfZa-3qtO0etd48KB8GU')