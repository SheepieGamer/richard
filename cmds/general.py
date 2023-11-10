from discord.ext import commands
import discord, random

class Slapper(commands.Converter):
    use_nicknames: bool

    def __init__(self, *, use_nicknames):
        self.use_nicknames = use_nicknames

    async def convert(self, ctx, argument):
        someone = random.choice(ctx.guild.members)
        nickname = ctx.author
        return f"{nickname.mention} slaps {someone.mention} with {argument}"

@commands.hybrid_command(aliases=['latency'], help="Reply's with:\nPong! [bot's ping]ms", brief="Gets the bot's ping in milliseconds", enabled=True, hidden=False)
async def ping(ctx):
    await ctx.reply(f"Pong! {round(commands.latency * 1000, 1)}ms")

@commands.hybrid_command(help="", brief="", enabled=True, hidden=False)
async def say(ctx,*, what_to_say):
    await ctx.reply(what_to_say)

# @commands.hybrid_command(help="", brief="", enabled=True, hidden=False)
# async def choices(ctx, *options):
#     await ctx.reply(random.choice(options))


@commands.hybrid_command(help="", brief="", enabled=True, hidden=False)
async def joined(ctx, who: discord.Member):
    await ctx.reply(f"welcome {who.mention}. {who} joined at {who.joined_at}")

@commands.hybrid_command(help="", brief="", enabled=True, hidden=False)
async def slap(ctx, using: Slapper(use_nicknames=True)):
    await ctx.reply(using)

@commands.command(aliases=[''], hidden=True)
async def aaaaaaaaaaaaaaaaaaaaaaa(ctx):
    await ctx.reply("You have found the secret command. Good job. Have a cookie :cookie:")

async def setup(bot):
    bot.add_command(ping)
    bot.add_command(say)
    # bot.add_command(choices)
    bot.add_command(joined)
    bot.add_command(slap)
    bot.add_command(aaaaaaaaaaaaaaaaaaaaaaa)