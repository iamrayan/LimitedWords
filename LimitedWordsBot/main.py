import discord
from discord.ext import commands
import random
from database.functions import *
import math
from autorolecog import AutoRoleCog
from giveaway.giveawaycog import GiveAwayCog
from admincog import AdminCog
from termcolor import colored
from random import randint
from pets.petinteraction import attach_commands
from events.christmascog import ChristmasCog
from events.newyearcog import NewYearCog
from moderationcog import ModerationCog
from generalinteractions import add_general_commands
from wordpopup import WordPopUp


cooldowns = {}

bot = commands.Bot("!", intents=discord.Intents.all(), case_insensitive=True, help_command=None)

help_commands = {
    "help": "`Shows this commands`",
    "daily": "`You can run this command once in 24 hours. If you don't do it within 48 hours, your current streak will be gone`",
    "monke (words)": "`Gamble up some words to see if monke gives you double the words or none`"
}

basic_roles = [1054323884490493962, 1054324109972086804, 1054324225843937290, 1054324297495232582]

prison_chat_id = 1046101755999563887


@bot.event
async def on_ready():
    await update_words(bot.get_guild(1039438917105102848), bot)
    
    invites = await bot.get_guild(1039438917105102848).invites()

    for invite in invites:
        my_base.links[invite.code] = invite

    await bot.add_cog(AutoRoleCog(bot))
    await bot.add_cog(GiveAwayCog(bot))
    await bot.add_cog(AdminCog(bot))
    await bot.add_cog(ModerationCog(bot))
    await bot.add_cog(ChristmasCog())
    await bot.add_cog(NewYearCog())
    await bot.add_cog(WordPopUp(bot))
    attach_commands(bot)
    add_general_commands(bot)
    await bot.tree.sync()

    print(colored("System: ", "blue") + colored("Bot is Online!", "green"))


@bot.tree.command(name="daily", description="Claim your daily!")
async def daily(interaction: discord.Interaction):
    if interaction.user in my_base.prisoners.keys(): return

    ready = daily_ready(interaction.user)

    embed = discord.Embed(title="{}'s daily".format(interaction.user.name), colour=colors())

    if not ready:
        embed.description = "You have already claimed your daily!"
        embed.set_footer(text="Come back soon for your daily")
    else:
        reward = 50 + ready["streak"] * 20

        embed.description = "Your daily has been redeemed!"
        embed.add_field(name="Reward", value=str(reward))
        embed.add_field(name="Streak", value=ready["streak"])
        embed.set_footer(text="You can redeem again in 24 hours!")

        total_words = await give_user_words(interaction.user, reward)

        await interaction.user.edit(nick="["+str(total_words)+"] "+interaction.user.name)

        redeem_daily(interaction.user)
        

    await interaction.response.send_message(embed=embed)

    print(colored("Command: ", "blue") + colored("Daily command called!", "green"))


@bot.tree.command(name="monke", description="Gamble away your coins!")
async def monke(interaction: discord.Interaction, words: int):
    if interaction.user in my_base.prisoners.keys(): return

    cooldown_user = cooldowns.get(str(interaction.user.id))
    if cooldown_user != None:
        if cooldown_user - time.time() < 0:
            cooldowns.pop(str(interaction.user.id))
        else:
            await interaction.response.send_message("You need to wait {} more seconds to use this command".format(int(cooldown_user - time.time())))
            return
        
    if words > 100:
        await interaction.response.send_message("The max bet limited is 100")
        return

    if int(words) > get_user_words(interaction.user):
        await interaction.response.send_message("You dont have enough words")
        return

    words_converted = None
    try:
        words_converted = int(words)
    except:
        await interaction.response.send_message("Word amount should be a number")
        return
        
    chance = randint(1, 100)

    if chance <= 65:
        decisions = [
            "Monke wanted a vacation so badly that he took your words",
            "Monke sent his kids but that naught little monke's decided to steal it",
            "Monke was too cute that you accidently tripped and sent your word's flying off to monke's pocket",
            "You decide to steal his words but you failed and monke stole your words"
        ]

        await interaction.response.send_message(embed=MonkeEmbed(choice(decisions), words_converted, 0))

        total_words = await give_user_words(interaction.user, words_converted * (-1))

        await interaction.user.edit(nick="["+str(total_words)+"] "+interaction.user.name)
    else:
        decisions = [
            "Monke decided to be nice for once and gave words",
            "Monke repaid for buying him candy",
            "Both of you decided to make a rap battle and you won"
        ]

        return_amount = words_converted + int((user_monkerate(interaction.user) / 100) * words_converted)
        await interaction.response.send_message(embed=MonkeEmbed(choice(decisions), words_converted, return_amount))

        total_words = await give_user_words(interaction.user, return_amount)

        await interaction.user.edit(nick="["+str(total_words)+"] "+interaction.user.name)
        
    cooldowns[str(interaction.user.id)] = time.time()+60

    print(colored("Command: ", "blue") + colored("Monke command called!", "green"))


@bot.tree.command(name="help", description="List of all the commands")
async def help(interaction: discord.Interaction):
    if interaction.user in my_base.prisoners.keys(): return

    help_embed = discord.Embed(title="List of Commands", colour=colors())
    help_embed.description = "Here are the list of available commands in this bot"

    for com, des in help_commands.items():
        help_embed.add_field(name=com, value=des, inline=False)

    await interaction.response.send_message(embed=help_embed)

    print(colored("Command: ", "blue") + colored("Help command called!", "green"))

