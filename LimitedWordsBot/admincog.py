import discord
from discord.ext import commands
from database.functions import *
from termcolor import colored


class AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def Givewords(self, ctx: commands.Context, user: discord.Member, words: int):
        if ctx.author != ctx.guild.owner:
            await ctx.reply("This command is only available for {}".format(ctx.guild.owner.name), delete_after=5)
            return

        total_words = await give_user_words(user, words)

        await user.edit(nick="["+str(total_words)+"] "+user.name)

        await ctx.send("Words given to {0}: {1}".format(user.name, words))
        await ctx.send("Current words of {0}: {1}".format(user.name, total_words))

        print(colored("Admin: ", "blue") + colored("Givewords called!", "green"))
    

    @commands.command()
    async def updatedb(self, ctx: commands.Context):
        if ctx.author != ctx.guild.owner:
            await ctx.reply("This command is only available for {}".format(ctx.guild.owner.name), delete_after=5)
            return

        my_base.update_now()

        await ctx.reply("Database updated with current data.")

        print(colored("Admin: ", "blue") + colored("Database updated!", "green"))


    @commands.command()
    async def stopbot(self, ctx: commands.Context):
        if ctx.author != ctx.guild.owner:
            await ctx.reply("This command is only available for {}".format(ctx.guild.owner.name))
            return

        my_base.update_now()

        await ctx.reply("101 B0t s10pped 1010010")

        await self.bot.close()

        print(colored("System: ", "blue") + colored("Bot Stopped!", "green"))