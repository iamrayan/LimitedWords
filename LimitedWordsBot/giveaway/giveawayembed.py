from discord import Embed, Colour
from discord.ui import View
from random import choice
from database.functions import *
import asyncio
from registerid.getid import *
import time
from .giveawayview import GiveAwayView


class GiveAwayEmbed(Embed):
    def __init__(self, view: View, bot, reward, giveaway_time, on_going="On going..."):
        self.bot = bot

        super().__init__(title=":tada:   Give Away   :tada:", color=Colour.purple())

        self.view = view
        self.giveaway_time = giveaway_time
        self.reward = reward

        self.description = "**A give away being hosted! Click the button below the message to enter in the give away!**"
        self.add_field(name="Time:", value=f"<t:{time.time() + self.giveaway_time}:R>", inline=False)
        self.add_field(name="Reward:", value=f"`{reward} words`", inline=False)
        self.add_field(name="Winners:", value=on_going, inline=False)
    
    async def start(self, id, message: discord.Message):
        await asyncio.sleep(self.time)
        
        winner_message = ""

        if len(self.view.joined) == 0:
            await message.reply("No one participated")
            winner_message = "N/A"
        else:
            winner = choice(self.view.joined)

            total_words = await give_user_words(winner, self.reward)

            await winner.edit(nick="["+str(total_words)+"] "+winner.name)

            await message.reply("The winner is <@1040533717816459386> !")
            winner_message = winner.name
        
        disabled_view = GiveAwayView().children[0].disabled = True
        updated_embed = GiveAwayEmbed(self.view, self.bot, self.reward, self.giveaway_time, on_going=winner_message)

        await message.edit(embed=updated_embed, view=disabled_view)

        delete_id(id)