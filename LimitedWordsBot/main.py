import discord
from discord.ext import commands
import random
from database.functions import *
import math
from autorolecog import AutoRoleCog
from giveaway.giveawaycog import GiveAwayCog
from wordscurrency.currencycommandscog import CurrencyCommandsCog
from admincog import AdminCog
from generalcog import GeneralCog
from termcolor import colored

print("atleast work")

bot = commands.Bot("!", intents=discord.Intents.all(), case_insensitive=True, help_command=None)

help_commands = {
    "prefix": "`!`",
    "help": "`Shows this commands`",
    "daily": "`You can run this command once in 24 hours. If you don't do it within 48 hours, your current streak will be gone`",
    "monke (words)": "`Gamble up some words to see if monke gives you double the words or none`"
}

prison_chat_id = 1046101755999563887


@bot.event
async def on_ready():
    await update_words(bot.get_guild(1039438917105102848), bot)
    
    invites = await bot.get_guild(1039438917105102848).invites()

    for invite in invites:
        my_base.links[invite.code] = invite

    await bot.add_cog(AutoRoleCog(bot))
    await bot.add_cog(GiveAwayCog(bot))
    await bot.add_cog(CurrencyCommandsCog(bot))
    await bot.add_cog(AdminCog(bot))
    await bot.add_cog(GeneralCog(bot, help_commands))

    print(colored("System: ", "blue") + colored("Bot is Online!", "green"))


@bot.event
async def on_invite_create(invite: discord.Invite):
    my_base.links[invite.code] = invite
    print(colored("Dizzy: ", "blue") + colored("Invite link created!", "green"))


@bot.event
async def on_invite_delete(invite: discord.Invite):
    my_base.links.pop(invite.code)
    print(colored("Dizzy: ", "blue") + colored("Invite link deleted!", "green"))


@bot.event
async def on_member_join(member: discord.Member):
    if member.bot:
        await member.add_roles(1042735438621855774)
        await member.edit(nick="[inf] "+member.name)
        return

    await member.add_roles(member.guild.get_role(1039442856177307658))

    invites = await member.guild.invites()
    
    inviter = await get_inviter(invites, member.guild)
    
    message = ""
    exists = my_base.exists(member)
    welcome_channel = bot.get_channel(1039442754926805043)

    new_member_words = random.randint(50, 150)
    inviter_words = math.ceil(new_member_words / 2)

    if exists:
        message += "Welcome again to Limited Words <@{0}>!\n".format(member.id)
    else:
        await give_user_words(member, new_member_words)

        message += "Welcome to Limited Words <@{0}>! To begin, you are given {1} words!\n".format(member.id, new_member_words)
    
    if inviter == False:
        message += "The inviter could not be found"
    if inviter is not None and not exists:
        if inviter == member.guild.owner:
            message += "<@{0}>, the inviter, has also received inf words!".format(inviter.id)
        else:
            await give_user_words(inviter, inviter_words)
            await inviter.edit(nick="["+str(inviter_words)+"] "+inviter.name)

            message += "<@{0}>, the inviter, has also received {1} words!".format(inviter.id, inviter_words)
        
    await member.edit(nick="[{0}] {1}".format(str(new_member_words), member.name))
    await welcome_channel.send(message)

    print(colored("Dizzy: ", "blue") + colored("New Member joined!", "green"))


@bot.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if before.author in my_base.prisoners.keys(): return
    if before.author == before.guild.owner: return
    if before.author == bot.user: return

    used_words = len(after.clean_content.split(" "))
    user_words = my_base.data[str(before.author.id)]["words"]

    words_left = user_words - used_words

    if words_left == 0:
        await after.delete()
        await add_prisoner(before.author, "out of words", time=time.time()+86400)
        await before.author.edit(nick=f"[prisoner] {before.author.name}")

        return

    if words_left < 0:
        await after.delete()
        await before.channel.send("You cannot edit/send words more than you have", delete_after=5)
        return

    await before.author.edit(nick="["+str(words_left)+"] "+before.author.name)
    await decrease_user_words_to(before.author, words_left)

    print(colored("Dizzy: ", "blue") + colored("Message edited!", "green"))
    

@bot.listen("on_message")
async def word_check(ctx: discord.Message):
    if ctx.author in my_base.prisoners.keys(): return
    if ctx.author.bot or ctx.author.id == ctx.guild.owner.id or ctx.channel.id == prison_chat_id: 
        return

    words = await get_user_words(ctx.author)

    used_words = len(ctx.clean_content.split(" "))

    words = int(words) - used_words 

    if words == 0:
        await ctx.delete()
        await add_prisoner(ctx.author, "out of words", time=time.time()+86400)
        await ctx.author.edit(nick=f"[prisoner] {ctx.author.name}")

        return

    if words < 0:
        await ctx.delete()
        await ctx.channel.send("You cannot send words more than you have", delete_after=5)
        return

    await decrease_user_words_to(ctx.author, words)

    await ctx.author.edit(nick="["+str(words)+"] "+ctx.author.name)

    print(colored("Dizzy: ", "blue") + colored("New message sent!", "green"))


bot.run("MTAzOTQ2OTYwMTUzODQ0MTIyNg.Gzup3-.42vttlpEuxugGpZTXSpLtK8s92aFDy6fslPI-g")
