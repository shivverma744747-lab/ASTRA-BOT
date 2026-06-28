import discord
from discord.ext import commands

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BOT_COLOR = discord.Color(0x000000)
        self.OWNER_ID = 1427675629351866398

    async def check_superuser_protection(self, member):
        """Check if member is protected by superuser system"""
        return member.id in self.bot.superusers

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Ban a member"""
        if await self.check_superuser_protection(member):
            embed = discord.Embed(
                title="❌ Protected",
                description=f"{member.mention} is a superuser and cannot be banned",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        await member.ban(reason=reason)
        
        embed = discord.Embed(
            title="🔨 Member Banned",
            description=f"{member.mention} has been banned",
            color=self.BOT_COLOR
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User, *, reason="No reason provided"):
        """Unban a user"""
        await ctx.guild.unban(user, reason=reason)
        
        embed = discord.Embed(
            title="✅ Member Unbanned",
            description=f"{user.mention} has been unbanned",
            color=self.BOT_COLOR
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="softban")
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Softban a member (ban and unban to delete messages)"""
        if await self.check_superuser_protection(member):
            embed = discord.Embed(
                title="❌ Protected",
                description=f"{member.mention} is a superuser and cannot be softbanned",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        await member.ban(reason=reason)
        await ctx.guild.unban(member, reason=f"Softban: {reason}")
        
        embed = discord.Embed(
            title="🔨 Member Softbanned",
            description=f"{member.mention} has been softbanned (messages deleted)",
            color=self.BOT_COLOR
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Kick a member"""
        if await self.check_superuser_protection(member):
            embed = discord.Embed(
                title="❌ Protected",
                description=f"{member.mention} is a superuser and cannot be kicked",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        await member.kick(reason=reason)
        
        embed = discord.Embed(
            title="👢 Member Kicked",
            description=f"{member.mention} has been kicked",
            color=self.BOT_COLOR
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="mute")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Mute a member"""
        if await self.check_superuser_protection(member):
            embed = discord.Embed(
                title="❌ Protected",
                description=f"{member.mention} is a superuser and cannot be muted",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
        
        await member.add_roles(muted_role)
        
        embed = discord.Embed(
            title="🔇 Member Muted",
            description=f"{member.mention} has been muted",
            color=self.BOT_COLOR
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="unmute")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Unmute a member"""
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if muted_role:
            await member.remove_roles(muted_role)
        
        embed = discord.Embed(
            title="🔊 Member Unmuted",
            description=f"{member.mention} has been unmuted",
            color=self.BOT_COLOR
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="warn")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Warn a member"""
        if await self.check_superuser_protection(member):
            embed = discord.Embed(
                title="❌ Protected",
                description=f"{member.mention} is a superuser and cannot be warned",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(
            title="⚠️ Member Warned",
            description=f"{member.mention} has been warned",
            color=discord.Color.orange()
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="unwarn")
    @commands.has_permissions(manage_messages=True)
    async def unwarn(self, ctx, member: discord.Member):
        """Unwarn a member"""
        embed = discord.Embed(
            title="✅ Warning Removed",
            description=f"{member.mention}'s warning has been removed",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="say")
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, *, message: str):
        """Make the bot say something"""
        await ctx.send(message)
        await ctx.message.delete()

async def setup(bot):
    await bot.add_cog(ModerationCog(bot))
