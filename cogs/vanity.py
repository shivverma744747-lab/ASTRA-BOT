import discord
from discord.ext import commands
import json
import os

class VanityRolesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BOT_COLOR = discord.Color(0x000000)
        self.vanity_file = "data/vanity.json"
        self.load_vanity()

    def load_vanity(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if os.path.exists(self.vanity_file):
            with open(self.vanity_file, 'r') as f:
                self.vanity = json.load(f)
        else:
            self.vanity = {}

    def save_vanity(self):
        with open(self.vanity_file, 'w') as f:
            json.dump(self.vanity, f, indent=2)

    @commands.command(name="vanity")
    @commands.has_permissions(manage_roles=True)
    async def vanity(self, ctx, member: discord.Member, *, role_name: str = None):
        """Create a vanity role for a member"""
        if role_name is None:
            role_name = f"{member.name}'s Role"
        
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)
        
        # Check if user already has a vanity role
        if guild_id in self.vanity and user_id in self.vanity[guild_id]:
            old_role_id = self.vanity[guild_id][user_id]
            try:
                old_role = ctx.guild.get_role(old_role_id)
                if old_role:
                    await old_role.delete()
            except:
                pass
        
        # Create new role
        try:
            role = await ctx.guild.create_role(
                name=role_name,
                color=discord.Color(0x000000)
            )
            
            await member.add_roles(role)
            
            if guild_id not in self.vanity:
                self.vanity[guild_id] = {}
            
            self.vanity[guild_id][user_id] = role.id
            self.save_vanity()
            
            embed = discord.Embed(
                title="🌈 Vanity Role Created",
                description=f"{member.mention} now has {role.mention}",
                color=self.BOT_COLOR
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Failed to create role: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(VanityRolesCog(bot))
