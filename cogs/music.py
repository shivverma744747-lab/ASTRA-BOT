import discord
from discord.ext import commands
import asyncio

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BOT_COLOR = discord.Color(0x000000)
        self.queue = {}
        self.playing = {}

    def get_queue(self, guild_id):
        if guild_id not in self.queue:
            self.queue[guild_id] = []
        return self.queue[guild_id]

    @commands.command(name="play")
    async def play(self, ctx, *, song: str):
        """Play a song"""
        if ctx.author.voice is None:
            embed = discord.Embed(
                title="❌ Error",
                description="You must be in a voice channel",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        guild_id = ctx.guild.id
        queue = self.get_queue(guild_id)
        queue.append(song)
        
        embed = discord.Embed(
            title="🎵 Added to Queue",
            description=f"Song: {song}",
            color=self.BOT_COLOR
        )
        embed.add_field(name="Position", value=f"#{len(queue)}", inline=True)
        await ctx.send(embed=embed)

    @commands.command(name="pause")
    async def pause(self, ctx):
        """Pause music"""
        guild_id = ctx.guild.id
        self.playing[guild_id] = False
        
        embed = discord.Embed(
            title="⏸️ Music Paused",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="resume")
    async def resume(self, ctx):
        """Resume music"""
        guild_id = ctx.guild.id
        self.playing[guild_id] = True
        
        embed = discord.Embed(
            title="🔊 Music Resumed",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="stop")
    async def stop(self, ctx):
        """Stop music"""
        guild_id = ctx.guild.id
        self.queue[guild_id] = []
        self.playing[guild_id] = False
        
        embed = discord.Embed(
            title="🛑 Music Stopped",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="queue")
    async def queue(self, ctx):
        """View music queue"""
        guild_id = ctx.guild.id
        queue = self.get_queue(guild_id)
        
        if not queue:
            embed = discord.Embed(
                title="🎵 Queue",
                description="Queue is empty",
                color=self.BOT_COLOR
            )
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(
            title="🎵 Queue",
            color=self.BOT_COLOR
        )
        
        for i, song in enumerate(queue[:10], 1):
            embed.add_field(name=f"#{i}", value=song, inline=False)
        
        if len(queue) > 10:
            embed.add_field(name="...", value=f"And {len(queue) - 10} more songs", inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name="skip")
    async def skip(self, ctx):
        """Skip current song"""
        guild_id = ctx.guild.id
        queue = self.get_queue(guild_id)
        
        if queue:
            queue.pop(0)
            embed = discord.Embed(
                title="⏭️ Skipped",
                description="Song skipped",
                color=self.BOT_COLOR
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Error",
                description="Queue is empty",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(MusicCog(bot))
