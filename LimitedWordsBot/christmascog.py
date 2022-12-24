import discord
from discord import ui
from discord.ext import commands
from database.functions import *
import asyncio
from termcolor import colored


class ChristmasCog(commands.Cog):
    @commands.command()
    async def christmastime(self, ctx: commands.Context):
        embed = discord.Embed(title="**Ho, Ho, Ho...**  ", color=discord.Colour.green())
        embed.description = "*To celebrate Christmas, we will be offering a\ngreat opportunity for anyone to receive any\nwish from the list below*"
        embed.set_footer(text="🎅 This is a limited time offer 🎅")
        
        view = ChristmasView()

        message = await ctx.send(embed=embed, view=view)

        view.add_message(message)
        await view.end()


class ChristmasView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.sleep_time = 432000
    

    @ui.button(label="500 words", style=discord.ButtonStyle.danger)
    async def wordwish(self, interaction: discord.Interaction, button: ui.Button):
        if my_base.data[str(interaction.user.id)]["wish"]:
            await interaction.response.send_message("You have already made your wish!", ephemeral=True)
            return
        
        words = await give_user_words(interaction.user, 500)

        await interaction.user.edit(nick="["+str(words)+"] "+interaction.user.name)

        my_base.data[str(interaction.user.id)]["wish"] = True

        await interaction.response.send_message("Wish Granted!\n500 words have been added to your balance!")

        print(colored("Christmas: ", "blue") + colored("500 words wish made!", "green"))
    
    
    @ui.button(label="Monkerate 25%+", style=discord.ButtonStyle.success)
    async def increasemonkerate(self, interaction: discord.Interaction, button: ui.Button):
        if my_base.data[str(interaction.user.id)]["wish"]:
            await interaction.response.send_message("You have already made your wish!", ephemeral=True)
            return
        
        rate = add_monkerate(interaction.user, 25)

        my_base.data[str(interaction.user.id)]["wish"] = True

        await interaction.response.send_message(f"Wish Granted!\nYour monke rate is now {rate}!")

        print(colored("Christmas: ", "blue") + colored("25%+ Monke Rate wish made!", "green"))
    

    @ui.button(label="Snowman (pet)", style=discord.ButtonStyle.danger)    
    async def petsnowman(self, interaction: discord.Interaction, button: ui.Button):
        if my_base.data[str(interaction.user.id)]["wish"]:
            await interaction.response.send_message("You have already made your wish!", ephemeral=True)
            return
        
        ability = PetAbilities(10, 10, 10)
        perks = PetPerks(5, 30)

        add_pet(interaction.user, Snowman(ability, perks, 100))

        my_base.data[str(interaction.user.id)]["wish"] = True

        await interaction.response.send_message(f"Wish Granted!\nYou have recieved a Snowman pet!", ephemeral=True)

        print(colored("Christmas: ", "blue") + colored("Snowman wish made!", "green"))
    
    
    def add_message(self, message: discord.Message):
        self.message = message


    async def end(self):
        await asyncio.sleep(self.sleep_time)
        
        disabled_view = ChristmasView()

        for i in disabled_view.children:
            i.disabled = True

        await self.message.edit(view=disabled_view)