@bot.tree.command(name="monkerate", description="Your monke rate")
async def monkeratecom(interaction: discord.Interaction):
    if interaction.user in my_base.prisoners.keys(): return
    if interaction.user == interaction.guild.owner: return

    await interaction.response.send_message(f"Your monke rate: `{user_monkerate(interaction.user)}%`")

    print(colored("Command: ", "blue") + colored("Monke Rate command called!", "green"))


>>>>>>> main
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
        await member.add_roles(member.guild.get_role(1042735438621855774))
        await member.edit(nick="[inf] "+member.name)
        return

    member_is_prisoner = is_prisoner(member)

    for role_id in basic_roles:
            await member.add_roles(member.guild.get_role(role_id))

    if not member_is_prisoner:
        await member.add_roles(member.guild.get_role(1039442856177307658))
    else:
        await member.add_roles(member.guild.get_role(1046101250468487168))

    invites = await member.guild.invites()
    
    inviter = get_inviter(invites, member.guild)
    
    message = ""
    exists = my_base.exists(member)
    welcome_channel = bot.get_channel(1039442754926805043)

    new_member_words = random.randint(50, 150)

    if exists and member_is_prisoner:
        message += f"**Welcome our member *<@{member.id}>!***\n\n- You have been detected as prisoner, you will be send straigt to prison"
    elif exists:
        message += f"**Welcome our member *<@{member.id}>!***\n\n- Since you have already began, you will be continuing with your latest word amount\n\n"
    else:
        await give_user_words(member, new_member_words)
        message += f"**Welcome our newest member *<@{member.id}>!***\n\n"
        message += f"- To begin you are given *{new_member_words}* words\n"

    if inviter == False:
        message += "- Sadly, the inviter could not be found\n\n"
    if inviter is not None and not exists:
        if inviter == member.guild.owner:
            message += f"- The inviter, *<@{inviter.id}>* has also received *inf* words.\n\n"
        elif is_prisoner(inviter):
            delay_word(inviter, inviter_words)

            message += f"- The inviter, *<@{inviter.id}>* is currently in prison, so *{inviter_words}* words have been delayed"
        else:
            inviter_words = math.ceil(new_member_words / 2)
            boost_avail = inviteboost_avail(inviter)
            if boost_avail != 0 or boost_avail is not None:
                inviter_words += boost_avail

            words_given = await give_user_words(inviter, inviter_words)
            await inviter.edit(nick="["+str(words_given)+"] "+inviter.name)

            message += f"- The inviter, *<@{inviter.id}>* has also received *{inviter_words}* words\n\n"
    

    if not member_is_prisoner:
        await member.edit(nick=f"[{str(get_user_words(member))}] {member.name}")
    else:
        await member.edit(nick=f"[prison] {member.name}")

    message += "*Make sure you enjoy!*"
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
        await before.author.edit(nick=f"[jail] {before.author.name}")
        await before.author.add_roles(before.guild.get_role(1046101250468487168))

        return

    if words_left < 0:
        await after.delete()
        await before.channel.send("You cannot edit/send words more than you have", delete_after=5)
        return

    await before.author.edit(nick="["+str(words_left)+"] "+before.author.name)
    decrease_user_words_to(before.author, words_left)

    print(colored("Dizzy: ", "blue") + colored("Message edited!", "green"))
    

@bot.listen("on_message")
async def word_check(ctx: discord.Message):
    if ctx.author in my_base.prisoners.keys(): return
    if ctx.channel.id == 1057596783078944850 and ctx.type == discord.MessageType.premium_guild_subscription:
        reward_words = randint(750, 1000)

        if is_prisoner(ctx.author):
            delay_word(ctx.author, reward_words)

            await ctx.channel.send(f"**<@{ctx.author.id}> has boosted our server!**\nReward: {reward_words}!\n*Since he is in prison, his words will be delayed*")
        else:
            words = await give_user_words(ctx.author, reward_words)
            await ctx.author.edit(nick=f"[{words}] {ctx.author.name}")

            await ctx.channel.send(f"**<@{ctx.author.id}> has boosted our server!**\nReward: {reward_words}!")
        
        return
        
    if ctx.channel.id == 1053640012924731442:
        await ctx.add_reaction("✅")
        await ctx.add_reaction("❌")
    if ctx.author.bot or ctx.author.id == ctx.guild.owner.id or ctx.channel.id == prison_chat_id: 
        return

    words = get_user_words(ctx.author)

    used_words = len(ctx.clean_content.split(" "))

    words = int(words) - used_words 

    if words == 0:
        await ctx.delete()
        await add_prisoner(ctx.author, "out of words", time=time.time()+86400)
        await ctx.author.edit(nick=f"[prison] {ctx.author.name}")
        await ctx.author.add_roles(ctx.guild.get_role(1046101250468487168))
        
        return

    if words < 0:
        await ctx.delete()
        await ctx.channel.send("You cannot send words more than you have", delete_after=5)
        return

    decrease_user_words_to(ctx.author, words)

    await ctx.author.edit(nick="["+str(words)+"] "+ctx.author.name)

    print(colored("Dizzy: ", "blue") + colored("New message sent!", "green"))


bot.run("MTAzOTQ2OTYwMTUzODQ0MTIyNg.Gz99BS.1mafLZub4gOKYoe675iYeIIltjaJvx9t8z7P4E")
