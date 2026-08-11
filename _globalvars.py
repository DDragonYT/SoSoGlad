import json
from enum import Enum

_FILEDATAJSON = json.load(open("resources/data/data.json", "r"))

RECIPES:dict = json.load(open("resources/data/recipes.json", "r"))

class MTGPack:
    def __init__(self, price, id, image, name, rarity_chances, description):
        self.price = price
        self.id = id
        self.image = image
        self.name = name
        self.rarity_chances = rarity_chances,
        self.description = description


CARD_IMAGE = "resources/images/cards"
RARITIES = ["mythic", "rare", "uncommon", "common"]
PACKS = {
    "2ED": MTGPack(
        60,
        "2ED",
        "https://static.wikia.nocookie.net/mtgsalvation_gamepedia/images/6/6d/Unlimited_booster.jpg/revision/latest?cb=20131109150010",
        "Unlimited Edition",
        [101, 90, 60, 0],
        "Unlimited Edition, or Unlimited is the second edition of the core set. This white-bordered set consisted of the same 302 cards as the Beta print run. It was released in December 1993. "
    )
}

with open("resources/data/secret.key", "r") as keysecret:
    API_KEY = keysecret.readline()

REFERENCES = _FILEDATAJSON["references"]
ODDS_REFERENCES = _FILEDATAJSON["odds_references"]
ANNOUNCEMENT_CHANNEL = int(_FILEDATAJSON["announcement_channel"])
SELL_PRICE = int(_FILEDATAJSON["sell_price"])
BADGE_VALUES = {}

PROFILE_STATS = {
    "level": "Level",
    "exp": "XP",
    "xp_needed": "XP to Next Level",
    "net_worth": "Net Worth",
    "equipped_pet": "Equipped Pet",
    # "favourite_card" : "Favourite Card",
    "equipped_badge": "Equipped Badge",
    "biggest_win": "Biggest Gambling Win",
}

LEVEL_DIVIDER = 2
LEVEL_CURVE = 2
LEVEL_BASE = 100
BADGE_TYPES = ["badges", "deluxe_badges"]


WALLET_STATS = {  # What should we call these stats?
    "coins": "Coins 🪙",
    "gems": "Gems 💎",
    "last_daily": "Last Daily",
    "badgeinvvalue": "Badges Value",
    "net_worth": "Net Worth",
}

DAILY_AMOUNT = 100

RARITY_KEYS = [
    "common",
    "uncommon",
    "rare",
    "epic",
    "legendary"
]



class BadgeRarity(Enum):
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"
    UNREAL = "Unreal"
    GODLY = "Godly"

RARITY_VALUES = {
    BadgeRarity.COMMON: 10,
    BadgeRarity.UNCOMMON: 25,
    BadgeRarity.RARE: 50,
    BadgeRarity.EPIC: 500,
    BadgeRarity.LEGENDARY: 3000,
    BadgeRarity.UNREAL:20000,
    BadgeRarity.GODLY:50000,

}

class Badge():
    def __init__(self, title, description, image, rarity, max_level = 30, sellable = True):
        self.title = title
        self.description = description
        self.image = image
        self.rarity = rarity
        self.max_level = max_level
        self.sellable = sellable

BADGE_DATA = {
    "scare_survivor": Badge(
        title="Scare Survivor Badge",
        description="Survive a super scary encounter. So so brave.",
        image="👻",
        rarity=BadgeRarity.RARE
    ),
    "high_roller":Badge(
        title="High Roller Badge",
        description="Roll a 1000! You really should hit Crown.",
        image="🎰",
        rarity=BadgeRarity.EPIC
    ),
    "consistent_6":Badge(
        title="Rookie Gambler Badge",
        description="Roll the same number three times in a row on a D6.",
        image="🎲",
        rarity=BadgeRarity.UNCOMMON,
        max_level=50
    ),
    "consistent_10":Badge(
        title="Novice Gambler Badge",
        description="Roll the same number three times in a row on a D10. Nice!",
        image="🎲",
        rarity=BadgeRarity.UNCOMMON,
        max_level=50
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
        rarity=BadgeRarity.UNCOMMON
    ),
    "victim":Badge(
        title="The Victim Badge",
        description="Get absolutely unfairly robbed.",
        image="🍺",
        rarity=BadgeRarity.COMMON
    ),
    "flip_5":Badge(
        title="Mini Flipper Badge",
        description="Flip the same face 5 times in a row! Nice job!",
        image="🪙",
        rarity=BadgeRarity.COMMON,
        max_level=50
    ),
    "flip_7":Badge(
        title="Medium Flipper Badge",
        description="Flip the same face 7 times in a row! Wow! Thats almost unbelievable",
        image="🪙",
        rarity=BadgeRarity.UNCOMMON,
        max_level=50
    ),
    "flip_10":Badge(
        title="Massive Flipper Badge",
        description="Flip the same face 10 times in a row! Are you cheating?",
        image="🪙",
        rarity=BadgeRarity.EPIC
    ),
    "flip_15":Badge(
        title="Elder Flipper Badge",
        description="Flip the same face 15 times in a row! Bro is wallhacking.",
        image="🪙",
        rarity=BadgeRarity.UNREAL
    ),
    "flip_25":Badge(
        title="Statistical Anomaly Badge",
        description="Flip the same face 25 times IN A ROW. Are we fucking for real.",
        image="🪙",
        rarity=BadgeRarity.GODLY
    ),
    "yapper":Badge(
        title="Yapper Badge",
        description="Send 1000 messages, holy fucking yap.",
        image="🗣️",
        rarity=BadgeRarity.EPIC,
    ),
    "deluxe_badge":Badge(
        title="Badge Hunter DX",
        description="Acquire a deluxe badge!",
        image="🥇",
        rarity=BadgeRarity.EPIC,
    ),
    "deluxe_badge_dx":Badge(
        title="Deluxe Badge Hunter DX",
        description="Acquire a 10 deluxe badges!",
        image="🎖️",
        rarity=BadgeRarity.UNREAL,
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
        rarity=BadgeRarity.COMMON,
        max_level=100,
        ),
    "maga" : Badge(
        title="MAGA Badge",
        description="You really shouldn't have this one, supporter of the orange man.",
        image="🍊",
        rarity=BadgeRarity.UNCOMMON,
        max_level=100,
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
        ),
    "perfect_alpha_shiny_hunter" : Badge(
            title="Alpha Shiny Hunter Badge",
            description="What. The. Fuck.",
            image="🪽",
            rarity=BadgeRarity.GODLY
            ),
    "jasper" : Badge(
        title="Jasper Badge",
        description="You've been Jaspered",
        image="👨",
        rarity=BadgeRarity.RARE   
        ),
    "jackpot" : Badge(
        title ="Jackpot Hitter Badge",
        description ="You're very lucky",
        image ="🎰",
        rarity=BadgeRarity.UNCOMMON
        ),
    "even" : Badge(
        title = "Even Stevens Badge",
        description= "You gambled and made net zero, impressive",
        image = "⚖️",
        rarity =BadgeRarity.COMMON
    ),   
}   
