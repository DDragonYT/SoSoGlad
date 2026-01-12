import json

# def add_badge(user, badge):
#     with open(f"users/{user}.json", "w+") as userdata:
#         print(json.load(userdata))

# add_badge("ddragonyt",0)
with open(f"users/ddragonyt.json", "r") as userdata:
    print(json.load(userdata))