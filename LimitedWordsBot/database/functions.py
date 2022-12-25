from . import base
import discord
from discord.ext import commands
import time
from pets.snowman import Snowman
from pets.petutilities import PetAbilities, PetPerks


my_base = base.Base()


async def create_data(user: discord.Member, words: int):
    data = {
        'words': words,
        'latestdaily': int(time.time() - 86401),
        'warnings': 0,
        'streak': 0,
        'wish': False,
        'monkerate': 50,
        'selectedpet': "",
        'inviteboost': 0,
        'lastpetactive': int(time.time() - 3600),
        'pets': [],
        'prisoner': False,
        'delayed': 0,
        'warn': 0
    }

    my_base.data[str(user.id)] = data

    my_base.db.collection('users').document(str(user.id)).set(data)

    await user.edit(nick="["+str(words)+"] "+user.name)


async def update_words(guild: discord.Guild, bot: commands.Bot):
    for member in guild.members:
        if member != guild.owner and not member.bot:
            user_data = my_base.db.collection('users').document(str(member.id)).get()
            
            dicted = user_data.to_dict()
            my_base.data[str(member.id)] = dicted

            if not my_base.data[str(member.id)]["prisoner"]:
                await member.edit(nick="["+str(dicted["words"])+"] "+member.name)
            else:
                dicted = my_base.db.collection('prisoners').document(str(member.id)).get().to_dict()

                my_base.prisoners[member] = dicted

async def give_user_words(user: discord.Member, words: int):
    if my_base.exists(user):
        if user == user.guild.owner: return
        
        user_words = my_base.data[str(user.id)]["words"]

        total_words = int(user_words) + int(words)

        my_base.data[str(user.id)]["words"] = total_words
        return total_words
    else:
        await create_data(user, words)

        return words


def decrease_user_words_to(user: discord.Member, words: int):
    my_base.data[str(user.id)]["words"] = words


def get_user_words(user: discord.User):
    return my_base.data[str(user.id)]["words"]


def get_inviter(invites, guild):
    for invite in invites:
        invite_link = my_base.links.get(invite.code)

        if invite_link is not None and invite_link.uses != invite.uses:
            inviter = invite_link.inviter
            return guild.get_member(inviter.id)

    return False


def daily_ready(user: discord.User):
    latest_daily = my_base.data[str(user.id)]['latestdaily']

    current_time = int(time.time())

    if current_time - latest_daily >= 172800:
        my_base.data[str(user.id)]["streak"] = 0
        return my_base.data[str(user.id)]
    
    if current_time - latest_daily >= 86400:
        return my_base.data[str(user.id)]
        
    return False


def redeem_daily(user: discord.Member):
    my_base.data[str(user.id)]["latestdaily"] = int(time.time())
    my_base.data[str(user.id)]["streak"] += 1


def add_prisoner(user: discord.Member, reason: str, time: int):
    my_base.prisoners[user] = {
        "reason": reason,
        "time": time
    }


def is_prisoner(user: discord.Member):
    if my_base.prisoners.get(user) != None:
        return True
    return False


def add_monkerate(user: discord.Member, amount: int):
    my_base.data[str(user.id)]["monkerate"] = my_base.data[str(user.id)]["monkerate"] + amount
    return my_base.data[str(user.id)]["monkerate"]


def pet_exists(user: discord.Member):
    return len(my_base.data[str(user.id)]["pets"]) > 0


def user_pets(user: discord.Member):
    pets = []

    for pet in my_base.data[str(user.id)]["pets"]:
        if pet["name"] == "Snowman":
            abilities = PetAbilities(pet["speed"], pet["agility"], pet["strength"])
            perks = PetPerks(pet["monkerate"], pet["inviteboost"])
            pets.append(Snowman(abilities, perks, pet["mood"]))
    
    return pets


def get_pet(user: discord.Member, pet: str):
    for _pet in my_base.data[str(user.id)]["pets"]:
        if _pet["name"] == pet:
            abilities = PetAbilities(_pet["speed"], _pet["agility"], _pet["strength"])
            perks = PetPerks(_pet["monkerate"], _pet["inviteboost"])
            return Snowman(abilities, perks, _pet["mood"])


def pet_selected(user: discord.Member):
    if my_base.data[str(user.id)]["selectedpet"] == "":
        return None
    return get_pet(user, my_base.data[str(user.id)]["selectedpet"])


def add_pet(user: discord.Member, pet):
    my_base.data[str(user.id)]["pets"].append({
        "agility": pet.abilities.agility,
        "inviteboost": pet.perks.invite_boost,
        "monkerate": pet.perks.monkerate,
        "mood": pet.mood,
        "name": str(pet),
        "speed": pet.abilities.speed,
        "strength": pet.abilities.strength
    })

    if my_base.data[str(user.id)]["selectedpet"] == "":
        my_base.data[str(user.id)]["selectedpet"] = str(pet)


def update_pet(user: discord.Member, pet):
    for _pet in my_base.data[str(user.id)]["pets"]:
        if _pet["name"] == str(pet):
            _pet["agility"] = pet.abilities.agility
            _pet["inviteboost"] = pet.perks.invite_boost
            _pet["monkerate"] = pet.perks.monkerate
            _pet["mood"] = pet.mood
            _pet["speed"] = pet.abilities.speed
            _pet["strength"] = pet.abilities.strength
            return


def inviteboost_avail(user: discord.Member):
    for _pet in my_base.data[str(user.id)]["pets"]:
        if _pet["name"] == my_base.data[str(user.id)]["selectedpet"]:
            return _pet["inviteboost"]


def user_monkerate(user: discord.Member):
    monkerate = my_base.data[str(user.id)]["monkerate"]

    for _pet in my_base.data[str(user.id)]["pets"]:
        if _pet["name"] == my_base.data[str(user.id)]["selectedpet"]:
            return monkerate + _pet["monkerate"]
    
    return monkerate


def delay_word(user: discord.Member, words: int):
    my_base.data[str(user.id)]["delayed"] = my_base.data[str(user.id)]["delayed"] + words


def warn_user(user: discord.Member):
    my_base.data[str(user.id)]["warn"] = my_base.data[str(user.id)]["warn"] + 1
    return my_base.data[str(user.id)]["warn"]