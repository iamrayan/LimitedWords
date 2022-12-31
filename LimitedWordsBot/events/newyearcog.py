import discord
from discord import ui
from discord.ext import commands
from database.functions import *
from termcolor import colored
import asyncio


class NewYearCog(commands.Cog):
    @commands.is_owner()
    @commands.command()
    async def newyeartime(self, ctx: commands.Context, time):
        view = NewYearView(time)

        message = await ctx.send("**Happy New Year!**", view)

        view.add_message(message)
        await view.end()


class NewYearView(ui.View):
    def __init__(self, sleeptime):
        super().__init__(timeout=None)
        self.sleeptime = sleeptime
        self.wishers = []
    
    @ui.button(label="1000 words", style=discord.ButtonStyle.success)
    async def wordwish(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user in self.wishers:
            await interaction.response.send_message("You have already made your wish!", ephemeral=True)
            return
        if is_prisoner(interaction.user):
            delay_word(interaction.user, 1000)

            self.wishers.append(interaction.user)

            await interaction.response.send_message("Claimed Successfully!\n1000 words have been delayed till you are out of prison!")
        else:
            words = await give_user_words(interaction.user, 1000)

            self.wishers.append(interaction.user)

            await interaction.user.edit(nick="["+str(words)+"] "+interaction.user.name)

            await interaction.response.send_message("Claimed Successfully!\n1000 words have been added to your balance!")

        print(colored("New Year: ", "blue") + colored("1000 words wish made!", "green"))
    
    def add_message(self, message: discord.Message):
        self.message = message

    async def end(self):
        await asyncio.sleep(self.sleep_time)
        
        disabled_view = NewYearView(self.sleeptime)

        for i in disabled_view.children:
            i.disabled = True

        await self.message.edit(view=disabled_view)