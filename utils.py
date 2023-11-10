import settings

logger = settings.logging.getLogger(__name__)

async def print_user(bot):
    logger.info(f"User: {bot.user} (ID: {bot.user.id})")

async def load_videocmds(bot):
    for extension_file in settings.VIDEOCMDS_DIR.glob("*.py"):
        if extension_file.name != "__init__.py" and not extension_file.name.startswith("_"):
            await bot.load_extension(f"{settings.VIDEOCMDS_DIR.name}.{extension_file.name[:-3]}")
            logger.info(f"videocmds.{extension_file.name[:-3]} successfully loaded")

async def load_cogs(bot):
    for cog_file in settings.COGS_DIR.glob("*.py"):
        if cog_file.name != "__init__.py":
            await bot.load_extension(f"cogs.{cog_file.name[:-3]}")
            logger.info(f"cogs.{cog_file.name[:-3]} successfully loaded")

async def load_cmds(bot):
    for cmd_file in settings.CMDS_DIR.glob("*.py"):
        if cmd_file.name != "__init__.py":
            await bot.load_extension(f"cmds.{cmd_file.name[:-3]}")
            logger.info(f"cmds.{cmd_file.name[:-3]} successfully loaded")

async def other(bot):
    bot.tree.copy_global_to(guild=bot.guilds[0])
    await bot.tree.sync(guild=bot.guilds[0])
    logger.info("Tree synced")
    logger.info("--")
    logger.info("--")


# nothing after