import discord
from discord.ext import commands
from termcolor import colored


class AutoRoleCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.reaction_roles = {
            "📢": 1040862991228338206,
            "🎉": 1040863362826895412,
            "📝": 1041653671357849650,
        }


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.message_id == 1041652654037811200:
            guild = self.bot.get_guild(1039438917105102848)
            role = guild.get_role(self.reaction_roles[payload.emoji.name])

            await guild.get_member(payload.user_id).add_roles(role)
        elif payload.channel_id == 1053640012924731442:
            message = self.bot.get_channel(payload.channel_id).get_partial_message(payload.message_id)
            
            if payload.emoji.name == "✅":
                await message.remove_reaction("❌", payload.member)
            elif payload.emoji.name == "❌":
                await message.remove_reaction("✅", payload.member)

        print(colored("Reaction: ", "blue") + colored("Reaction reacted!", "green"))
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.message_id == 1041652654037811200:
            guild = self.bot.get_guild(1039438917105102848)
            role = guild.get_role(self.reaction_roles[payload.emoji.name])

            await guild.get_member(payload.user_id).remove_roles(role)
        
        print(colored("Reaction: ", "blue") + colored("Reaction unreacted!", "green"))