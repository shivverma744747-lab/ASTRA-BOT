import discord
from discord.ext import commands
import json
import os

class LevelingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BOT_COLOR = discord.Color(0x000000)
        self.levels_file = "data/levels.json"
        self.load_levels()

    def load_levels(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if os.path.exists(self.levels_file):
            with open(self.levels_file, 'r') as f:
                self.levels = json.load(f)
        else:
            self.levels = {}

    def save_levels(self):
        with open(self.levels_file, 'w') as f:
            json.dump(self.levels, f, indent=2)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return
        
        user_id = str(message.author.id)
        guild_id = str(message.guild.id)
        
        if user_id not in self.levels:
            self.levels[user_id] = {}
        if guild_id not in self.levels[user_id]:
            self.levels[user_id][guild_id] = {"xp": 0, "level": 1}
        
        # Add XP
        xp_gain = len(message.content) // 5
        if xp_gain > 0:
            self.levels[user_id][guild_id]["xp"] += xp_gain
            
            # Check level up
            xp_needed = self.levels[user_id][guild_id]["level"] * 100
            if self.levels[user_id][guild_id]["xp"] >= xp_needed:
                self.levels[user_id][guild_id]["level"] += 1
                self.levels[user_id][guild_id]["xp"] = 0
                
                embed = discord.Embed(
                    title="⬆️ Level Up!",
                    description=f"{message.author.mention} reached level {self.levels[user_id][guild_id]['level']}",
                    color=self.BOT_COLOR
                )
                await message.channel.send(embed=embed)
            
            self.save_levels()

    @commands.command(name="level")
    async def level(self, ctx, member: discord.Member = None):
        """Check your level"""
        if member is None:
            member = ctx.author
        
        user_id = str(member.id)
        guild_id = str(ctx.guild.id)
        
        if user_id not in self.levels or guild_id not in self.levels[user_id]:
            embed = discord.Embed(
                title="📊 Level",
                description=f"{member.mention} has not sent any messages yet",
                color=self.BOT_COLOR
            )
            await ctx.send(embed=embed)
            return
        
        level_data = self.levels[user_id][guild_id]
        xp_needed = level_data["level"] * 100
        
        embed = discord.Embed(
            title="📊 Level",
            color=self.BOT_COLOR
        )
        embed.add_field(name="Member", value=member.mention, inline=False)
        embed.add_field(name="Level", value=level_data["level"], inline=True)
        embed.add_field(name="XP", value=f"{level_data['xp']}/{xp_needed}", inline=True)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="leaderboard")
    async def leaderboard(self, ctx):
        """Show level leaderboard"""
        guild_id = str(ctx.guild.id)
        leaderboard = []
        
        for user_id, user_data in self.levels.items():
            if guild_id in user_data:
                leaderboard.append((int(user_id), user_data[guild_id]["level"]))
        
        leaderboard.sort(key=lambda x: x[1], reverse=True)
        leaderboard = leaderboard[:10]
        
        embed = discord.Embed(
            title="🏆 Level Leaderboard",
            color=self.BOT_COLOR
        )
        
        description = ""
        for i, (user_id, level) in enumerate(leaderboard, 1):
            user = await self.bot.fetch_user(user_id)
            description += f"{i}. {user.mention} - Level {level}\n"
        
        embed.description = description
        await ctx.send(embed=embed)

    @commands.command(name="setlevel")
    @commands.has_permissions(manage_guild=True)
    async def setlevel(self, ctx, member: discord.Member, level: int):
        """Set a member's level (Owner only)"""
        if ctx.author.id != 1427675629351866398:
            embed = discord.Embed(
                title="❌ Owner Only",
                description="Only bot owner can use this command",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        user_id = str(member.id)
        guild_id = str(ctx.guild.id)
        
        if user_id not in self.levels:
            self.levels[user_id] = {}
        if guild_id not in self.levels[user_id]:
            self.levels[user_id][guild_id] = {"xp": 0, "level": 1}
        
        self.levels[user_id][guild_id]["level"] = level
        self.save_levels()
        
        embed = discord.Embed(
            title="✅ Level Set",
            description=f"{member.mention}'s level set to {level}",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="resetlevel")
    @commands.has_permissions(manage_guild=True)
    async def resetlevel(self, ctx, member: discord.Member):
        """Reset a member's level"""
        if ctx.author.id != 1427675629351866398:
            embed = discord.Embed(
                title="❌ Owner Only",
                description="Only bot owner can use this command",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        user_id = str(member.id)
        guild_id = str(ctx.guild.id)
        
        if user_id in self.levels and guild_id in self.levels[user_id]:
            self.levels[user_id][guild_id] = {"xp": 0, "level": 1}
            self.save_levels()
            
            embed = discord.Embed(
                title="✅ Level Reset",
                description=f"{member.mention}'s level has been reset",
                color=self.BOT_COLOR
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(LevelingCog(bot))
