import discord
from discord.ext import commands
import json
import os

class ServerProfileCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BOT_COLOR = discord.Color(0x000000)
        self.profiles_file = "data/serverprofiles.json"
        self.load_profiles()

    def load_profiles(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if os.path.exists(self.profiles_file):
            with open(self.profiles_file, 'r') as f:
                self.profiles = json.load(f)
        else:
            self.profiles = {}

    def save_profiles(self):
        with open(self.profiles_file, 'w') as f:
            json.dump(self.profiles, f, indent=2)

    @commands.command(name="avatar")
    async def avatar(self, ctx, server_id: int = None, image_url: str = None):
        """Set or get server avatar"""
        if server_id is None:
            server_id = ctx.guild.id
        
        server_id_str = str(server_id)
        
        if server_id_str not in self.profiles:
            self.profiles[server_id_str] = {}
        
        if image_url:
            if ctx.author.id != 1427675629351866398:
                embed = discord.Embed(
                    title="❌ Owner Only",
                    description="Only bot owner can set server profile",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
            
            self.profiles[server_id_str]["avatar"] = image_url
            self.save_profiles()
            
            embed = discord.Embed(
                title="✅ Avatar Set",
                description="Server avatar has been set",
                color=self.BOT_COLOR
            )
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
        else:
            if "avatar" in self.profiles[server_id_str]:
                embed = discord.Embed(
                    title="🖼️ Server Avatar",
                    color=self.BOT_COLOR
                )
                embed.set_image(url=self.profiles[server_id_str]["avatar"])
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="❌ Error",
                    description="No avatar set for this server",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)

    @commands.command(name="serverbanner")
    async def serverbanner(self, ctx, server_id: int = None, image_url: str = None):
        """Set or get server banner"""
        if server_id is None:
            server_id = ctx.guild.id
        
        server_id_str = str(server_id)
        
        if server_id_str not in self.profiles:
            self.profiles[server_id_str] = {}
        
        if image_url:
            if ctx.author.id != 1427675629351866398:
                embed = discord.Embed(
                    title="❌ Owner Only",
                    description="Only bot owner can set server profile",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
            
            self.profiles[server_id_str]["banner"] = image_url
            self.save_profiles()
            
            embed = discord.Embed(
                title="✅ Banner Set",
                description="Server banner has been set",
                color=self.BOT_COLOR
            )
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
        else:
            if "banner" in self.profiles[server_id_str]:
                embed = discord.Embed(
                    title="🖼️ Server Banner",
                    color=self.BOT_COLOR
                )
                embed.set_image(url=self.profiles[server_id_str]["banner"])
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="❌ Error",
                    description="No banner set for this server",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)

    @commands.command(name="bioserver")
    async def bioserver(self, ctx, server_id: int = None, *, bio: str = None):
        """Set or get server bio"""
        if server_id is None:
            server_id = ctx.guild.id
        
        server_id_str = str(server_id)
        
        if server_id_str not in self.profiles:
            self.profiles[server_id_str] = {}
        
        if bio:
            if ctx.author.id != 1427675629351866398:
                embed = discord.Embed(
                    title="❌ Owner Only",
                    description="Only bot owner can set server profile",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
            
            self.profiles[server_id_str]["bio"] = bio
            self.save_profiles()
            
            embed = discord.Embed(
                title="✅ Bio Set",
                description=bio,
                color=self.BOT_COLOR
            )
            await ctx.send(embed=embed)
        else:
            if "bio" in self.profiles[server_id_str]:
                embed = discord.Embed(
                    title="📝 Server Bio",
                    description=self.profiles[server_id_str]["bio"],
                    color=self.BOT_COLOR
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="❌ Error",
                    description="No bio set for this server",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)

    @commands.command(name="nameserver")
    async def nameserver(self, ctx, server_id: int = None, *, name: str = None):
        """Set or get server name"""
        if server_id is None:
            server_id = ctx.guild.id
        
        server_id_str = str(server_id)
        
        if server_id_str not in self.profiles:
            self.profiles[server_id_str] = {}
        
        if name:
            if ctx.author.id != 1427675629351866398:
                embed = discord.Embed(
                    title="❌ Owner Only",
                    description="Only bot owner can set server profile",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
            
            self.profiles[server_id_str]["name"] = name
            self.save_profiles()
            
            embed = discord.Embed(
                title="✅ Name Set",
                description=name,
                color=self.BOT_COLOR
            )
            await ctx.send(embed=embed)
        else:
            if "name" in self.profiles[server_id_str]:
                embed = discord.Embed(
                    title="📝 Server Name",
                    description=self.profiles[server_id_str]["name"],
                    color=self.BOT_COLOR
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="❌ Error",
                    description="No custom name set for this server",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ServerProfileCog(bot))
