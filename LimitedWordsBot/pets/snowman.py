from discord import Member
from .pettemplate import PetTemplate
from .petutilities import *


class Snowman(PetTemplate):
    def __init__(self, abilities: PetAbilities, perks: PetPerks, mood: int):
        super().__init__(abilities, perks, mood)

    def __str__(self) -> str:
        return "Snowman"