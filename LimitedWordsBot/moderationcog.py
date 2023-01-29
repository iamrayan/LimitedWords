import discord
from discord.ext import commands
from discord import app_commands
from database.functions import *
from time import time
from termcolor import colored


class ModerationCog(commands.Cog):
    @app_commands.command(name="warn")
    async def warn(self, interaction: discord.Interaction, user: discord.Member, reason: str):
        await interaction.response.defer()

        if is_prisoner(user):
            await interaction.response.send_message("User is in prison", ephemeral=True)
            return

        warns = warn_user(user)

        if warns == 3:
            await add_prisoner(user, "Warning reached 3", time() + 86400)
            await user.edit(nick=f"[prison] {user.name}")
            await user.add_roles(interaction.guild.get_role(1046101250468487168))

            response_embed = WarnResponseEmbed(user.name, 3, discord.Colour.red(), reason, "Prison")

            await interaction.followup.send(embed=response_embed)

            print(colored("Mod: ", "blue") + colored("Warn command called and sent to Prison!", "green"))

            return
        
        if warns == 5:
            dm_embed = WarnEmbed(5, discord.Colour.red(), reason, punishment="Ban")

            dm = await user.create_dm()
            await dm.send(embed=dm_embed)

            response_embed = WarnResponseEmbed(user.name, 5, discord.Colour.red(), reason, "Ban")

            await interaction.followup.send(embed=response_embed)
            await interaction.guild.ban(user, reason="Reached 5 warnings")

            print(colored("Mod: ", "blue") + colored("Warn command called and banned!", "green"))

            return

        dm_embed = WarnEmbed(warns, discord.Colour.yellow(), reason, "N/A")

        dm = await user.create_dm()
        await dm.send(embed=dm_embed)

        response_embed = WarnResponseEmbed(user.name, warns, discord.Colour.yellow(), reason, "N/A")

        await interaction.response.send_message(embed=response_embed)

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

        await interaction.followup.send(f"<@{user.id}> has been sent to prison\nReason: {reason}")

        print(colored("Mod: ", "blue") + colored("Prison command called and sent to Prison!", "green"))
    

    @app_commands.command(name="revokewarn", description="Revoke a warn from a user")
    async def revokewarn(self, interaction: discord.Interaction, user: discord.Member):
        before_warns = get_user_warns(user)

        if before_warns == 0:
            await interaction.response.send_message("User has no warns")
            return
        
        after_warns = revoke_warn(user)

        embed = discord.Embed(title="Warning Revoked", color=discord.Colour.random())

        embed.description = f"**User** - {user.name}"

        embed.add_field(name="Before", value=f"`{before_warns}`")
        embed.add_field(name="After", value=f"`{after_warns}`")

        await interaction.response.send_message(embed=embed)

        print(colored("Mod: ", "blue") + colored("Revoke Warn command called", "green"))
    

class WarnEmbed(discord.Embed):
    def __init__(self, warn_number: int, color: discord.Colour, reason: str, punishment: str):
        super().__init__(title="Warning Alert", color=color)
        
        self.description = f"**Warnings** - {warn_number}\n**Reason** - {reason}\n**Punishment** - {punishment}"
        self.set_footer(text="Be careful around the server")


class WarnResponseEmbed(discord.Embed):
    def __init__(self, user_name: str, warn_number: int, color: discord.Colour, reason: str, punishment: str):
        super().__init__(title=f"{user_name}'s warning", color=color)

        self.description = f"**Warnings** - {warn_number}\n**Reason** - {reason}\n**Punishment** - {punishment}"
        self.set_footer(text="Learn from the mistakes of others")