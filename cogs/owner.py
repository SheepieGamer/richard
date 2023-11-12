import discord
from discord.ext import commands
import settings

logger = settings.logging.getLogger(__name__)


class MyCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(hidden=True)
    async def ext(ctx):
        if ctx.author.id == 1117914448745738444:
            if ctx.invoked_subcommand is None:
                await ctx.reply("Invalid subcommand.")
        else:
            await ctx.reply("Permission denied.")


    @ext.command(hidden=True)
    async def reload(ctx, cogs: str):
        if ctx.author.id == 1117914448745738444:
            await commands.reload_extension(f"{cogs.lower()}")
            print(f"INFO       - bot             : {cogs} successfully reloaded")
            await ctx.reply(f"successfully reloaded {cogs}")
        else:
            await ctx.reply("Permission denied.")

    @ext.command(hidden=True)
    async def load(ctx, cogs: str):
        if ctx.author.id == 1117914448745738444:
            await commands.load_extension(f"cogs.{cogs.lower()}")
            print(f"INFO       - bot             : cogs.{cogs} successfully loaded")
            await ctx.reply(f"successfully loaded {cogs}")
        else:
            await ctx.reply("Permission denied.")

    @ext.command(hidden=True)
    async def unload(ctx, cogs: str):
        if ctx.author.id == 1117914448745738444:
            if cogs != "owner":
                await commands.unload_extension(f"cogs.{cogs.lower()}")
                print(f"INFO       - bot             : cogs.{cogs} successfully unloaded")
                await ctx.reply(f"successfully unloaded {cogs}")
            elif cogs == "owner":
                await ctx.reply("Cannot unload cogs \"owner\"")

        else:
            await ctx.reply("Permission denied.")

async def setup(bot):
    await bot.add_cog(MyCog(bot))