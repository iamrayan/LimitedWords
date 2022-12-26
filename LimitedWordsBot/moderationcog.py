import discord
from discord.ext import commands
from discord import app_commands
from database.functions import *
from time import time


class ModerationCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        bot.tree.add_command(self.warn)


    @app_commands.context_menu(name="Warn")
    async def warn(interaction: discord.Interaction, user: discord.Member):
        if is_prisoner(user):
            await interaction.response.send_message("User is in prison", ephemeral=True)
            return

        warns = warn_user(user)

        if warns == 3:
            await add_prisoner(user, "Warning reached 3", time() + 86400)
            await user.edit(nick=f"[prison] {interaction.user.name}")
            await user.add_roles(interaction.guild.get_role(1046101250468487168))
            
            dm = await user.create_dm()
            await dm.send("You have reached 3 warnings and you have been sent to the **Prison**")

            await interaction.response.send_message(f"<@{user.id}> has been warned\n<@{user.id}> has been sent to prison due to reaching 3 warnings")
            return
        
        if warns == 5:
            dm = await user.create_dm()
            await dm.send("You have been **Banned** on Limited Words\nReason: Reaching 5 warnings")
            await interaction.response.send_message(f"<@{user.id}> has been warned\n<@{user.id}> has been banned due to reached 5 warnings")
            await interaction.guild.ban(interaction.user, reason="Reached 5 warnings")

            return

        await interaction.response.send_message(f"<@{user.id}> has been warned\nTotal warns for <@{user.id}> - {warns}")

    
    @app_commands.context_menu(name="Release")
    async def release(interaction: discord.Interaction, user: discord.Member):
        if not is_prisoner(user):
            await interaction.response.send_message("User is not a prisoner", ephemeral=True)
            return
        
        await my_base.release_prisoner(user)

        dm = await user.create_dm()
        await dm.send("You have been released from prison!")
        await interaction.response.send_message("User has been released from prison!", ephemeral=True)