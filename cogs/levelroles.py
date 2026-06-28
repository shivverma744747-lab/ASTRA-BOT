import discord
from discord.ext import commands
import json
import os

class LevelRolesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BOT_COLOR = discord.Color(0x000000)
        self.level_roles_file = "data/levelroles.json"
        self.load_level_roles()

    def load_level_roles(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if os.path.exists(self.level_roles_file):
            with open(self.level_roles_file, 'r') as f:
                self.level_roles = json.load(f)
        else:
            self.level_roles = {}

    def save_level_roles(self):
        with open(self.level_roles_file, 'w') as f:
            json.dump(self.level_roles, f, indent=2)

    @commands.command(name="levelrole")
    @commands.has_permissions(manage_roles=True)
    async def levelrole(self, ctx, level: int, role: discord.Role):
        """Set a role to be given at a specific level"""
        guild_id = str(ctx.guild.id)
        
        if guild_id not in self.level_roles:
            self.level_roles[guild_id] = {}
        
        self.level_roles[guild_id][str(level)] = role.id
        self.save_level_roles()
        
        embed = discord.Embed(
            title="✅ Level Role Set",
            description=f"Level {level}: {role.mention}",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    async def check_level_roles(self, member, guild_id, level):
        """Check and assign level roles"""
        guild_id_str = str(guild_id)
        
        if guild_id_str not in self.level_roles:
            return
        
        for req_level, role_id in self.level_roles[guild_id_str].items():
            if int(req_level) <= level:
                role = member.guild.get_role(role_id)
                if role and role not in member.roles:
                    try:
                        await member.add_roles(role)
                    except:
                        pass

async def setup(bot):
    await bot.add_cog(LevelRolesCog(bot))
