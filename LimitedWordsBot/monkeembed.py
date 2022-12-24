from discord import Embed, Colour
from random import choice



class MonkeEmbed(Embed):
    def __init__(self, description, bet_amount, return_amount):
        super().__init__(title="🐒  Monke Gamble  🐒", colour=choice([Colour.red(), Colour.green()]))

        self.description = description
        self.add_field(name="Bet Amount", value=f"`{bet_amount}`")
        self.add_field(name="Return Amount", value=f"`{return_amount}`")
        self.set_footer(text="🙈🙉🙈🙉🙈🙉🙈")