from discord import ButtonStyle, PartialEmoji, Interaction
from discord.ui import Button, View, button


class GiveAwayView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.joined = []
    
    @button(style=ButtonStyle.success, emoji=PartialEmoji(name="🎉"))
    async def giveawaybutton(self, interaction: Interaction, button: Button):
        if interaction.user in self.joined:
                await interaction.response.send_message("You have already joined this give away", ephemeral=True)
                return

        self.joined.append(interaction.user)
        await interaction.response.send_message("Good Luck!", ephemeral=True)
        return