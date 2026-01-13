import json
from badge import badgedata

def add_badge(user, badge):
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
    else:
        badges[badge] = {"lvl":1}

    with open(f"users/{user}.json", "w+") as userjson:
        json.dump(userdata, userjson, indent=2)

# add_badge("ddragonyt",0)
# userdata = json.load(open("users/ddragonyt.json","rb"))
# print(userdata)
