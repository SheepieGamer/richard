import settings
import utils
import discord
from discord.ext import commands

logger = settings.logging.getLogger("bot")

def main():
    bot = commands.Bot(command_prefix=settings.PREFIX, intents=settings.INTENTS)

    @bot.event
    async def on_ready():
        await utils.print_user(bot)
        await utils.load_cogs(bot)
        await utils.load_cmds(bot)
        await utils.other(bot)
        logger.info("Startup complete")
        # nothing after


    
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(error)

    @bot.hybrid_command()
    async def hii(ctx):
        await ctx.send(f"hewwo {ctx.author.mention}", ephemeral=True)

    @bot.tree.command(description="desc", name="name")
    async def hewwo(interaction: discord.Interaction):
        await interaction.response.send_message(f"hii {interaction.user.mention}", ephemeral=True)




    bot.run(settings.TOKEN, root_logger=True)


""" command template

@bot.command(help="", brief="", enabled=True, hidden=False)
async def cmd(ctx):
    await ctx.reply(f"")

"""

if __name__ == "__main__":
    main()