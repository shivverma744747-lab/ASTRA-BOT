import discord
from discord.ext import commands
import json
import os

class VerificationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BOT_COLOR = discord.Color(0x000000)
        self.verify_file = "data/verify.json"
        self.load_verify()

    def load_verify(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if os.path.exists(self.verify_file):
            with open(self.verify_file, 'r') as f:
                self.verify = json.load(f)
        else:
            self.verify = {}

    def save_verify(self):
        with open(self.verify_file, 'w') as f:
            json.dump(self.verify, f, indent=2)

    @commands.command(name="setupverify")
    @commands.has_permissions(manage_guild=True)
    async def setupverify(self, ctx, channel: discord.TextChannel, role: discord.Role):
        """Setup verification system"""
        guild_id = str(ctx.guild.id)
        
        if guild_id not in self.verify:
            self.verify[guild_id] = {}
        
        self.verify[guild_id]["channel_id"] = channel.id
        self.verify[guild_id]["role_id"] = role.id
        self.save_verify()
        
        embed = discord.Embed(
            title="✅ Verification Setup",
            description=f"Channel: {channel.mention}\nRole: {role.mention}",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)
        
        # Send verification message
        verify_embed = discord.Embed(
            title="✅ Verification Required",
            description="React with ✅ to verify and gain access to the server",
            color=self.BOT_COLOR
        )
        message = await channel.send(embed=verify_embed)
        await message.add_reaction("✅")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            return
        
        guild_id = str(payload.guild_id)
        if guild_id not in self.verify:
            return
        
        if payload.channel_id != self.verify[guild_id]["channel_id"]:
            return
        
        if str(payload.emoji) != "✅":
            return
        
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role_id = self.verify[guild_id]["role_id"]
        role = guild.get_role(role_id)
        
        if member and role:
            await member.add_roles(role)

    @commands.command(name="verify")
    async def verify(self, ctx):
        """Verify yourself"""
        guild_id = str(ctx.guild.id)
        
        if guild_id not in self.verify:
            embed = discord.Embed(
                title="❌ Error",
                description="Verification not setup in this server",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        role_id = self.verify[guild_id]["role_id"]
        role = ctx.guild.get_role(role_id)
        
        if role:
            await ctx.author.add_roles(role)
            embed = discord.Embed(
                title="✅ Verified",
                description=f"You have been given {role.mention}",
                color=self.BOT_COLOR
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(VerificationCog(bot))
