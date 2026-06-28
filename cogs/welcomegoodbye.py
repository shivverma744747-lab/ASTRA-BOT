import discord
from discord.ext import commands
import json
import os

class WelcomeGoodbyeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BOT_COLOR = discord.Color(0x000000)
        self.messages_file = "data/welcomegoodbye.json"
        self.load_messages()

    def load_messages(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if os.path.exists(self.messages_file):
            with open(self.messages_file, 'r') as f:
                self.messages = json.load(f)
        else:
            self.messages = {}

    def save_messages(self):
        with open(self.messages_file, 'w') as f:
            json.dump(self.messages, f, indent=2)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = str(member.guild.id)
        if guild_id in self.messages and "welcome" in self.messages[guild_id]:
            channel_id = self.messages[guild_id]["welcome"]["channel_id"]
            message = self.messages[guild_id]["welcome"]["message"]
            
            channel = member.guild.get_channel(channel_id)
            if channel:
                message = message.replace("{user}", member.mention).replace("{server}", member.guild.name)
                embed = discord.Embed(
                    title="👋 Welcome!",
                    description=message,
                    color=self.BOT_COLOR
                )
                embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild_id = str(member.guild.id)
        if guild_id in self.messages and "goodbye" in self.messages[guild_id]:
            channel_id = self.messages[guild_id]["goodbye"]["channel_id"]
            message = self.messages[guild_id]["goodbye"]["message"]
            
            channel = member.guild.get_channel(channel_id)
            if channel:
                message = message.replace("{user}", member.name).replace("{server}", member.guild.name)
                embed = discord.Embed(
                    title="👋 Goodbye!",
                    description=message,
                    color=self.BOT_COLOR
                )
                await channel.send(embed=embed)

    @commands.command(name="setwelcome")
    @commands.has_permissions(manage_guild=True)
    async def setwelcome(self, ctx, channel: discord.TextChannel, *, message: str):
        """Set welcome message"""
        guild_id = str(ctx.guild.id)
        
        if guild_id not in self.messages:
            self.messages[guild_id] = {}
        
        self.messages[guild_id]["welcome"] = {
            "channel_id": channel.id,
            "message": message
        }
        self.save_messages()
        
        embed = discord.Embed(
            title="✅ Welcome Message Set",
            description=f"Channel: {channel.mention}\nMessage: {message}",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="setgoodbye")
    @commands.has_permissions(manage_guild=True)
    async def setgoodbye(self, ctx, channel: discord.TextChannel, *, message: str):
        """Set goodbye message"""
        guild_id = str(ctx.guild.id)
        
        if guild_id not in self.messages:
            self.messages[guild_id] = {}
        
        self.messages[guild_id]["goodbye"] = {
            "channel_id": channel.id,
            "message": message
        }
        self.save_messages()
        
        embed = discord.Embed(
            title="✅ Goodbye Message Set",
            description=f"Channel: {channel.mention}\nMessage: {message}",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(WelcomeGoodbyeCog(bot))
