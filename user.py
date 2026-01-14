import json
from badge import badgedata
import discord

async def add_badge(self, user, badge):
    userdata = {}
    try:
        with open(f"users/{user}.json", "rb") as userjson:
            userdata = json.load(userjson)
    except:
        userdata = {}
    if "badges" not in userdata.keys():
        userdata["badges"] = {}
    badges = userdata["badges"]

    if badge in badges.keys():
        if badges[badge]["lvl"] < badgedata[badge].max_level:
            badges[badge]["lvl"] += 1
            await announce_badge(self,user,badge)

    else:
        badges[badge] = {"lvl":1}
        await announce_badge(self,user,badge)

    with open(f"users/{user}.json", "w+") as userjson:
        json.dump(userdata, userjson, indent=2)


async def announce_badge(self,user,badge):
    channel = self.get_channel(1460597413478928445)
    badge_info = badgedata[badge]
    await channel.send(f"""**{user} got a {badge_info.title}!**

{badge_info.image} {badge_info.title}
*{badge_info.description}*
({badge_info.rarity.name})""")
# add_badge("ddragonyt",0)
# userdata = json.load(open("users/ddragonyt.json","rb"))
# print(userdata)
