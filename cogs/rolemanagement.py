import discord
from discord.ext import commands

class RoleManagementCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BOT_COLOR = discord.Color(0x000000)

    @commands.command(name="roleall")
    @commands.has_permissions(manage_roles=True)
    async def roleall(self, ctx, role: discord.Role):
        """Give a role to all members in the server"""
        count = 0
        async for member in ctx.guild.fetch_members(limit=None):
            if not member.bot:
                try:
                    await member.add_roles(role)
                    count += 1
                except:
                    pass
        
        embed = discord.Embed(
            title="✅ Role Added",
            description=f"{role.mention} has been added to {count} members",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="roleadd")
    @commands.has_permissions(manage_roles=True)
    async def roleadd(self, ctx, member: discord.Member, role: discord.Role):
        """Add a role to a member"""
        await member.add_roles(role)
        
        embed = discord.Embed(
            title="✅ Role Added",
            description=f"{role.mention} has been added to {member.mention}",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="roleremove")
    @commands.has_permissions(manage_roles=True)
    async def roleremove(self, ctx, member: discord.Member, role: discord.Role):
        """Remove a role from a member"""
        await member.remove_roles(role)
        
        embed = discord.Embed(
            title="✅ Role Removed",
            description=f"{role.mention} has been removed from {member.mention}",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="roleremoveall")
    @commands.has_permissions(manage_roles=True)
    async def roleremoveall(self, ctx, role: discord.Role):
        """Remove a role from all members"""
        count = 0
        async for member in ctx.guild.fetch_members(limit=None):
            if role in member.roles:
                try:
                    await member.remove_roles(role)
                    count += 1
                except:
                    pass
        
        embed = discord.Embed(
            title="✅ Role Removed",
            description=f"{role.mention} has been removed from {count} members",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="rolecreate")
    @commands.has_permissions(manage_roles=True)
    async def rolecreate(self, ctx, *, name: str):
        """Create a new role"""
        role = await ctx.guild.create_role(name=name, color=discord.Color(0x000000))
        
        embed = discord.Embed(
            title="✅ Role Created",
            description=f"{role.mention} has been created",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="roledelete")
    @commands.has_permissions(manage_roles=True)
    async def roledelete(self, ctx, role: discord.Role):
        """Delete a role"""
        role_name = role.name
        await role.delete()
        
        embed = discord.Embed(
            title="✅ Role Deleted",
            description=f"{role_name} has been deleted",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="roleedit")
    @commands.has_permissions(manage_roles=True)
    async def roleedit(self, ctx, role: discord.Role, *, name: str):
        """Edit a role name"""
        await role.edit(name=name)
        
        embed = discord.Embed(
            title="✅ Role Edited",
            description=f"{role.mention} has been renamed to {name}",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(RoleManagementCog(bot))
