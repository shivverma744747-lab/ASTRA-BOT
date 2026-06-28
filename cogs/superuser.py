import discord
from discord.ext import commands

class SuperuserCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BOT_COLOR = discord.Color(0x000000)
        self.OWNER_ID = 1427675629351866398

    @commands.command(name="addsuperuser")
    async def addsuperuser(self, ctx, member: discord.Member):
        """Add a superuser (Owner only)"""
        if ctx.author.id != self.OWNER_ID:
            embed = discord.Embed(
                title="❌ Owner Only",
                description="Only bot owner can use this command",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        if member.id in self.bot.superusers:
            embed = discord.Embed(
                title="⚠️ Already Superuser",
                description=f"{member.mention} is already a superuser",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            return
        
        self.bot.superusers.add(member.id)
        
        embed = discord.Embed(
            title="✅ Superuser Added",
            description=f"{member.mention} has been added as a superuser",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="removesuperuser")
    async def removesuperuser(self, ctx, member: discord.Member):
        """Remove a superuser (Owner only)"""
        if ctx.author.id != self.OWNER_ID:
            embed = discord.Embed(
                title="❌ Owner Only",
                description="Only bot owner can use this command",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        if member.id not in self.bot.superusers:
            embed = discord.Embed(
                title="⚠️ Not a Superuser",
                description=f"{member.mention} is not a superuser",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            return
        
        self.bot.superusers.discard(member.id)
        
        embed = discord.Embed(
            title="✅ Superuser Removed",
            description=f"{member.mention} has been removed as a superuser",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="listsuperusers")
    async def listsuperusers(self, ctx):
        """List all superusers (Owner only)"""
        if ctx.author.id != self.OWNER_ID:
            embed = discord.Embed(
                title="❌ Owner Only",
                description="Only bot owner can use this command",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        if not self.bot.superusers:
            embed = discord.Embed(
                title="👑 Superusers",
                description="No superusers have been added yet",
                color=self.BOT_COLOR
            )
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(
            title="👑 Superusers",
            color=self.BOT_COLOR
        )
        
        for user_id in self.bot.superusers:
            try:
                user = await self.bot.fetch_user(user_id)
                embed.add_field(name=user.name, value=f"ID: {user_id}", inline=False)
            except:
                embed.add_field(name="Unknown User", value=f"ID: {user_id}", inline=False)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(SuperuserCog(bot))
