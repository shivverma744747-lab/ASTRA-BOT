import discord
from discord.ext import commands, tasks
import asyncio
import json
import os
from datetime import datetime, timedelta

class GiveawayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BOT_COLOR = discord.Color(0x000000)
        self.giveaways_file = "data/giveaways.json"
        self.load_giveaways()
        self.check_giveaways.start()

    def load_giveaways(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if os.path.exists(self.giveaways_file):
            with open(self.giveaways_file, 'r') as f:
                self.giveaways = json.load(f)
        else:
            self.giveaways = {}

    def save_giveaways(self):
        with open(self.giveaways_file, 'w') as f:
            json.dump(self.giveaways, f, indent=2)

    @tasks.loop(minutes=1)
    async def check_giveaways(self):
        """Check and end expired giveaways"""
        now = datetime.now().timestamp()
        ended = []
        
        for giveaway_id, giveaway in self.giveaways.items():
            if giveaway['end_time'] <= now and not giveaway['ended']:
                await self.end_giveaway(giveaway_id)
                ended.append(giveaway_id)
        
        for giveaway_id in ended:
            del self.giveaways[giveaway_id]
            self.save_giveaways()

    async def end_giveaway(self, giveaway_id):
        """End a giveaway and pick a winner"""
        giveaway = self.giveaways[giveaway_id]
        
        try:
            channel = self.bot.get_channel(giveaway['channel_id'])
            message = await channel.fetch_message(giveaway['message_id'])
            
            # Get all reactions
            reactions = [reaction for reaction in message.reactions if str(reaction.emoji) == "🎉"]
            
            if reactions:
                users = await reactions[0].users().flatten()
                users = [u for u in users if not u.bot]
                
                if users:
                    winner = discord.utils.random.choice(users)
                    embed = discord.Embed(
                        title="🎉 Giveaway Ended!",
                        description=f"Prize: {giveaway['prize']}\nWinner: {winner.mention}",
                        color=self.BOT_COLOR
                    )
                    await channel.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="🎉 Giveaway Ended",
                        description=f"Prize: {giveaway['prize']}\nNo valid participants!",
                        color=self.BOT_COLOR
                    )
                    await channel.send(embed=embed)
            
            giveaway['ended'] = True
            self.save_giveaways()
        except Exception as e:
            print(f"Error ending giveaway: {e}")

    @commands.command(name="giveaway")
    @commands.has_permissions(manage_guild=True)
    async def giveaway(self, ctx, duration: str, *, prize: str):
        """Start a giveaway (e.g., &giveaway 1h Nitro)"""
        try:
            # Parse duration
            multipliers = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
            amount = int(duration[:-1])
            unit = duration[-1].lower()
            
            if unit not in multipliers:
                raise ValueError
            
            duration_seconds = amount * multipliers[unit]
            end_time = (datetime.now() + timedelta(seconds=duration_seconds)).timestamp()
            
            # Create giveaway message
            embed = discord.Embed(
                title="🎉 Giveaway!",
                description=f"Prize: **{prize}**\nReact with 🎉 to participate!",
                color=self.BOT_COLOR
            )
            embed.add_field(name="Duration", value=duration, inline=True)
            embed.add_field(name="Ends at", value=f"<t:{int(end_time)}:R>", inline=True)
            
            message = await ctx.send(embed=embed)
            await message.add_reaction("🎉")
            
            # Save giveaway
            giveaway_id = str(message.id)
            self.giveaways[giveaway_id] = {
                'channel_id': ctx.channel.id,
                'message_id': message.id,
                'prize': prize,
                'end_time': end_time,
                'ended': False
            }
            self.save_giveaways()
        
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Invalid format. Use: &giveaway 1h Prize",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.command(name="giveaway_end")
    @commands.has_permissions(manage_guild=True)
    async def giveaway_end(self, ctx, message_id: int):
        """End a giveaway early"""
        giveaway_id = str(message_id)
        
        if giveaway_id not in self.giveaways:
            embed = discord.Embed(
                title="❌ Error",
                description="Giveaway not found",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        await self.end_giveaway(giveaway_id)
        del self.giveaways[giveaway_id]
        self.save_giveaways()
        
        embed = discord.Embed(
            title="✅ Giveaway Ended",
            description="Giveaway has been ended early",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @check_giveaways.before_loop
    async def before_check_giveaways(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(GiveawayCog(bot))
