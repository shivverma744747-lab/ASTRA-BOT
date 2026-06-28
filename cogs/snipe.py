import discord
from discord.ext import commands
import json
import os

class SnipeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BOT_COLOR = discord.Color(0x000000)
        self.snipes = {}
        self.editsnipes = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        
        channel_id = message.channel.id
        self.snipes[channel_id] = {
            "author": message.author,
            "content": message.content,
            "timestamp": message.created_at
        }

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return
        
        channel_id = before.channel.id
        self.editsnipes[channel_id] = {
            "author": before.author,
            "before": before.content,
            "after": after.content,
            "timestamp": before.created_at
        }

    @commands.command(name="snipe")
    async def snipe(self, ctx):
        """Snipe the last deleted message"""
        channel_id = ctx.channel.id
        
        if channel_id not in self.snipes:
            embed = discord.Embed(
                title="❌ Error",
                description="No deleted messages to snipe",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        snipe = self.snipes[channel_id]
        embed = discord.Embed(
            title="🔍 Sniped Message",
            description=snipe["content"],
            color=self.BOT_COLOR
        )
        embed.set_author(name=snipe["author"].name, icon_url=snipe["author"].avatar.url if snipe["author"].avatar else snipe["author"].default_avatar.url)
        embed.set_footer(text=f"Deleted at {snipe['timestamp']}")
        await ctx.send(embed=embed)

    @commands.command(name="editsnipe")
    async def editsnipe(self, ctx):
        """Snipe the last edited message"""
        channel_id = ctx.channel.id
        
        if channel_id not in self.editsnipes:
            embed = discord.Embed(
                title="❌ Error",
                description="No edited messages to snipe",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        snipe = self.editsnipes[channel_id]
        embed = discord.Embed(
            title="🔍 Edit Sniped Message",
            color=self.BOT_COLOR
        )
        embed.add_field(name="Before", value=snipe["before"], inline=False)
        embed.add_field(name="After", value=snipe["after"], inline=False)
        embed.set_author(name=snipe["author"].name, icon_url=snipe["author"].avatar.url if snipe["author"].avatar else snipe["author"].default_avatar.url)
        embed.set_footer(text=f"Edited at {snipe['timestamp']}")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(SnipeCog(bot))
