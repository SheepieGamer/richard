import discord
from discord.ext import commands

class Greetings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if str(message.content) == "hi" or str(message.content) == "hello" or str(message.content) == "sup" or str(message.content) == "wassup":
            await message.add_reaction("👋")

    # @commands.Cog.listener()
    # async def on_message(self, message: discord.Message):
    #     if not message.author.id == 1167904817922977933:
    #         await message.reply("E")

    @commands.hybrid_command()
    async def hello(self, ctx, *, member: discord.Member):
        await ctx.send(f"Hello {member.mention}")

async def setup(bot):
    await bot.add_cog(Greetings(bot))