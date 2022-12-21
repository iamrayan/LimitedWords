from discord.ext import commands
from .giveawayembed import GiveAwayEmbed
from .giveawayview import GiveAwayView
from termcolor import colored


class GiveAwayCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    

    @commands.command()
    async def giveaway(self, ctx: commands.Context, minutes: float, reward_words):
        if ctx.author != ctx.guild.owner:
            await ctx.reply("This command is only available for {}".format(ctx.guild.owner.name), delete_after=5)
            return
        
        view = GiveAwayView()
        giveaway = GiveAwayEmbed(view, self.bot, reward_words, minutes*60)

        message = await ctx.send(content="<@&1041653671357849650>", embed=giveaway, view=view)
        await giveaway.start(message)

        await ctx.message.delete()

        print(colored("Admin: ", "blue") + colored("Give Away created!", "green"))