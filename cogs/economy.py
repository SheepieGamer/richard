import discord
import random
import peewee
from discord.ext import commands
import settings
from models.account import Account

logger = settings.logging.getLogger(__name__)


class EconomyBot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(aliases=['me', 'bal'])
    async def balance(self, ctx):
        account = Account.fetch(ctx.message)

        await ctx.reply(f"{ctx.author.display_name} has {account.amount} credits")

    @commands.hybrid_command(aliases=['coin'])
    async def coinflip(self, ctx, choice: str, amount_bet: int):
        account = Account.fetch(ctx.message)

        if amount_bet > account.amount:
            await ctx.reply("Insufficient funds")
            return

        heads = random.randint(0,1)
        won = False
        if heads and choice.lower().startswith("h"):
            won = True
            account.amount += amount_bet
        elif not heads and choice.lower().startswith("t"):
            won = True
            account.amount += amount_bet
        else:
            account.amount -= amount_bet

        account.save()
        message = "You Lost!"
        if won:
            message = "You won!"
        await ctx.reply(message)
        
        
        

async def setup(bot):
    await bot.add_cog(EconomyBot(bot))
