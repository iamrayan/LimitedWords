import discord
from discord.ext import commands
from database.functions import *
from time import time
import math
import random
from termcolor import colored


play_cooldown = {}
feed_cooldown = {}


def decide_mood(pet):
    if pet.mood < 30:
        return discord.Colour.red()
    elif pet.mood < 50:
        return discord.Colour.yellow()
    elif pet.mood <= 100:
        return discord.Colour.green()

def convert(seconds: int):
    if seconds < 60:
        return f"{math.floor(seconds)} seconds"
    if seconds < 3600:
        return f"{math.floor(seconds/60)} minutes"
    if seconds > 86400:
        return f"{math.floor(seconds/3600)} hours"


def attach_commands(bot: commands.Bot):
    @bot.tree.command(name="petstats", description="Reveal your pet stats!")
    async def petstats(interaction: discord.Interaction):
        if not pet_exists(interaction.user):
            await interaction.response.send_message("Unfortunately, you do not have any pets")
            return

        changed = False

        selected_pet = pet_selected(interaction.user)
        last_active = my_base.data[str(interaction.user.id)]["lastpetactive"]
        active_times = int((time() - last_active) / 1800)

        if active_times > 1:
            for _ in range(int(active_times)):
                selected_pet.mood -= random.randint(4, 8)
                changed = True

        if selected_pet.mood < 0: selected_pet.mood = 0 

        pet_embed = discord.Embed(title=f"{interaction.user.name}'s {str(selected_pet)}", color=decide_mood(selected_pet))
            
        pet_embed.set_thumbnail(url="https://png.pngtree.com/png-clipart/20200225/original/pngtree-christmas-snowman-vector-download-png-image_5275255.jpg")
        pet_embed.add_field(name="Mood", value=f"`{selected_pet.mood}`")
        pet_embed.add_field(name="Monke Rate", value=f"`{selected_pet.perks.monkerate}%`")
        pet_embed.add_field(name="Invite Boost", value=f"`{selected_pet.perks.invite_boost}`")
        pet_embed.add_field(name="Speed", value=f"`{selected_pet.abilities.speed}`")
        pet_embed.add_field(name="Agility", value=f"`{selected_pet.abilities.agility}`")
        pet_embed.add_field(name="Strength", value=f"`{selected_pet.abilities.strength}`")

        await interaction.response.send_message(embed=pet_embed)

        if changed:
            update_pet(interaction.user, selected_pet)
            my_base.data[str(interaction.user.id)]["lastpetactive"] = time()
        
        print(colored("Command: ", "blue") + colored("Petstats command called!", "green"))
    

    @bot.tree.command(name="feed", description="Feed your Pet!")
    async def feedpet(interaction: discord.Interaction):
        cooldown = feed_cooldown.get(interaction.user.id)
        if cooldown is not None:
            if cooldown - time() < 0:
                feed_cooldown.pop(interaction.user.id)
            else:
                await interaction.response.send_message(f"Your pet's tummy is filled up now, come back in {convert(cooldown - time())} to feed your pet again!")
                return
        if not pet_exists(interaction.user):
            await interaction.response.send_message("Unfortunately, you do not have any pets")
            return

        changed = False

        selected_pet = pet_selected(interaction.user)
        last_active = my_base.data[str(interaction.user.id)]["lastpetactive"]
        active_times = int((time() - last_active) / 1800)

        if active_times > 1:
            for _ in range(int(active_times)):
                selected_pet.mood -= random.randint(4, 8)
                changed = True

        if selected_pet.mood < 0: selected_pet.mood = 0

        mood_before = selected_pet.mood
        mood = selected_pet.feed()

        mood_embed = discord.Embed(color=decide_mood(selected_pet))
        
        mood_embed.description = f"**{str(selected_pet)}'s mood**"
        mood_embed.add_field(name="before", value=f"`{mood_before}`")
        mood_embed.add_field(name="after", value=f"`{mood}`")
        mood_embed.set_footer(text=f"Increased by {mood - mood_before}")

        await interaction.response.send_message(embed=mood_embed)

        update_pet(interaction.user, selected_pet)

        if changed:
            my_base.data[str(interaction.user.id)]["lastpetactive"] = time()

        feed_cooldown[interaction.user.id] = time() + 3600

        print(colored("Command: ", "blue") + colored("Feed command called!", "green"))
    

    @bot.tree.command(name="play", description="Play with your Pet!")
    async def playpet(interaction: discord.Interaction):
        cooldown = play_cooldown.get(interaction.user.id)
        if cooldown is not None:
            if cooldown - time() < 0:
                play_cooldown.pop(interaction.user.id)
            else:
                await interaction.response.send_message(f"Your pet's tired from the last time he played, come back in {convert(cooldown - time())} to play with your pet again!")
                return
        if not pet_exists(interaction.user):
            await interaction.response.send_message("Unfortunately, you do not have any pets")
            return
        
        changed = False

        selected_pet = pet_selected(interaction.user)
        last_active = my_base.data[str(interaction.user.id)]["lastpetactive"]
        active_times = int((time() - last_active) / 1800)

        if active_times > 1:
            for _ in range(int(active_times)):
                selected_pet.mood -= random.randint(4, 8)
                changed = True
        
        if selected_pet.mood < 0: selected_pet.mood = 0

        before_mood = selected_pet.mood

        play_result = selected_pet.play().split(" ")

        play_embed = discord.Embed(title=f"{play_result[0]} Improved!", color=decide_mood(selected_pet))
        play_embed.add_field(name=play_result[0], value=f"`{play_result[1]}`")
        play_embed.add_field(name="\u2800", value="\u2800")
        play_embed.add_field(name="Mood", value=f"`{selected_pet.mood}`")
        play_embed.add_field(name="Before", value=f"`{play_result[2]}`")
        play_embed.add_field(name="\u2800", value="\u2800")
        play_embed.add_field(name="Before", value=f"`{before_mood}`")

        await interaction.response.send_message(embed=play_embed)

        update_pet(interaction.user, selected_pet)

        if changed:
            my_base.data[str(interaction.user.id)]["lastpetactive"] = time()

        play_cooldown[interaction.user.id] = time() + 3600

        print(colored("Command: ", "blue") + colored("Play command called!", "green"))