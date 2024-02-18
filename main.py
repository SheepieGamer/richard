import utils, discord, settings
from discord import app_commands
from discord.ext import commands
from database import economy
from models.account import Account

logger = settings.logging.getLogger("bot")

def main(token):
    economy.db.create_tables([Account])

    activity = discord.Activity(type=discord.ActivityType.watching, name="richard")

    bot = commands.Bot(command_prefix=settings.PREFIX, intents=settings.INTENTS, activity=activity)

    # bot.tree.sync()

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

    # play together
    @bot.tree.command()
    @app_commands.choices(game=[app_commands.Choice(name="Unrailed", value="unrailed"), app_commands.Choice(name="Valorant", value="valorant"), app_commands.Choice(name="CS:GO", value="csgo"), app_commands.Choice(name="Other", value="other")])
    async def play(interaction: discord.Interaction, game: app_commands.Choice[str], players: int = 4):
        view = utils.ReadyOrNotView(timeout=None)
        view.initiatior = interaction.user
        view.game = utils.games_list[game.value]
        view.players = players
        await view.send(interaction)
    
    
    @bot.event 
    async def on_message(message: discord.Message):
        await utils.chat_gpt(message=message, bot=bot)
    bot.run(token, root_logger=True)

if __name__ == "__main__":
    main(settings.TOKEN)



