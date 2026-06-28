import discord
from discord.ext import commands
import json
import os

class BoostCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BOT_COLOR = discord.Color(0x000000)
        self.boosts_file = "data/boosts.json"
        self.load_boosts()

    def load_boosts(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if os.path.exists(self.boosts_file):
            with open(self.boosts_file, 'r') as f:
                self.boosts = json.load(f)
        else:
            self.boosts = {}

    def save_boosts(self):
        with open(self.boosts_file, 'w') as f:
            json.dump(self.boosts, f, indent=2)

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        if before.premium_subscription_count < after.premium_subscription_count:
            guild_id = str(after.id)
            
            if guild_id in self.boosts and "channel_id" in self.boosts[guild_id]:
                channel = after.get_channel(self.boosts[guild_id]["channel_id"])
                if channel:
                    message = self.boosts[guild_id].get("message", "{server} just got boosted! 🚀")
                    message = message.replace("{server}", after.name).replace("{count}", str(after.premium_subscription_count))
                    
                    embed = discord.Embed(
                        title="⭐ Server Boosted!",
                        description=message,
                        color=self.BOT_COLOR
                    )
                    await channel.send(embed=embed)

    @commands.command(name="setboost")
    @commands.has_permissions(manage_guild=True)
    async def setboost(self, ctx, channel: discord.TextChannel, *, message: str = "{server} just got boosted! 🚀"):
        """Set boost message"""
        guild_id = str(ctx.guild.id)
        
        if guild_id not in self.boosts:
            self.boosts[guild_id] = {}
        
        self.boosts[guild_id]["channel_id"] = channel.id
        self.boosts[guild_id]["message"] = message
        self.save_boosts()
        
        embed = discord.Embed(
            title="✅ Boost Message Set",
            description=f"Channel: {channel.mention}\nMessage: {message}",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(BoostCog(bot))
