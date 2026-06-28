import discord
from discord.ext import commands
import json
import os

class StickyNotesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BOT_COLOR = discord.Color(0x000000)
        self.notes_file = "data/stickynotes.json"
        self.load_notes()

    def load_notes(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if os.path.exists(self.notes_file):
            with open(self.notes_file, 'r') as f:
                self.notes = json.load(f)
        else:
            self.notes = {}

    def save_notes(self):
        with open(self.notes_file, 'w') as f:
            json.dump(self.notes, f, indent=2)

    @commands.command(name="stickynote")
    async def stickynote(self, ctx, *, note: str):
        """Create a sticky note"""
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        
        if user_id not in self.notes:
            self.notes[user_id] = {}
        if guild_id not in self.notes[user_id]:
            self.notes[user_id][guild_id] = []
        
        self.notes[user_id][guild_id].append(note)
        self.save_notes()
        
        embed = discord.Embed(
            title="📌 Sticky Note Added",
            description=note,
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="stickynotes")
    async def stickynotes(self, ctx, member: discord.Member = None):
        """View sticky notes"""
        if member is None:
            member = ctx.author
        
        user_id = str(member.id)
        guild_id = str(ctx.guild.id)
        
        if user_id not in self.notes or guild_id not in self.notes[user_id]:
            embed = discord.Embed(
                title="📌 Sticky Notes",
                description=f"{member.mention} has no sticky notes",
                color=self.BOT_COLOR
            )
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(
            title="📌 Sticky Notes",
            color=self.BOT_COLOR
        )
        
        for i, note in enumerate(self.notes[user_id][guild_id], 1):
            embed.add_field(name=f"Note {i}", value=note, inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name="delstickynote")
    async def delstickynote(self, ctx, note_number: int):
        """Delete a sticky note"""
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        
        if user_id not in self.notes or guild_id not in self.notes[user_id]:
            embed = discord.Embed(
                title="❌ Error",
                description="You have no sticky notes",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        if note_number < 1 or note_number > len(self.notes[user_id][guild_id]):
            embed = discord.Embed(
                title="❌ Error",
                description=f"Note {note_number} not found",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        deleted_note = self.notes[user_id][guild_id].pop(note_number - 1)
        self.save_notes()
        
        embed = discord.Embed(
            title="✅ Note Deleted",
            description=deleted_note,
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(StickyNotesCog(bot))
