import discord
from discord.ext import commands
import json
import os

class ReactionRolesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BOT_COLOR = discord.Color(0x000000)
        self.reaction_roles_file = "data/reactionroles.json"
        self.load_reaction_roles()

    def load_reaction_roles(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if os.path.exists(self.reaction_roles_file):
            with open(self.reaction_roles_file, 'r') as f:
                self.reaction_roles = json.load(f)
        else:
            self.reaction_roles = {}

    def save_reaction_roles(self):
        with open(self.reaction_roles_file, 'w') as f:
            json.dump(self.reaction_roles, f, indent=2)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            return
        
        message_id = str(payload.message_id)
        guild_id = str(payload.guild_id)
        
        if guild_id not in self.reaction_roles or message_id not in self.reaction_roles[guild_id]:
            return
        
        emoji = str(payload.emoji)
        if emoji not in self.reaction_roles[guild_id][message_id]:
            return
        
        role_id = self.reaction_roles[guild_id][message_id][emoji]
        guild = self.bot.get_guild(payload.guild_id)
        role = guild.get_role(role_id)
        member = guild.get_member(payload.user_id)
        
        if role and member:
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.user_id == self.bot.user.id:
            return
        
        message_id = str(payload.message_id)
        guild_id = str(payload.guild_id)
        
        if guild_id not in self.reaction_roles or message_id not in self.reaction_roles[guild_id]:
            return
        
        emoji = str(payload.emoji)
        if emoji not in self.reaction_roles[guild_id][message_id]:
            return
        
        role_id = self.reaction_roles[guild_id][message_id][emoji]
        guild = self.bot.get_guild(payload.guild_id)
        role = guild.get_role(role_id)
        member = guild.get_member(payload.user_id)
        
        if role and member:
            await member.remove_roles(role)

    @commands.command(name="reactionrole")
    @commands.has_permissions(manage_roles=True)
    async def reactionrole(self, ctx, message_id: int, emoji: str, role: discord.Role):
        """Add reaction role to a message"""
        try:
            message = await ctx.channel.fetch_message(message_id)
        except:
            embed = discord.Embed(
                title="❌ Error",
                description="Message not found",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        guild_id = str(ctx.guild.id)
        message_id_str = str(message_id)
        
        if guild_id not in self.reaction_roles:
            self.reaction_roles[guild_id] = {}
        if message_id_str not in self.reaction_roles[guild_id]:
            self.reaction_roles[guild_id][message_id_str] = {}
        
        self.reaction_roles[guild_id][message_id_str][emoji] = role.id
        self.save_reaction_roles()
        
        await message.add_reaction(emoji)
        
        embed = discord.Embed(
            title="😊 Reaction Role Added",
            description=f"Emoji: {emoji}\nRole: {role.mention}",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ReactionRolesCog(bot))
