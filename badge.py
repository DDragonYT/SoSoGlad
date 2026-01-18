from enum import Enum
from userdata import *
ANNOUNCEMENT_CHANNEL = 1461155461075042465


class BadgeRarity(Enum):
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"
    UNREAL = "Unreal"



class Badge():
    def __init__(self, title, description, image, rarity, max_level = 999):
        self.title = title
        self.description = description
        self.image = image
        self.rarity = rarity
        self.max_level = max_level

badgedata = {
    "scare_survivor": Badge(
        title="Scare Survivor Badge",
        description="Survive a super scary encounter. So brave.",
        image="👻",
        rarity=BadgeRarity.RARE
    ),
    "high_roller":Badge(
        title="High Roller Badge",
        description="Roll a 1000! You really should hit Crown.",
        image="🎰",
        rarity=BadgeRarity.LEGENDARY
    ),
    "consistent_6":Badge(
        title="Rookie Gambler Badge",
        description="Roll the same number three times in a row on a D6.",
        image="6️⃣",
        rarity=BadgeRarity.UNCOMMON
    ),
    "consistent_10":Badge(
        title="Novice Gambler Badge",
        description="Roll the same number three times in a row on a D10. Nice!",
        image="🔟",
        rarity=BadgeRarity.RARE
    ),
    "consistent_20":Badge(
        title="Pro Gambler Badge",
        description="Roll the same number three times in a row on a D20. Awesome job!",
        image="🏋🏻",
        rarity=BadgeRarity.EPIC
    ),
    "consistent_100":Badge(
        title="Gambling Legend Badge",
        description="Roll the same number three times in a row on a D6. This is crazy. Congratulations.",
        image="💯",
        rarity=BadgeRarity.LEGENDARY
    ),
    "consistent_1000":Badge(
        title="Gambling God Badge",
        description="Roll the same number three times in a row on a D1000. Stop cheating bro.",
        image="🌏",
        rarity=BadgeRarity.UNREAL
    ),
    "kirky":Badge(
        title="Kirkified Badge",
        description="Earned by getting Kirkified 100 times.",
        image="🔫",
        rarity=BadgeRarity.UNCOMMON
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
        ),
    "racially_motivated" : Badge(
        title="Racially Motivated Badge",
        description="Acquired by being randomly racially motivated for no reaosn.",
        image="🙍🏿",
        rarity=BadgeRarity.UNCOMMON
        ),
    "maga" : Badge(
        title="MAGA Badge",
        description="You really shouldn't have this one, supporter of the orange man.",
        image="🍊",
        rarity=BadgeRarity.UNCOMMON
        ),
    "six_seven" : Badge(
        title="67 Badge",
        description="Do I really need to explain this one.",
        image="♿",
        rarity=BadgeRarity.EPIC
        ),
    "shiny_hunter" : Badge(
        title="Shiny Hunter Badge",
        description="Get a job bro, thats crazy.",
        image="✨",
        rarity=BadgeRarity.LEGENDARY
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
    try:
        userdata = get_userdata(target)
        output += f"**{target}'s Badges:**"
        user_badges = userdata["badges"]
        for badge in user_badges.keys():
            badgeinfo = badgedata[badge]
            badge_level = user_badges[badge]["lvl"]
            level_text = f" Level {badge_level}" if badge_level > 1 else ""
            output += f"\n- {badgeinfo.image} *{badgeinfo.title}{level_text}* ({badgeinfo.rarity.name})"
    except:
        output += f"\n{target} doesn't have any badges!"
    await message.reply(output)

async def add_badge(self, message, badge):
    userdata = {}
    user = message.author
    userdata = get_userdata(user)
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

    set_userdata(user, userdata)


async def announce_badge(self, user, badge):
    channel = self.get_channel(ANNOUNCEMENT_CHANNEL)
    badge_info = badgedata[badge]
    await channel.send(f"""**{user.mention} got a {badge_info.title}!**

{badge_info.image} {badge_info.title}
*{badge_info.description}*
({badge_info.rarity.name})""")