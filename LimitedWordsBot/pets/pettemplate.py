from .petutilities import PetAbilities, PetPerks
import random


feed_improved_min, feed_improved_max = 15, 30
play_improved_min, play_improved_max = 5, 25

class PetTemplate:
    def __init__(self, abilities: PetAbilities, perks: PetPerks, mood: int):
        self.abilities = abilities
        self.perks = perks
        self.mood = mood
    
    def feed(self):
        result = random.randint(feed_improved_min, feed_improved_max)
        self.mood += result
        
        if self.mood > 100: self.mood = 100

        return self.mood
    
    def play(self):
        result = random.randint(play_improved_min, play_improved_max)
        self.mood += result
        
        if self.mood > 100: self.mood = 100

        ability_choice = random.randint(1, 3)

        if ability_choice == 1:
            speed = random.randint(1, 3)
            self.abilities.speed += speed

            if self.abilities.speed > 100: self.abilities.speed = 100

            return f"Speed {self.abilities.speed} {self.abilities.speed - speed}"
        elif ability_choice == 2:
            agility = random.randint(1, 3)
            self.abilities.agility += agility
            
            if self.abilities.agility > 100: self.abilities.agility = 100

            return f"Agility {self.abilities.agility} {self.abilities.agility - agility}"
        elif ability_choice == 3:
            strength = random.randint(1, 3)
            self.abilities.strength += strength
            
            if self.abilities.strength > 100: self.abilities.strength = 100

            return f"Strength {self.abilities.strength} {self.abilities.strength - strength}"