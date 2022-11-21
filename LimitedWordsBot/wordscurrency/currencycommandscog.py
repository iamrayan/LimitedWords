from discord import Embed, Colour
from discord.ext import commands
from database.functions import *


class CurrencyCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def daily(self, ctx: commands.Context):
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