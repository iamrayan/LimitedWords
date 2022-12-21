from . import base
import discord
from discord.ext import commands
import time


my_base = base.Base()


async def create_data(user: discord.Member, words: int):
    data = {
        'words': words,
        'latestdaily': int(time.time() - 86401),
        'warnings': 0,
        'streak': 0,
        'wish': False,
        'monkerate': 50
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
                
            await member.edit(nick="["+str(dicted["words"])+"] "+member.name)


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


def redeem_daily(user: discord.User):
    my_base.data[str(user.id)]["latestdaily"] = int(time.time())
    my_base.data[str(user.id)]["streak"] += 1


def add_prisoner(user: discord.Member, reason: str, time: int):
    my_base.prisoners[user] = {
        "reason": reason,
        "time": time
    }


def add_monkerate(user: discord.Member, amount: int):
    my_base.data[str(user.id)]["monkerate"] = my_base.data[str(user.id)]["monkerate"] + amount
    return my_base.data[str(user.id)]["monkerate"]


def get_monkerate(user: discord.Member):
    return my_base.data[str(user.id)]["monkerate"]