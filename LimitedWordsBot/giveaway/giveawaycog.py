import time
from discord import ButtonStyle, PartialEmoji, Interaction
from discord.ui import Button, View
from discord.ext import commands
from .giveawayembed import GiveAwayEmbed
from registerid.getid import *
from .giveawayview import GiveAwayView


class GiveAwayCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    

    @commands.command()
    async def giveaway(self, ctx: commands.Context, minutes: float, reward_words):
        if ctx.author != ctx.guild.owner:
            await ctx.reply("This command is only available for {}".format(ctx.guild.owner.name), delete_after=5)
            return
        
        seconds = minutes * 60

        if seconds < 86400:
            readable_time = time.strftime("%H:%M:%S", time.gmtime(minutes*60))
        else:
            readable_time = time.strftime("%d days %H:%M:%S", time.gmtime(minutes*60))
        
        id = register_id()
        view = GiveAwayView(id)
        giveaway = GiveAwayEmbed(view, self.bot, reward_words, readable_time, minutes*60)

        message = await ctx.send(content="<@&1041653671357849650>", embed=giveaway, view=view)
        await giveaway.start(id, message)