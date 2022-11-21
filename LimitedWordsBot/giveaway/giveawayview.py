from discord import ButtonStyle, PartialEmoji, Interaction
from discord.ui import Button, View


class GiveAwayView(View):
    def __init__(self, id):
        super().__init__()
        self.joined = []

        button = Button(style=ButtonStyle.success, custom_id=id, emoji=PartialEmoji(name="🎉"))

        button.callback = self.callback

        self.add_item(button)
    
    async def callback(self, interaction: Interaction):
            if interaction.user in self.joined:
                await interaction.response.send_message("You have already joined this give away", ephemeral=True)
                return

            self.joined.append(interaction.user)
            await interaction.response.send_message("Good Luck!", ephemeral=True)
            return