import discord
from discord.ext import commands
import json
import os
import re

class AutoresponderCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BOT_COLOR = discord.Color(0x000000)
        self.responders_file = "data/autoresponders.json"
        self.load_responders()

    def load_responders(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if os.path.exists(self.responders_file):
            with open(self.responders_file, 'r') as f:
                self.responders = json.load(f)
        else:
            self.responders = {}

    def save_responders(self):
        with open(self.responders_file, 'w') as f:
            json.dump(self.responders, f, indent=2)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return
        
        guild_id = str(message.guild.id)
        if guild_id not in self.responders:
            return
        
        for trigger, response in self.responders[guild_id].items():
            if re.search(trigger, message.content, re.IGNORECASE):
                await message.channel.send(response)
                break

    @commands.command(name="autoresponder")
    @commands.has_permissions(manage_messages=True)
    async def autoresponder(self, ctx, *, trigger_and_response: str):
        """Add autoresponder (format: trigger | response)"""
        try:
            trigger, response = trigger_and_response.split(" | ", 1)
        except ValueError:
            embed = discord.Embed(
                title="❌ Error",
                description="Format: trigger | response",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        guild_id = str(ctx.guild.id)
        if guild_id not in self.responders:
            self.responders[guild_id] = {}
        
        self.responders[guild_id][trigger] = response
        self.save_responders()
        
        embed = discord.Embed(
            title="✅ Autoresponder Added",
            description=f"Trigger: {trigger}\nResponse: {response}",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="removeresponder")
    @commands.has_permissions(manage_messages=True)
    async def removeresponder(self, ctx, *, trigger: str):
        """Remove an autoresponder"""
        guild_id = str(ctx.guild.id)
        
        if guild_id not in self.responders or trigger not in self.responders[guild_id]:
            embed = discord.Embed(
                title="❌ Error",
                description="Autoresponder not found",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        del self.responders[guild_id][trigger]
        self.save_responders()
        
        embed = discord.Embed(
            title="✅ Autoresponder Removed",
            description=f"Trigger: {trigger}",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="listresponders")
    async def listresponders(self, ctx):
        """List all autoresponders"""
        guild_id = str(ctx.guild.id)
        
        if guild_id not in self.responders or not self.responders[guild_id]:
            embed = discord.Embed(
                title="🗒️ Autoresponders",
                description="No autoresponders set",
                color=self.BOT_COLOR
            )
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(
            title="🗒️ Autoresponders",
            color=self.BOT_COLOR
        )
        
        for i, (trigger, response) in enumerate(self.responders[guild_id].items(), 1):
            embed.add_field(name=f"#{i} Trigger", value=trigger, inline=False)
            embed.add_field(name="Response", value=response, inline=False)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AutoresponderCog(bot))
