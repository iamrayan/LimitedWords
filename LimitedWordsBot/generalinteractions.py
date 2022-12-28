from random import choice, randint
import time
import discord
from termcolor import colored
from LimitedWordsBot.database.functions import daily_ready, get_user_words, give_user_words, redeem_daily, user_monkerate, my_base
from LimitedWordsBot.monkeembed import MonkeEmbed

cooldowns = []
def colors():
    return choice([discord.Colour.red(), discord.Colour.green()])

def add_general_commands(bot):
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
                "Monke decided to be nice for once and gave you double words",
                "Monke repaid you double words for buying him candy",
                "Both of you decided to make a rap battle and you won. He gave you double amount the words"
            ]

            return_amount = words_converted + int((user_monkerate(interaction.user) / 100) * words_converted)
            await interaction.response.send_message(embed=MonkeEmbed(choice(decisions), words_converted, return_amount))

            total_words = await give_user_words(interaction.user, return_amount)

            await interaction.user.edit(nick="["+str(total_words)+"] "+interaction.user.name)
            
        cooldowns[str(interaction.user.id)] = time.time()+60

        print(colored("Command: ", "blue") + colored("Monke command called!", "green"))

    @bot.tree.command(name="monkerate", description="Your monke rate")
    async def monkeratecom(interaction: discord.Interaction):
        if interaction.user in my_base.prisoners.keys(): return
        if interaction.user == interaction.guild.owner: return

        await interaction.response.send_message(f"Your monke rate: `{user_monkerate(interaction.user)}%`")

        print(colored("Command: ", "blue") + colored("Monke Rate command called!", "green"))
