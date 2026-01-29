from enum import Enum
from random import randint
from userdata import *
import os
datajson = json.load(open("data.json","r"))
ANNOUNCEMENT_CHANNEL = int(datajson["announcement_channel"])
BADGE_VALUES = {}


class BadgeRarity(Enum):
    COMMON = "Common"
    DRACONIC = "Draconic"
    RARE = "Rare"
    WHIMSIC = "WHIMSIC"
    LEGENDARY = "Legendary"
    UNREAL = "Unreal"
    GODLY = "Godly"

rarity_values = {
    BadgeRarity.COMMON: 10,
    BadgeRarity.RARE: 25,
    BadgeRarity.WHIMSIC: 50,
    BadgeRarity.LEGENDARY: 500,
    BadgeRarity.DRACONIC: 3000,
    BadgeRarity.UNREAL:20000,
    BadgeRarity.GODLY:50000,

}

class Badge():
    def __init__(self, title, description, image, rarity, max_level = 999, sellable = True):
        self.title = title
        self.description = description
        self.image = image
        self.rarity = rarity
        self.max_level = max_level
        self.sellable = sellable

badgedata = {
    "scare_survivor": Badge(
        title="Scare Survivor Badge",
        description="Survive a super scary encounter. So brave.",
        image="👻",
        rarity=BadgeRarity.WHIMSIC
    ),
    "high_roller":Badge(
        title="High Roller Badge",
        description="Roll a 1000! You really should hit Crown.",
        image="🎰",
        rarity=BadgeRarity.DRACONIC
    ),
    "consistent_6":Badge(
        title="Rookie Gambler Badge",
        description="Roll the same number three times in a row on a D6.",
        image="🎲",
        rarity=BadgeRarity.RARE
    ),
    "consistent_10":Badge(
        title="Novice Gambler Badge",
        description="Roll the same number three times in a row on a D10. Nice!",
        image="🎲",
        rarity=BadgeRarity.RARE
    ),
    "consistent_20":Badge(
        title="Pro Gambler Badge",
        description="Roll the same number three times in a row on a D20. Awesome job!",
        image="🎲",
        rarity=BadgeRarity.LEGENDARY
    ),
    "consistent_100":Badge(
        title="Gambling Legend Badge",
        description="Roll the same number three times in a row on a D100. This is crazy. Congratulations.",
        image="🎲",
        rarity=BadgeRarity.UNREAL
    ),
    "consistent_1000":Badge(
        title="Gambling God Badge",
        description="Roll the same number three times in a row on a D1000. Stop cheating bro.",
        image="🎲",
        rarity=BadgeRarity.GODLY
    ),

    "kirky":Badge(
        title="Kirkified Badge",
        description="Earned by getting Kirkified 100 times.",
        image="🔫",
        rarity=BadgeRarity.RARE
    ),
    "victim":Badge(
        title="The Victim Badge",
        description="Get absolutely unfairly robbed.",
        image="🍺",
        rarity=BadgeRarity.RARE
    ),
    "flip_3":Badge(
        title="Micro Flipper Badge",
        description="Get absolutely unfairly robbed.",
        image="🪙",
        rarity=BadgeRarity.RARE
    ),
    "flip_5":Badge(
        title="Mini Flipper Badge",
        description="Get absolutely unfairly robbed.",
        image="🪙",
        rarity=BadgeRarity.RARE
    ),
    "flip_7":Badge(
        title="Medium Flipper Badge",
        description="Get absolutely unfairly robbed.",
        image="🪙",
        rarity=BadgeRarity.WHIMSIC
    ),
    "flip_10":Badge(
        title="Elder Flipper Badge",
        description="Get absolutely unfairly robbed.",
        image="🪙",
        rarity=BadgeRarity.DRACONIC
    ),
    "flip_25":Badge(
        title="Statical Anomaly Badge",
        description="Get absolutely unfairly robbed.",
        image="🪙",
        rarity=BadgeRarity.GODLY
    ),
    "yapper":Badge(
        title="Yapper Badge",
        description="Send 1000 messages, holy fucking yap.",
        image="🗣️",
        rarity=BadgeRarity.WHIMSIC,
    ),
    "deluxe_badge":Badge(
        title="Badge Hunter DX",
        description="Acquire a deluxe badge!",
        image="🥇",
        rarity=BadgeRarity.WHIMSIC,
    ),
    "deluxe_badge_dx":Badge(
        title="Deluxe Badge Hunter DX",
        description="Acquire a 10 deluxe badges!",
        image="🎖️",
        rarity=BadgeRarity.DRACONIC,
    ),
    "trigger" : Badge(
        title="Triggerer Badge",
        description="Trigger one of SoSoGlad's post traumatic stress disorders.",
        image="🤖",
        rarity=BadgeRarity.COMMON,
        max_level=1,
        ),
    "hacker" : Badge(
        title="Hackerman Badge",
        description="Use a SoSoGlad command. What a tech master.",
        image="🧑🏻‍💻",
        rarity=BadgeRarity.COMMON,
        max_level=1
        ),
    "thrill_seeker" : Badge(
        title="Thrill Seeker Badge",
        description="Be lucky enough to encounter an event.",
        image="🪂",
        rarity=BadgeRarity.COMMON,
        max_level=50
        ),
    "racially_motivated" : Badge(
        title="Racially Motivated Badge",
        description="Acquired by being randomly racially motivated for no reason.",
        image="🙍🏿",
        rarity=BadgeRarity.RARE
        ),
    "maga" : Badge(
        title="MAGA Badge",
        description="You really shouldn't have this one, supporter of the orange man.",
        image="🍊",
        rarity=BadgeRarity.RARE
        ),
    "six_seven" : Badge(
        title="67 Badge",
        description="Do I really need to explain this one.",
        image="♿",
        rarity=BadgeRarity.WHIMSIC
        ),
    "shiny_hunter" : Badge(
        title="Shiny Hunter Badge",
        description="Get a job bro, thats crazy.",
        image="✨",
        rarity=BadgeRarity.DRACONIC
        ),
    "alpha_shiny_hunter" : Badge(
        title="Alpha Shiny Hunter",
        description="Okay, there's no way you got this badge.",
        image="🔥",
        rarity=BadgeRarity.UNREAL
        )
}

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
    userdata = get_userdata(target)
    if "badges" in userdata.keys():
        output += f"**{target}'s Badges:**"
        user_badges = userdata["badges"]
        for badge in user_badges.keys():
            badgeinfo = badgedata[badge]
            badge_level = user_badges[badge]["lvl"]
            level_text = f" Level {badge_level}" if badge_level > 1 else ""
            output += f"\n- {badgeinfo.image} *{badgeinfo.title}{level_text}* ({badgeinfo.rarity.name})"
    else:
        output += f"\n{target} doesn't have any badges!"
    await message.reply(output)

