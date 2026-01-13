from enum import Enum

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