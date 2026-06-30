from json import load
from embed import gen_error
from userdata import get_userdata

ITEM_ICONS = {  # Used to define what icon an item type should have
    "lolly": "🍭",
    "minion": "😈",
    "pet": "🐕",
    "booster": "🔋",
    "crate": "🎁",
    "equipment": "🗡️",
    "trinket": "📿",
    "currency": "💰",
    "resource":"🪵"
}


def get_itemdata(itemname=None):
    with open("items.json", "rb") as itemjson:
        if itemname:
            return load(itemjson)[itemname]
        else:
            return load(itemjson)
