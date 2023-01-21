import discord
from discord.ext import commands
from discord import app_commands
from database.functions import *
from time import time
from termcolor import colored


class ModerationCog(commands.Cog):
    @app_commands.command(name="warn")
    async def warn(self, interaction: discord.Interaction, user: discord.Member, reason: str):
        if is_prisoner(user):
            await interaction.response.send_message("User is in prison", ephemeral=True)
            return

        warns = warn_user(user)

        if warns == 3:
            await add_prisoner(user, "Warning reached 3", time() + 86400)
            await user.edit(nick=f"[prison] {user.name}")
            await user.add_roles(interaction.guild.get_role(1046101250468487168))
            
            dm = await user.create_dm()
            await dm.send("You have reached 3 warnings and you have been sent to the **Prison**")

            await interaction.response.send_message(f"<@{user.id}> has been warned\n<@{user.id}> has been sent to prison due to reaching 3 warnings")

            print(colored("Mod: ", "blue") + colored("Warn command called and sent to Prison!", "green"))

            return
        
        if warns == 5:
            dm = await user.create_dm()
            await dm.send("You have been **Banned** on Limited Words\nReason: Reaching 5 warnings")
            await interaction.response.send_message(f"<@{user.id}> has been warned\n<@{user.id}> has been banned due to reached 5 warnings")
            await interaction.guild.ban(user, reason="Reached 5 warnings")

            print(colored("Mod: ", "blue") + colored("Warn command called and banned!", "green"))

            return

        dm = await user.create_dm()
        await dm.send(f"You have been **Warned** on Limited Words for {reason}")
        await interaction.response.send_message(f"<@{user.id}> has been warned\nTotal warnings: {warns}\nReason: {reason}")

        print(colored("Mod: ", "blue") + colored("Warn command called!", "green"))

    
    @app_commands.command(name="release", description="Release prisoners")
    async def release(self, interaction: discord.Interaction, user: discord.Member):
        if not is_prisoner(user):
            await interaction.response.send_message("User is not a prisoner", ephemeral=True)
            return
        
        await my_base.release_prisoner(user)

        dm = await user.create_dm()
        await dm.send("You have been released from **Prison**")
        await interaction.response.send_message("User has been released from prison!", ephemeral=True)

        print(colored("Mod: ", "blue") + colored("Release command called!", "green"))

    
    @app_commands.command(name="prison", description="Put someone in prison")
    async def prison(self, interaction: discord.Interaction, user: discord.Member, reason: str, seconds: int):
        if is_prisoner(user):
            await interaction.response.send_message("User is already a prisoner", ephemeral=True)
            return
        
        await interaction.response.defer()

        await add_prisoner(user, reason, time() + seconds)
        await user.edit(nick=f"[prison] {user.name}")
        await user.add_roles(interaction.guild.get_role(1046101250468487168))
            
        dm = await user.create_dm()
        await dm.send(f"You have been sent to prison\nBy: `{interaction.user.name}`\nReason: `{reason}`")

        await interaction.followup.send(f"<@{user.id}> has been sent to prison\nReason: {reason}")

        print(colored("Mod: ", "blue") + colored("Prison command called and sent to Prison!", "green"))