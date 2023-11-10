import discord
from discord.ext import commands, tasks
import settings

logger = settings.logging.getLogger(__name__)

class BackgroundTasks(commands.Cog):

    # def __init__(self, bot):
    #     self.bot = bot
    #     # self.check_users.add_exception_type(Exception)
    #     self.check_users.start()

    # def cog_unload(self) -> None:
    #     self.check_users.stop()
    
    # @tasks.loop(seconds=10)
    # async def check_users(self):
    #     online = 0
    #     idle = 0
    #     dnd = 0
    #     offline = 0
    #     for member in self.bot.guilds[0].members:
    #         if member.status == discord.Status.online:
    #             online += 1
    #         if member.status == discord.Status.idle:
    #             idle += 1
    #         if member.status == discord.Status.dnd:
    #             dnd += 1
    #         if member.status == discord.Status.offline:
    #             offline += 1

    #     # if offline == 1:
    #     #     raise Exception("Help")

    #     logger.info({
    #         "online": online,
    #         "offline": offline,
    #         "dnd": dnd,
    #         "idle": idle
    #     })
    
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