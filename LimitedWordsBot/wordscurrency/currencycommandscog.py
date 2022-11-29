from discord import Embed, Colour
from discord.ext import commands
from database.functions import *
from .monkeembed import MonkeEmbed
from random import randint, choice
import time


class CurrencyCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.cooldowns = {}
    
    @commands.command()
    async def daily(self, ctx: commands.Context):
        if ctx.author in my_base.prisoners.keys(): return

        ready = await daily_ready(ctx.author)

        embed = Embed(title="{}'s daily".format(ctx.author.name), colour=Colour.green())

        if not ready:
            embed.description = "You have already claimed your daily!"
            embed.set_footer(text="Come back soon for your daily")
        else:
            reward = 50 + ready["streak"] * 20

            embed.description = "Your daily has been redeemed!"
            embed.add_field(name="Reward", value=str(reward))
            embed.add_field(name="Streak", value=ready["streak"])
            embed.set_footer(text="You can redeem again in 24 hours!")

            total_words = await give_user_words(ctx.author, reward)

            await ctx.author.edit(nick="["+str(total_words)+"] "+ctx.author.name)

            await redeem_daily(ctx.author)
        

        await ctx.send(embed=embed)
    

    @commands.command()
    async def monke(self, ctx: commands.Context, words):
        if ctx.author in my_base.prisoners.keys(): return

        cooldown_user = self.cooldowns.get(str(ctx.author.id))
        if cooldown_user != None:
            if cooldown_user - time.time() < 0:
                self.cooldowns.pop(str(ctx.author.id))
            else:
                await ctx.reply("You need to wait {} more seconds to use this command".format(int(cooldown_user - time.time())))
                return
        
        if words > 100:
            await ctx.reply("The max bet limited is 100")
            return

        if len(ctx.message.clean_content.split(" ")) + int(words) > await get_user_words(ctx.author):
            await ctx.reply("You dont have enough words")
            return

        words_converted = None
        try:
            words_converted = int(words)
        except:
            await ctx.reply("Word amount should be a number")
            return
        
        chance = randint(0, 100)

        if chance <= 65:
            decisions = [
                "Monke wanted a vacation so badly that he took your words",
                "Monke sent his kids but that naught little monke's decided to steal it",
                "Monke was too cute that you accidently tripped and sent your word's flying off to monke's pocket",
                "You decide to steal his words but you failed and monke stole your words"
            ]

            await ctx.send(embed=MonkeEmbed(choice(decisions), words_converted, 0))

            total_words = await give_user_words(ctx.author, words_converted * (-1))

            await ctx.author.edit(nick="["+str(total_words)+"] "+ctx.author.name)
        else:
            decisions = [
                "Monke decided to be nice for once and gave you double words",
                "Monke repaid you double words for buying him candy",
                "Both of you decided to make a rap battle and you won. He gave you double amount the words"
            ]

            await ctx.send(embed=MonkeEmbed(choice(decisions), words_converted, words_converted * 2))

            total_words = await give_user_words(ctx.author, words_converted*2)

            await ctx.author.edit(nick="["+str(total_words)+"] "+ctx.author.name)
        
        self.cooldowns[str(ctx.author.id)] = time.time()+60