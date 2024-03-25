import utils, discord, settings, asyncio
from discord import app_commands
from discord.ext import commands
from database import economy
from models.account import Account
from keep_alive import keep_alive
from main import bot
keep_alive()



logger = settings.logging.getLogger("bot")

def main(token):
    global bot
    economy.db.create_tables([Account])
    
    @bot.event
    async def on_ready():
        await utils.print_user(bot)
        await utils.load_cogs(bot)
        await utils.load_cmds(bot)
        await utils.other(bot)
        await asyncio.sleep(1)
        logger.info("--")
        logger.info("Startup complete")
        # nothing after

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(error)

    # play together
    @bot.tree.command()
    @app_commands.choices(game=[app_commands.Choice(name="Unrailed", value="unrailed"), app_commands.Choice(name="Valorant", value="valorant"), app_commands.Choice(name="CS:GO", value="csgo"), app_commands.Choice(name="Other", value="other")])
    async def play(interaction: discord.Interaction, game: app_commands.Choice[str], players: int = 4):
        view = utils.ReadyOrNotView(timeout=None)
        view.initiatior = interaction.user
        view.game = utils.games_list[game.value]
        view.players = players
        await view.send(interaction)
    
    bot.run(token, root_logger=True)

if __name__ == "__main__":
    main(settings.TOKEN)