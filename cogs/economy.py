import discord
from discord.ext import commands
import settings

logger = settings.logging.getLogger(__name__)


class EconomyBot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(EconomyBot(bot))