import discord

class Ranks:
    async def process_message(self, message: discord.Message):
        ...
    async def process_reaction(self, payload: discord.RawReactionActionEvent):
        ...