async def add_badge(self, message, badge):
    if randint(1,300) == 1:
        badge_type = "deluxe_badges"
    else:
        badge_type = "badges"
    userdata = {}
    user = message.author
    userdata = get_userdata(user)
    if badge_type not in userdata.keys():
        userdata[badge_type] = {}
    badges = userdata[badge_type]

    if badge in badges.keys():
        if badges[badge]["lvl"] < badgedata[badge].max_level:
            badges[badge]["lvl"] += 1
            await announce_badge(self,user,badge,badge_type)

    else:
        badges[badge] = {"lvl":1}
        await announce_badge(self,user,badge, badge_type)

    set_userdata(user, userdata)


async def announce_badge(self, user, badge, badge_type):
    channel = self.get_channel(ANNOUNCEMENT_CHANNEL)
    badge_info = badgedata[badge]
    if badge_type == "deluxe_badges":
        deluxe_badge = True
    else:
        deluxe_badge = False
    await channel.send(f"""**{user.mention} got a {"Deluxe "if deluxe_badge else ""}{badge_info.title}!{" Ain't you a lucky boy!" if deluxe_badge else ""}**

{badge_info.image} {"Deluxe "if deluxe_badge else ""}{badge_info.title}
*{badge_info.description}*
({badge_info.rarity.name})
{"(DELUXE)"if deluxe_badge else ""}
""")

def calc_badges():
    global BADGE_VALUES
    directory = os.fsencode("users")
    badge_totals = {}
    for badge_type in ["badges", "deluxe_badges"]:
        if not badge_type in BADGE_VALUES.keys():
            BADGE_VALUES[badge_type] = {}

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            with open(f"users/{filename}") as filejson:
                fileobj = json.load(filejson)
                filekeys = fileobj.keys()
                for badge_type in ["badges", "deluxe_badges"]:
                    if badge_type in filekeys:  
                            
                            for badge in fileobj[badge_type]:
                                if badge_type == "badges":
                                    if badge in badge_totals.keys():
                                        badge_totals[badge] += fileobj[badge_type][badge]['lvl']
                                    else:
                                        badge_totals[badge] = fileobj[badge_type][badge]['lvl']
                                else:
                                    basevalue = rarity_values[badgedata[badge].rarity]
                                    BADGE_VALUES["deluxe_badges"][badge] = basevalue * 10

    for badge in badge_totals.keys():
        badgeqty = badge_totals[badge]
        basevalue = rarity_values[badgedata[badge].rarity]

        if badgeqty > basevalue / 5:
            valuecurve = 0.99
        else:
            valuecurve = 0.99
        BADGE_VALUES["badges"][badge] =  round(
            (valuecurve ** (badgeqty/1)) * basevalue
            ) + 1


def sell_badge(user, badgename, deluxe = False, qty=1):
    if deluxe:
        badge_type = "deluxe_badges"
    else:
        badge_type = "badges"

    userdata = get_userdata(user)
    if badgename in userdata[badge_type]:
        if userdata[badge_type][badgename]["lvl"] > qty:
            current_value = BADGE_VALUES[badge_type][badgename]
            sale_amount = qty * current_value
            userdata["coins"] += sale_amount
            userdata[badge_type][badgename]["lvl"] -= qty
        else:
            return
    else:
        return            
    set_userdata(user, userdata)
    return sale_amount

def calc_inv(user):
    userdata = get_userdata(user)
    inventory_value = 0
    for badgetype in ["badges","deluxe_badges"]:
        if badgetype in userdata.keys():
            for badge in userdata[badgetype]:
                inventory_value += BADGE_VALUES[badgetype][badge]
    return inventory_value

calc_badges()
print(BADGE_VALUES)
sell_badge("ddragonyt","six_seven", False, 1)
for user in ["ddragonyt", "bob_three", "kerselranch", "robroxian", "tc38"]:
    print(f"Inventory Value of {user}: {calc_inv(user)}")
