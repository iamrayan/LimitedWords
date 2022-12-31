from discord import Embed, Colour
from discord.ui import View
from random import choice
from database.functions import *
import asyncio
import time
from .giveawayview import GiveAwayView
from math import floor


class GiveAwayEmbed(Embed):
    def __init__(self, view: View, bot, reward, giveaway_time, on_going="On going..."):
        self.bot = bot

        super().__init__(title=":tada:   Give Away   :tada:", color=choice([Colour.red(), Colour.green()]))

        self.view = view
        self.giveaway_time = giveaway_time
        self.reward = reward

        self.description = "**A give away being hosted! Click the button below the message to enter in the give away!**"
        self.add_field(name="Time:", value=f"<t:{floor(time.time() + self.giveaway_time)}:R>", inline=False)
        self.add_field(name="Reward:", value=f"`{reward} words`", inline=False)
        self.add_field(name="Winners:", value=f"`{on_going}`", inline=False)
    
    async def start(self, message: discord.Message):
        await asyncio.sleep(self.giveaway_time)
        
        winner_message = ""

        if len(self.view.joined) == 0:
            await message.reply("No one participated")
            winner_message = "N/A"
        else:
            winner = None

            while True:
                winner = choice(self.view.joined)
                if message.guild.get_member(winner) is not None:
                    break

            if not is_prisoner(winner):
                total_words = await give_user_words(winner, self.reward)

                await winner.edit(nick="["+str(total_words)+"] "+winner.name)

                await message.reply("The winner is <@1040533717816459386> !")
            else:
                delay_word(winner, self.reward)

                await message.reply("The winner is <@1040533717816459386> !\nSince <@1040533717816459386> is currently in prison, his words will be delayed till he gets out of prison")

            winner_message = winner.name
        
        disabled_view = GiveAwayView()
        GiveAwayView().children[0].disabled = True
        
        updated_embed = GiveAwayEmbed(self.view, self.bot, self.reward, self.giveaway_time, on_going=winner_message)

        await message.edit(embed=updated_embed, view=disabled_view)