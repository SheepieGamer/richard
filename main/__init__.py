import settings, discord
from discord.ext import commands

activity = discord.Activity(type=discord.ActivityType.watching, name="richard")
bot = commands.Bot(command_prefix=settings.PREFIX, intents=settings.INTENTS, activity=activity)
