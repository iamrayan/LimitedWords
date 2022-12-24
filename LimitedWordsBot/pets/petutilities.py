from dataclasses import dataclass


class PetAbilities:
    def __init__(self, speed: int, agility: int, strength: int):
        self.speed = speed
        self.agility = agility
        self.strength = strength
    
class PetPerks:
    def __init__(self, monkerate: int, invite_boost: int):
        self.monkerate = monkerate
        self.invite_boost = invite_boost