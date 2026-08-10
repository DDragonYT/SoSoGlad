from PIL import Image
import os
import json
import scrython

CARD_IMAGE = "resources/images/cards"
RARITIES = ["common","uncommon","rare","mythic"]

def display_binder(set_name):
    cards = os.listdir(f"{CARD_IMAGE}/{set_name}/")
    print(cards)

    columns = 20
    rows = int(len(cards) / columns)

    card = cards[(0)]
    new_im = Image.open(f"{CARD_IMAGE}/{set_name}/{card}")
    im_w = new_im.width
    im_h = new_im.height
    full_height = im_h * rows
    full_width = im_w * columns

    new_im = Image.new("RGB", (full_width, full_height))
    c = 0
    for i in range(0, columns):
        for j in range(0, rows):

            card = cards[c]
            c += 1
            im = Image.open(f"{CARD_IMAGE}/{set_name}/{card}")
            new_im.paste(im, (i * im_w, j * im_h))

    return new_im

def get_card_image(cardname, set_name):
    new_im = Image.open(f"{CARD_IMAGE}/{set_name}/{cardname}.full.jpg")
    return new_im

def get_card_list():
    sets = os.listdir(f"{CARD_IMAGE}/")
    if os.path.isfile("cards.json"):
        with open("cards.json", "r") as cards:
            card_json = json.load(cards)
    else:
        card_json = {}
    for set in sets:
        
        if not set in card_json.keys():
            card_json[set] = {}
            for rarity in RARITIES:
                card_json[set][rarity] = []
            for card in os.listdir(f"{CARD_IMAGE}/{set}/"):
                try:
                    card_name = card.split(".")[0]
                    cardinfo = scrython.cards.Named(fuzzy=card_name)
                    card_json[set][card_name] = {
                        "rarity":cardinfo.rarity,
                        "color_identity":cardinfo.color_identity,
                        "mana_cost":cardinfo.mana_cost,
                        "artist":cardinfo.artist,
                        "type_line":cardinfo.type_line,
                        "oracle_text":cardinfo.oracle_text,
                        }
                    print(f"Retrieved [{card}] data.")
                    card_rarity = input(f"What rarity should {card} be? Press enter to just use {cardinfo.rarity}: ")
                    if not card_rarity:
                        card_rarity = cardinfo.rarity
                    card_json[set][card_rarity].append(card)

                except:
                    print(f"Could not retrieve [{card}] data.")
    with open("cards.json", "w") as f:
        json.dump(card_json, f)
            


 


# new_im = display_binder("2ED")
# new_im.show()


# get_card_list()
# get_card_image("Black Lotus","2ED").show()