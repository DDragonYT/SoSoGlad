from random import randint

RARITY_KEYS = [
    "common",
    "uncommon",
    "rare",
    "epic",
    "legendary"
]

def apply_luck_mult(crate, luck_mult):
    if luck_mult != 0:
        total_chance = 0
        for rarity in crate.keys():
            if rarity in RARITY_KEYS:
                if rarity != "common":
                    crate[rarity]["chance"] = crate[rarity]["chance"] * luck_mult
                    total_chance += crate[rarity]["chance"]
            crate["common"]["chance"] = 100 - total_chance
        return crate
    else:
        return crate

def get_crate_result(cratesdict, crate, luck_multiplier=1):
    crate = cratesdict[crate].copy()
    mod_crate = apply_luck_mult(crate, luck_multiplier)
    print(mod_crate)
    roll = randint(1, 1000000) / 10000
    totalraritychance = 0

    print(f"{roll=}")
    for rarity in mod_crate.keys():
        if rarity in RARITY_KEYS:
            craterarity = mod_crate[rarity]
            totalraritychance += craterarity["chance"]
            if roll < totalraritychance:
                options = crate[rarity]["options"]
                rolled_item_data = options[randint(0, len(options) - 1)]
                try:
                    min_qty = rolled_item_data["min_qty"]
                    max_qty = rolled_item_data["max_qty"]

                    if max_qty != min_qty:
                        quantity = randint(min_qty, max_qty)
                    else:
                        quantity = max_qty
                    rolled_item = rolled_item_data["item"]
                except:
                    rolled_item = rolled_item_data
                    quantity = 1
                return (rolled_item, rarity, quantity)