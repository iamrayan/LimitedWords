import json
import random

characters = ["ABCDEFGHIJKLNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz", "0123456789"]
ids = []


def register_id():
    id = ""

    while True:
        for _ in range(10):
            character_group = random.choice(characters)
            character = random.choice(character_group)

            id += character
        
        if id in ids:
            id = ""
            continue
        else:
            break
        
    
    before_registeredids = open("registerid/registeredids.json", "r")
    before = json.load(before_registeredids)
    print(before)
    before_registeredids.close()
    
    before[id] = "id"

    with open("registerid/registeredids.json", "w") as registered_ids:
        json.dump(before, registered_ids)

    ids.append(id)

    return id


def delete_id(id: str):
    if id not in ids:
        return

    before_registeredids = open("registerid/registeredids.json", "r")
    before = json.load(before_registeredids)
    before_registeredids.close()

    before.pop(id)

    with open("registerid/registeredids.json", "w") as registered_ids:
        json.dump(before, registered_ids)

    ids.remove(id)