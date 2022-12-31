from discord import ui, ButtonStyle, Interaction, Embed, Colour
from discord.ext import commands, tasks
from database.functions import give_user_words
from asyncio import sleep
from random import randint


active = False

class WordPopUp(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.popupmessage.start()

    @tasks.loop(seconds=1.0)
    async def popupmessage(self):
        general = self.bot.get_guild(1039438917105102848).get_channel(1039443108926083082)

        reward = randint(20, 45)

        embed = Embed(title="Word Drop", color=Colour.random())
        embed.description = f"{reward} words have been dropped of an cargo plane into\nthis channel. Click the below button to collect it.\nOnly the first can get it!"

        global active
        active = True

        await general.send(embed=embed, view=WordPopUpView(reward))

        while True:
            if not active:
                await sleep(randint(10800, 21600))
                break
            else:
                await sleep(60)        


class WordPopUpView(ui.View):
    def __init__(self, reward):
        super().__init__(timeout=None)
        self.reward = reward
    

    @ui.button(label="Claim Words", style=ButtonStyle.success)
    async def popupclicked(self, interaction: Interaction, button):
        words = await give_user_words(interaction.user, self.reward)

        disabled_view = WordPopUpView(self.reward)

        for i in disabled_view.children:
            i.disabled = True

        global active
        active = False

        await interaction.message.edit(view=disabled_view)
        await interaction.user.edit(nick=f"[{words}] {interaction.user.name}")
        await interaction.response.send_message(f"<@{interaction.user.id}> has collected the words!")