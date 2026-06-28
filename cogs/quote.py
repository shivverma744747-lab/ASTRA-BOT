import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os

class QuoteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BOT_COLOR = discord.Color(0x000000)

    @commands.command(name="quote")
    async def quote(self, ctx, member: discord.Member = None):
        """Create a quote from a message with member's avatar"""
        if member is None:
            member = ctx.author
        
        if not ctx.message.reference:
            embed = discord.Embed(
                title="❌ Error",
                description="Please reply to a message to create a quote",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        
        try:
            # Get avatar
            avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
            avatar_response = requests.get(avatar_url)
            avatar_image = Image.open(BytesIO(avatar_response.content)).convert('RGBA')
            avatar_image = avatar_image.resize((100, 100))
            
            # Create quote image
            width, height = 800, 400
            image = Image.new('RGB', (width, height), color=(20, 20, 20))
            draw = ImageDraw.Draw(image)
            
            # Try to load a font, fallback to default if not available
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
                small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 25)
            except:
                font = ImageFont.load_default()
                small_font = ImageFont.load_default()
            
            # Paste avatar
            image.paste(avatar_image, (30, 30), avatar_image)
            
            # Draw text
            draw.text((150, 50), member.name, fill=(255, 255, 255), font=small_font)
            
            # Wrap message text
            message_text = replied_message.content
            words = message_text.split()
            lines = []
            current_line = ""
            
            for word in words:
                if len(current_line) + len(word) + 1 > 40:
                    lines.append(current_line)
                    current_line = word
                else:
                    current_line += " " + word if current_line else word
            lines.append(current_line)
            
            y_offset = 150
            for line in lines:
                draw.text((150, y_offset), line, fill=(200, 200, 200), font=font)
                y_offset += 50
            
            # Save and send
            image_bytes = BytesIO()
            image.save(image_bytes, format='PNG')
            image_bytes.seek(0)
            
            file = discord.File(image_bytes, filename="quote.png")
            embed = discord.Embed(
                title="📜 Quote Created",
                color=self.BOT_COLOR
            )
            embed.set_image(url="attachment://quote.png")
            await ctx.send(file=file, embed=embed)
        
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Failed to create quote: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
    
    @commands.tree.command(name="quote", description="Create a quote from a message")
    async def quote_slash(self, interaction: discord.Interaction, member: discord.Member = None):
        """Slash command version of quote"""
        await interaction.response.defer()
        
        if member is None:
            member = interaction.user
        
        try:
            # Get avatar
            avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
            avatar_response = requests.get(avatar_url)
            avatar_image = Image.open(BytesIO(avatar_response.content)).convert('RGBA')
            avatar_image = avatar_image.resize((100, 100))
            
            # Create quote image
            width, height = 800, 400
            image = Image.new('RGB', (width, height), color=(20, 20, 20))
            draw = ImageDraw.Draw(image)
            
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
                small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 25)
            except:
                font = ImageFont.load_default()
                small_font = ImageFont.load_default()
            
            image.paste(avatar_image, (30, 30), avatar_image)
            draw.text((150, 50), member.name, fill=(255, 255, 255), font=small_font)
            draw.text((150, 150), "Quote created via slash command", fill=(200, 200, 200), font=font)
            
            image_bytes = BytesIO()
            image.save(image_bytes, format='PNG')
            image_bytes.seek(0)
            
            file = discord.File(image_bytes, filename="quote.png")
            embed = discord.Embed(
                title="📜 Quote Created",
                color=self.BOT_COLOR
            )
            embed.set_image(url="attachment://quote.png")
            await interaction.followup.send(file=file, embed=embed)
        
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Failed to create quote: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(QuoteCog(bot))
