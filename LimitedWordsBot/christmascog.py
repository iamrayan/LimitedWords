import discord
from discord import ui
from discord.ext import commands
from random import choice


class ChristmasCog(commands.Cog):
    def __init__(self):
        pass

    
    @commands.command()
    async def chrismastime(self):
        color = choice([discord.Colour.red, discord.Colour.green])

        embed = discord.Embed("**Ho, Ho, Ho...**  ", color=color)
        embed.description = "*To celebrate Christmas, we will be\noffering a great opportunity for anyone\nto receive any wish from the list below*"
        embed.set_footer(text="🎅 This is a limited time offer 🎅")


class ChristmasView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    
    @ui.button(label="Get the christmas role")
    async def christmas_role(self):
        pass