import discord
from discord.ext import commands
import settings

logger = settings.logging.getLogger(__name__)


class ModCMDS(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    @commands.has_permissions(manage_messages=True)
    async def purge(ctx, channel : discord.TextChannel = None, limit : int = 100):
        """ Delete N number of messages in a channel """
        if channel is None:
            channel = ctx.message.channel
        await channel.purge(limit=limit)

async def setup(bot):
    await bot.add_cog(ModCMDS(bot))