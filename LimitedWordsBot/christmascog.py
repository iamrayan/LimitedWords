import discord
from discord import ui
from discord.ext import commands
from database.functions import my_base, give_user_words


class ChristmasCog(commands.Cog):
    def __init__(self):
        pass
    
    @commands.command()
    async def chrismastime(self):
        embed = discord.Embed("**Ho, Ho, Ho...**  ", color=discord.Colour.green())
        embed.description = "*To celebrate Christmas, we will be offering a\ngreat opportunity for anyone to receive any\nwish from the list below*"
        embed.set_footer(text="🎅 This is a limited time offer 🎅")


class ChristmasView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    

    @ui.button(label="1000 words")
    async def wordwish(self, interaction: discord.Interaction, button: ui.Button):
        if my_base[str(interaction.user.id)]["wish"]:
            await interaction.response.send_message("You have already made your wish!", ephemeral=True)
            return
        
        words = await give_user_words(interaction.user, 1000)

        await interaction.user.edit(nick="["+str(words)+"] "+interaction.user.name)

        my_base[str(interaction.user.id)]["wish"] = True