from discord import Embed, Colour
from discord.ui import View
from random import choice
from database.functions import *
import asyncio
from registerid.getid import *


class GiveAwayEmbed(Embed):
    def __init__(self, view: View, bot, reward, readable_time, time):
        self.bot = bot

        super().__init__(title=":tada:   Give Away   :tada:", color=Colour.purple())

        self.view = view
        self.time = time
        self.reward = reward

        self.description = "**A give away being hosted! Click the button below the message to enter in the give away!**"
        self.add_field(name="Time:", value=f"`{readable_time}`", inline=False)
        self.add_field(name="Reward:", value=f"`{reward} words`", inline=False)
    
    async def start(self, id, message):
        await asyncio.sleep(self.time)

        if len(self.view.joined) == 0:
            await message.reply("No one participated")
        else:
            winner = choice(self.view.joined)

            total_words = await give_user_words(winner, self.reward)

            await winner.edit(nick="["+str(total_words)+"] "+winner.name)

            await message.reply("The winner is <@1040533717816459386> !")

        delete_id(id)