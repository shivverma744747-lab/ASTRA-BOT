import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import sys

load_dotenv()

# Bot Configuration
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True
intents.guilds = True
intents.reactions = True
intents.presences = True

bot = commands.Bot(command_prefix="&", intents=intents, help_command=None)

OWNER_ID = 1427675629351866398
BOT_COLOR = discord.Color(0x000000)  # Black color for embeds

# Store superusers and bot data
bot.superusers = set()
bot.bot_data = {}

# Load cogs
async def load_cogs():
    cogs_dir = "cogs"
    if not os.path.exists(cogs_dir):
        os.makedirs(cogs_dir)
    
    for filename in os.listdir(cogs_dir):
        if filename.endswith(".py") and not filename.startswith("_"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"✅ Loaded cog: {filename}")
            except Exception as e:
                print(f"❌ Failed to load {filename}: {e}")

@bot.event
async def on_ready():
    print(f"\n✅ Bot logged in as {bot.user}")
    print(f"📊 Serving {len(bot.guilds)} guilds")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="&help | /help"
        )
    )
    await load_cogs()

@bot.event
async def setup_hook():
    try:
        synced = await bot.tree.sync()
        print(f"🔄 Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

@bot.command(name="help", aliases=["commands"])
async def help_command(ctx):
    """Show all commands registered in the bot"""
    
    if ctx.author.id == OWNER_ID:
        # Owner sees all commands including owner-only
        embed = discord.Embed(
            title="📚 All Bot Commands (Owner View)",
            description="Use `&command` or `/command` to execute\nPrefix: `&` | Slash Commands: `/`",
            color=BOT_COLOR
        )
        
        categories = {
            "🔊 Quote System": ["quote"],
            "🎉 Giveaway": ["giveaway", "giveaway_end"],
            "📊 Leveling": ["level", "leaderboard", "setlevel", "resetlevel"],
            "🎫 Ticket System": ["ticket", "close_ticket", "transcript"],
            "📡 Info": ["ping"],
            "👑 Superuser (Owner Only)": ["addsuperuser", "removesuperuser", "listsuperusers"],
            "🛡️ Moderation": ["ban", "unban", "softban", "kick", "mute", "unmute", "warn", "unwarn", "say"],
            "📌 Sticky Notes": ["stickynote", "stickynotes", "delstickynote"],
            "🎤 Voice Moderation": ["vckick", "vcmute", "vcunmute", "vcdeafen", "vcundeafen", "vckickall", "vcmuteall", "vcunmuteall", "vcmove", "vcpull"],
            "👥 Role Management": ["roleall", "roleadd", "roleremove", "roleremoveall", "rolecreate", "roledelete", "roleedit"],
            "👋 Welcome/Goodbye": ["setwelcome", "setgoodbye"],
            "⭐ Boost Messages": ["setboost"],
            "🎮 Fun Commands": ["joke", "meme", "8ball", "rate"],
            "👤 Server Profile": ["avatar", "serverbanner", "bioserver", "nameserver"],
            "🎵 Music": ["play", "pause", "resume", "stop", "queue", "skip"],
            "🔄 Autoresponders": ["autoresponder", "removeresponder", "listresponders"],
            "😊 Reaction Roles": ["reactionrole"],
            "🏅 Level Roles": ["levelrole"],
            "🌈 Vanity Roles": ["vanity"],
            "🔍 Snipe": ["snipe", "editsnipe"],
            "✅ Verification": ["verify", "setupverify"],
            "💾 Server Backup": ["backupserver", "restoreserver", "backuplist"],
        }
        
        total_commands = 0
        for category, commands_list in categories.items():
            embed.add_field(name=category, value="`, `".join(commands_list), inline=False)
            total_commands += len(commands_list)
        
        embed.set_footer(text=f"Total Commands: {total_commands} | Owner: {ctx.author}")
        await ctx.send(embed=embed)
    else:
        # Regular users see only public commands
        embed = discord.Embed(
            title="📚 Available Commands",
            description="Use `&command` or `/command` to execute\nPrefix: `&` | Slash Commands: `/`",
            color=BOT_COLOR
        )
        
        categories = {
            "🔊 Quote System": ["quote"],
            "🎉 Giveaway": ["giveaway"],
            "📊 Leveling": ["level", "leaderboard"],
            "🎫 Ticket System": ["ticket"],
            "📡 Info": ["ping"],
            "🛡️ Moderation": ["ban", "kick", "mute"],
            "📌 Sticky Notes": ["stickynote", "stickynotes"],
            "🎤 Voice Moderation": ["vckick", "vcmute"],
            "👥 Role Management": ["roleadd"],
            "🎮 Fun Commands": ["joke", "meme", "8ball", "rate"],
            "👤 Server Profile": ["avatar"],
            "🎵 Music": ["play", "pause", "stop"],
            "🔍 Snipe": ["snipe"],
        }
        
        total_commands = 0
        for category, commands_list in categories.items():
            embed.add_field(name=category, value="`, `".join(commands_list), inline=False)
            total_commands += len(commands_list)
        
        embed.set_footer(text=f"Total Commands: {total_commands} | Use &help for more info")
        await ctx.send(embed=embed)

@bot.tree.command(name="ping", description="Check bot latency")
async def ping_slash(interaction: discord.Interaction):
    """Slash command version of ping"""
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Latency: `{bot.latency * 1000:.2f}ms`",
        color=BOT_COLOR
    )
    await interaction.response.send_message(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    """Check bot latency"""
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Latency: `{bot.latency * 1000:.2f}ms`",
        color=BOT_COLOR
    )
    await ctx.send(embed=embed)

# Error handler
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="❌ Missing Argument",
            description=f"Missing required argument: `{error.param.name}`",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="❌ Permission Denied",
            description="You don't have permission to use this command",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    else:
        print(f"Error: {error}")

# Run the bot
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    print("❌ DISCORD_TOKEN not found in .env file")
    sys.exit(1)

bot.run(TOKEN)
