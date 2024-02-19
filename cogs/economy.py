import discord
import random
import peewee
from discord.ext import commands
import settings
from discord.ext.commands import cooldown, BucketType
from models.account import Account

logger = settings.logging.getLogger(__name__)


class EconomyBot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(aliases=['me', 'bal'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def balance(self, ctx):
        account = Account.fetch(ctx.message)

        await ctx.reply(f"{ctx.author.display_name} has {account.amount} credits")

    @commands.hybrid_command()
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def work(self,ctx):
        account = Account.fetch(ctx.message)
        won = random.randint(3, 189)
        account.amount += won
        if won <= 28:
            await ctx.reply(f"You worked for {won} coins. You did badly.")
        elif won <= 51:
            await ctx.reply(f"You worked for {won} coins. You did good.")
        elif won <= 103:
            await ctx.reply(f"You worked for {won} coins. You did very well.")
        elif won > 103:
            await ctx.reply(f"You worked for {won} coins. You did an excellent job.")
        else:
            await ctx.reply(f"You worked for {won} coins.")
        account.save()

    @commands.hybrid_command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def beg(self,ctx):
        account = Account.fetch(ctx.message)

        won = random.randint(0, 1)
        if won == 0:
            await ctx.reply("HAHHA YOU BEGGED AND DIDN'T GET ANYTHING :regional_indicator_l::joy:")
        elif won == 1:
            amount = random.randint(1,15)
            await ctx.reply(f"Lucky! You begged and got {amount} coins")
            account.amount += amount

        account.save()

    @commands.hybrid_command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def fish(self, ctx, sell: bool):
        account = Account.fetch(ctx.message)

        fishables = ['dory', 'nemo', 'boot', 'seaweed', 'fishing-line', 'hook', 'trout', 'salmon']

        fished = random.choice(fishables)

        if sell:
            if fished == 'dory':
                await ctx.reply(f"You fished up Dory. You sold Dory for 1 coin.")
                account.amount += 1
            if fished == 'nemo':
                await ctx.reply(f"You fished up Nemo. You sold Nemo for 2 coins.")
                account.amount += 2
            if fished == 'boot':
                await ctx.reply(f"You fished up a boot. You sold your boot for 2 coins.")
                account.amount += 2
            if fished == 'seaweed':
                await ctx.reply(f"You fished up seaweed. You sold your seaweed for 1 coin.")
                account.amount += 1
            if fished == 'fishing-line':
                await ctx.reply(f"You fished up fishing line. You sold your fishing line for 0 coins. :regional_indicator_l:")
            if fished == 'hook':
                await ctx.reply(f"You fished up a hook. You sold your hook for 3 coins.")
                account.amount += 3
            if fished == 'trout':
                await ctx.reply(f"You fished up a trout. You sold your trout for 15 coins.")
                account.amount += 15
            if fished == 'salmon':
                await ctx.reply(f"You fished up a salmon. You sold your salmon for 33 coins.")
                account.amount += 33
        else:
            await ctx.reply("You didn't choose to sell what you fished up. What an idiot.")
        account.save()

    @commands.hybrid_command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def dig(self, ctx, sell: bool):
        account = Account.fetch(ctx.message)

        diggables = ['worm', 'beetle', 'dirt', 'rusty-bucket', 'boot', 'ant', 'sand', 'dog', 'shovel', 'superman']

        dug = random.choice(diggables)

        if sell:
            if dug == 'worm':
                await ctx.reply(f"You dug up a worm. You sold your worm for 4 coins.")
                account.amount += 4
            if dug == 'beetle':
                await ctx.reply(f"You dug up a beetle. You sold your beetle for 6 coins.")
                account.amount += 6
            if dug == 'dirt':
                await ctx.reply(f"You dug up dirt. You sold your dirt for 2 coins.")
                account.amount += 2
            if dug == 'rusty-bucket':
                await ctx.reply(f"You dug up a rusty bucket. You sold your rusty bucket for 15 coins.")
                account.amount += 15
            if dug == 'boot':
                await ctx.reply(f"You dug up a boot. You sold your boot for 23 coins.")
                account.amount += 23
            if dug == 'ant':
                await ctx.reply(f"You dug up an ant. You sold your ant for 3 coins.")
                account.amount += 3
            if dug == 'sand':
                await ctx.reply(f"You dug up sand. You sold your sand for 3 coins.")
                account.amount += 3
            if dug == 'dog':
                await ctx.reply(f"You dug up a dog. You sold your dog for 33 coins.")
                account.amount += 33
            if dug == 'shovel':
                await ctx.reply(f"You dug up a shovel. You sold your shovel for 28 coins.")
                account.amount += 28
            if dug == 'superman':
                await ctx.reply(f"You dug up SUPERMAN?? You sold ``superman`` for 273 coins.")
                account.amount += 273
        else:
            await ctx.reply("You didn't choose to sell what you dug up. What an idiot.")
        account.save()

    @commands.hybrid_command(aliases=['cf'])
    @commands.cooldown(1, 30, commands.BucketType.user)
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
    
    # cooldowns

    @work.error
    async def command_name_error(self,ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"You're on cooldown!",description=f"Try again in {error.retry_after:.2f}s.")
            await ctx.reply(embed=em)  
    @balance.error
    async def command_name_error(self,ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"You're on cooldown!",description=f"Try again in {error.retry_after:.2f}s.")
            await ctx.reply(embed=em)        
    @beg.error
    async def command_name_error(self,ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"You're on cooldown!",description=f"Try again in {error.retry_after:.2f}s.")
            await ctx.reply(embed=em)
    @dig.error
    async def command_name_error(self,ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"You're on cooldown!",description=f"Try again in {error.retry_after:.2f}s.")
            await ctx.reply(embed=em)
    @coinflip.error
    async def command_name_error(self,ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"You're on cooldown!",description=f"Try again in {error.retry_after:.2f}s.")
            await ctx.reply(embed=em)


async def setup(bot):
    await bot.add_cog(EconomyBot(bot))
