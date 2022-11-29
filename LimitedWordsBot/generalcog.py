import discord
from discord.ext import commands
from database.functions import *


class GeneralCog(commands.Cog):
    def __init__(self, bot: commands.Bot, help_commands):
        self.bot = bot
        self.help_commands = help_commands


    @commands.command()
    async def help(self, ctx: commands.Context):
        if ctx.author in my_base.prisoners.keys(): return

        help_embed = discord.Embed(title="List of Commands", colour=discord.Colour.random())
        help_embed.description = "Here are the list of available commands in this bot"

        for com, des in self.help_commands.items():
            help_embed.add_field(name=com, value=des, inline=False)

        await ctx.send(embed=help_embed)