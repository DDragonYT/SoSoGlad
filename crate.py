from random import randint

test = {
    "uncommon":{"chance":80, "options":[
        "dog",
        "cat",
        "fish",
        "bird",
        "monkey",
        "mouse",
        "pig"
    ]},
    "rare":{"chance":16,"options":[
        "gorilla",
        "tiger",
        "horse",
    ]},
    "epic":{"chance":3,"options":[
        "orangutan",
        "lion",
        "whale",
    ]},
    "legendary":{"chance":0.9,"options":[
        "shark",
        "moose",
        "zebra"
    ]},
    "mythic":{"chance":0.09,"options":[
        "pheonix",
        "dragon",
        "t-rex"
    ]},
    "godly":{"chance":0.01,"options":[
        "unicorn"
    ]}
}

luck_multiplier = 2

def apply_luck_mult(crate):
    total_chance = 0
    for rarity in crate.keys():
        if rarity != "uncommon":
            crate[rarity]["chance"] = crate[rarity]["chance"] * 2
            total_chance += crate[rarity]["chance"]
    crate["uncommon"]["chance"] = 100 - total_chance
    return crate
    


def open_crate(crate):
    if luck_multiplier != 0:
        mod_crate = apply_luck_mult(crate)
    print(mod_crate)


    roll = randint(1,10000) / 100

    totalraritychance = 0

    print(f"{roll=}")
    for rarity in mod_crate.keys():
        craterarity = mod_crate[rarity]
        totalraritychance += craterarity["chance"]
        
        print(f"{totalraritychance=}")

        if roll < totalraritychance:
            print(f"{rarity=}")
            break

open_crate(test)