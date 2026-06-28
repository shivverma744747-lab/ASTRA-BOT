import discord
from discord.ext import commands
import json
import os

class VoiceModCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BOT_COLOR = discord.Color(0x000000)
        self.OWNER_ID = 1427675629351866398

    @commands.command(name="vckick")
    @commands.has_permissions(move_members=True)
    async def vckick(self, ctx, member: discord.Member):
        """Kick a member from voice channel"""
        if member.voice is None:
            embed = discord.Embed(
                title="❌ Error",
                description=f"{member.mention} is not in a voice channel",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        await member.move_to(None)
        
        embed = discord.Embed(
            title="🎤 Voice Kicked",
            description=f"{member.mention} has been kicked from voice",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="vcmute")
    @commands.has_permissions(move_members=True)
    async def vcmute(self, ctx, member: discord.Member):
        """Mute a member in voice channel"""
        if member.voice is None:
            embed = discord.Embed(
                title="❌ Error",
                description=f"{member.mention} is not in a voice channel",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        await member.edit(mute=True)
        
        embed = discord.Embed(
            title="🔇 Voice Muted",
            description=f"{member.mention} has been muted in voice",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="vcunmute")
    @commands.has_permissions(move_members=True)
    async def vcunmute(self, ctx, member: discord.Member):
        """Unmute a member in voice channel"""
        if member.voice is None:
            embed = discord.Embed(
                title="❌ Error",
                description=f"{member.mention} is not in a voice channel",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        await member.edit(mute=False)
        
        embed = discord.Embed(
            title="🔊 Voice Unmuted",
            description=f"{member.mention} has been unmuted in voice",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="vcdeafen")
    @commands.has_permissions(move_members=True)
    async def vcdeafen(self, ctx, member: discord.Member):
        """Deafen a member in voice channel"""
        if member.voice is None:
            embed = discord.Embed(
                title="❌ Error",
                description=f"{member.mention} is not in a voice channel",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        await member.edit(deafen=True)
        
        embed = discord.Embed(
            title="🔇 Voice Deafened",
            description=f"{member.mention} has been deafened in voice",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="vcundeafen")
    @commands.has_permissions(move_members=True)
    async def vcundeafen(self, ctx, member: discord.Member):
        """Undeafen a member in voice channel"""
        if member.voice is None:
            embed = discord.Embed(
                title="❌ Error",
                description=f"{member.mention} is not in a voice channel",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        await member.edit(deafen=False)
        
        embed = discord.Embed(
            title="🔊 Voice Undeafened",
            description=f"{member.mention} has been undeafened in voice",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="vckickall")
    @commands.has_permissions(move_members=True)
    async def vckickall(self, ctx):
        """Kick all members from a voice channel"""
        if ctx.author.voice is None:
            embed = discord.Embed(
                title="❌ Error",
                description="You must be in a voice channel",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        channel = ctx.author.voice.channel
        count = 0
        for member in channel.members:
            if member != ctx.author:
                await member.move_to(None)
                count += 1
        
        embed = discord.Embed(
            title="🎤 All Kicked",
            description=f"{count} members have been kicked from voice",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="vcmuteall")
    @commands.has_permissions(move_members=True)
    async def vcmuteall(self, ctx):
        """Mute all members in voice channel"""
        if ctx.author.voice is None:
            embed = discord.Embed(
                title="❌ Error",
                description="You must be in a voice channel",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        channel = ctx.author.voice.channel
        count = 0
        for member in channel.members:
            if member != ctx.author:
                await member.edit(mute=True)
                count += 1
        
        embed = discord.Embed(
            title="🔇 All Muted",
            description=f"{count} members have been muted in voice",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="vcunmuteall")
    @commands.has_permissions(move_members=True)
    async def vcunmuteall(self, ctx):
        """Unmute all members in voice channel"""
        if ctx.author.voice is None:
            embed = discord.Embed(
                title="❌ Error",
                description="You must be in a voice channel",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        channel = ctx.author.voice.channel
        count = 0
        for member in channel.members:
            if member != ctx.author:
                await member.edit(mute=False)
                count += 1
        
        embed = discord.Embed(
            title="🔊 All Unmuted",
            description=f"{count} members have been unmuted in voice",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="vcmove")
    @commands.has_permissions(move_members=True)
    async def vcmove(self, ctx, member: discord.Member, channel: discord.VoiceChannel):
        """Move a member to another voice channel"""
        if member.voice is None:
            embed = discord.Embed(
                title="❌ Error",
                description=f"{member.mention} is not in a voice channel",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        await member.move_to(channel)
        
        embed = discord.Embed(
            title="🎤 Member Moved",
            description=f"{member.mention} has been moved to {channel.mention}",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="vcpull")
    @commands.has_permissions(move_members=True)
    async def vcpull(self, ctx, member: discord.Member):
        """Pull a member to your voice channel"""
        if ctx.author.voice is None:
            embed = discord.Embed(
                title="❌ Error",
                description="You must be in a voice channel",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        if member.voice is None:
            embed = discord.Embed(
                title="❌ Error",
                description=f"{member.mention} is not in a voice channel",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        await member.move_to(ctx.author.voice.channel)
        
        embed = discord.Embed(
            title="🎤 Member Pulled",
            description=f"{member.mention} has been pulled to your voice channel",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(VoiceModCog(bot))
