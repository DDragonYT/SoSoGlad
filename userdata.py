import json

def get_userdata(user):
    try:
        with open(f"users/{user}.json", "rb") as userjson:
            return json.load(userjson)
    except:
        return {}

def set_userdata(user, userdata):
    with open(f"users/{user}.json", "w+") as userjson:
        json.dump(userdata, userjson, indent=2)