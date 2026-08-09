from PIL import Image
import os
import json

CARD_IMAGE = "resources/images/cards"


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
            for card in set:
                card_name = card.split(".")[0]
                rarity = input("what is the cards rarity? (1 = common, 2 = uncommon, 3 = rare, 4 = mythic)")
                card_json[set][card_name]
            


 


# new_im = display_binder("2ED")
# new_im.show()

get_card_image("Zombie Master","2ED").show()