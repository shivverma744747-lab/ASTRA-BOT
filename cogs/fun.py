import discord
from discord.ext import commands
import random
import aiohttp

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BOT_COLOR = discord.Color(0x000000)

    @commands.command(name="joke")
    async def joke(self, ctx):
        """Get a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "What do you call a fake noodle? An impasta!",
            "Why did the cookie go to the doctor? Because it felt crumbly!"
        ]
        
        joke = random.choice(jokes)
        embed = discord.Embed(
            title="😂 Joke",
            description=joke,
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="meme")
    async def meme(self, ctx):
        """Get a random meme"""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://meme-api.com/gimme') as resp:
                data = await resp.json()
                
                embed = discord.Embed(
                    title="🎉 Meme",
                    color=self.BOT_COLOR
                )
                embed.set_image(url=data['url'])
                embed.add_field(name="Subreddit", value=data['subreddit'], inline=True)
                embed.add_field(name="Upvotes", value=data['ups'], inline=True)
                
                await ctx.send(embed=embed)

    @commands.command(name="8ball")
    async def eightball(self, ctx, *, question: str):
        """Ask the magic 8 ball a question"""
        responses = [
            "Yes, definitely!",
            "No, not at all!",
            "Maybe... ask again later",
            "Absolutely!",
            "I'm not sure",
            "Very likely!",
            "Unlikely",
            "Signs point to yes",
            "Ask again later",
            "Don't count on it"
        ]
        
        response = random.choice(responses)
        embed = discord.Embed(
            title="🎱 Magic 8 Ball",
            description=f"Q: {question}\nA: {response}",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name="rate")
    async def rate(self, ctx, *, thing: str):
        """Rate something"""
        rating = random.randint(1, 10)
        stars = "⭐" * rating
        
        embed = discord.Embed(
            title="⭐ Rating",
            description=f"{thing}: {rating}/10\n{stars}",
            color=self.BOT_COLOR
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(FunCog(bot))
