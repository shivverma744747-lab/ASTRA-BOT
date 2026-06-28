import discord
from discord.ext import commands
import json
import os
from datetime import datetime

class TicketCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BOT_COLOR = discord.Color(0x000000)
        self.tickets_file = "data/tickets.json"
        self.load_tickets()

    def load_tickets(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if os.path.exists(self.tickets_file):
            with open(self.tickets_file, 'r') as f:
                self.tickets = json.load(f)
        else:
            self.tickets = {}

    def save_tickets(self):
        with open(self.tickets_file, 'w') as f:
            json.dump(self.tickets, f, indent=2)

    @commands.command(name="ticket")
    async def ticket(self, ctx, *, reason: str = "No reason provided"):
        """Create a support ticket"""
        guild = ctx.guild
        user = ctx.author
        
        # Create ticket channel
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        channel = await guild.create_text_channel(f"ticket-{user.name}", overwrites=overwrites)
        
        # Save ticket info
        ticket_id = str(channel.id)
        self.tickets[ticket_id] = {
            "user_id": user.id,
            "channel_id": channel.id,
            "reason": reason,
            "created_at": datetime.now().isoformat(),
            "messages": []
        }
        self.save_tickets()
        
        embed = discord.Embed(
            title="🎫 Ticket Created",
            description=f"**Reason:** {reason}",
            color=self.BOT_COLOR
        )
        embed.add_field(name="Channel", value=channel.mention, inline=False)
        
        await channel.send(embed=embed)
        
        embed2 = discord.Embed(
            title="✅ Ticket Created",
            description=f"Your ticket has been created: {channel.mention}",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed2)

    @commands.command(name="close_ticket")
    async def close_ticket(self, ctx):
        """Close a ticket"""
        ticket_id = str(ctx.channel.id)
        
        if ticket_id not in self.tickets:
            embed = discord.Embed(
                title="❌ Error",
                description="This is not a ticket channel",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        # Create transcript
        transcript = await self.create_transcript(ctx.channel)
        
        # Save transcript
        transcripts_dir = "data/transcripts"
        if not os.path.exists(transcripts_dir):
            os.makedirs(transcripts_dir)
        
        with open(f"{transcripts_dir}/{ticket_id}.txt", 'w') as f:
            f.write(transcript)
        
        embed = discord.Embed(
            title="🎫 Ticket Closed",
            description="Transcript has been saved",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)
        
        # Delete ticket data
        del self.tickets[ticket_id]
        self.save_tickets()
        
        # Delete channel after 5 seconds
        await asyncio.sleep(5)
        await ctx.channel.delete()

    async def create_transcript(self, channel):
        """Create a transcript of the ticket channel"""
        transcript = f"Ticket Transcript - {channel.name}\n"
        transcript += f"Created at: {datetime.now().isoformat()}\n"
        transcript += "="*50 + "\n\n"
        
        async for message in channel.history(oldest_first=True):
            transcript += f"{message.author}: {message.content}\n"
        
        return transcript

    @commands.command(name="transcript")
    async def transcript(self, ctx, channel: discord.TextChannel = None):
        """Get transcript of a ticket"""
        if channel is None:
            channel = ctx.channel
        
        ticket_id = str(channel.id)
        transcripts_dir = "data/transcripts"
        
        if os.path.exists(f"{transcripts_dir}/{ticket_id}.txt"):
            with open(f"{transcripts_dir}/{ticket_id}.txt", 'r') as f:
                transcript = f.read()
            
            file = discord.File(fp=io.StringIO(transcript), filename=f"{ticket_id}.txt")
            await ctx.send(file=file)
        else:
            embed = discord.Embed(
                title="❌ Error",
                description="No transcript found",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

import asyncio
import io

async def setup(bot):
    await bot.add_cog(TicketCog(bot))
