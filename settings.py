import pathlib, os, discord
import logging
from logging.config import dictConfig
from dotenv import load_dotenv

load_dotenv()

COLOR = discord.Color.random()

PREFIX = "r!"
INTENTS = discord.Intents.all()

TOKEN = os.getenv("DISCORD_API_TOKEN")

AI_API = os.getenv("AI_API")

BASE_DIR = pathlib.Path(__file__).parent
IMAGES_DIR = BASE_DIR / "images"
IMAGES_TEMP_DIR = IMAGES_DIR / "temp"
IMAGES_AVATAR_TEMP_DIR = IMAGES_DIR / "avatars"

CMDS_DIR = BASE_DIR / "cmds"
COGS_DIR = BASE_DIR / "cogs"


# GUILDS_ID = discord.Object(id=int(os.getenv("GUILD")))
# FEEDBACK_CH = int(os.getenv("FEEDBACK_CH", 0))
# GUILD_ID_INT = int(os.getenv("GUILD"))

LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
        },
        "standard": {"format": "%(levelname)-10s - %(name)-15s : %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "console2": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/infos.log",
            "mode": "w",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "bot": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "discord": {
            "handlers": ["console2", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

dictConfig(LOGGING_CONFIG)