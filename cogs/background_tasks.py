from discord.ext import commands, tasks
import settings
import discord

logger = settings.logging.getLogger(__name__)

class BackgroundTasks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        # self.check_users.add_exception_type(Exception)
        self.check_users.start()

    def cog_unload(self) -> None:
        self.check_users.stop()
    
    @tasks.loop(seconds=10)
    async def check_users(self):
        pass
    # @commands.hybrid_command()
    # async def start_loop(self, ctx):
    #     self.check_users.start()

    # @commands.hybrid_command()
    # async def stop_loop(self, ctx):
    #     self.check_users.stop()

    # @commands.hybrid_command()
    # async def change_loop(self, ctx, seconds: int):
    #     self.check_users.change_interval(seconds=seconds)
    #     await ctx.reply("done")

    # @check_users.before_loop
    # async def before_check_users(self):
    #     logger.warn("Before starting loop")

    # @check_users.after_loop
    # async def after_check_users(self):
    #     logger.warn("After stopping loop")
    pass



async def setup(bot):
    await bot.add_cog(BackgroundTasks(bot))