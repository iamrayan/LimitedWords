from discord import Embed, Colour



class MonkeEmbed(Embed):
    def __init__(self, description, bet_amount, return_amount):
        super().__init__(title="🐒  Monke Gamble  🐒", colour=Colour.from_rgb(150, 75, 0))

        self.description = description
        self.add_field(name="Bet Amount", value=f"`{bet_amount}`")
        self.add_field(name="Return Amount", value=f"`{return_amount}`")
        self.set_footer(text="🙈🙉🙈🙉🙈🙉🙈")