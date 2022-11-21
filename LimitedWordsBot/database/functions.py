from . import base
import discord
from discord.ext import commands
from random import randint
import time


my_base = base.Base()


async def create_data(user: discord.Member, words: int):
    data = {
        'id': user.id,
        'words': words,
        'latest daily': int(time.time() - 86401),
        'streak': 0
    }

    my_base.data[str(user.name)] = data

    my_base.db.collection('users').document(user.name).set(data)

    await user.edit(nick="["+str(words)+"] "+user.name)


async def update_words(guild: discord.Guild, bot: commands.Bot):
    for user in guild.members:
        if user != guild.owner and not user.bot:
            nick = user.nick

            if nick is None:
                await create_data(user, randint(10, 50))
            
            words = int(user.nick.split("]")[0].split("[")[1])

            my_base.data[str(user.name)] = {
                'id': user.id,
                'words': words,
                'latest daily': int(time.time() - 86401),
                'streak': 0
            }


async def give_user_words(user: discord.Member, words: int):
    if my_base.exists(user):
        user_words = my_base.data[str(user.name)]["words"]

        total_words = int(user_words) + int(words)

        my_base.data[str(user.name)]["words"] = total_words
        return total_words
    else:
        await create_data(user, words)

        return words


async def decrease_user_words_to(user: discord.Member, words: int):
    my_base.data[str(user.name)]["words"] = words


async def get_inviter(invites: list[discord.Invite], guild: discord.Guild):
    for invite in invites:
        invite_link = my_base.links.get(invite.code)

        if invite_link is not None and invite_link.uses != invite.uses:
            inviter = invite_link.inviter
            return guild.get_member(inviter.id)

    return False


async def daily_ready(user: discord.User):
    latest_daily = my_base.data[user.name]['latest daily']

    current_time = int(time.time())

    if (current_time - latest_daily) >= 86400:
        return my_base.data[user.name]
    return False


async def redeem_daily(user: discord.User):
    my_base.data[user.name]["latest daily"] = int(time.time())
    my_base.data[user.name]["streak"] += 1