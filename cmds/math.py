from discord.ext import commands

@commands.hybrid_command()
async def math(ctx, simple_advanced: str, operator: str, one, two):
    if simple_advanced == "simple":
        if operator == "addition":
            await ctx.reply(int(one) + int(two))
        elif operator == "substraction":
            await ctx.reply(int(one) - int(two))
        elif operator == "multiplication":
            await ctx.reply(int(one) * int(two))
        elif operator == "division":
            await ctx.reply(int(one) / int(two))
        else:
            ctx.reply("invalid operator")
    elif simple_advanced == "advanced":
        ctx.reply("in development")

# @commands.group(help="", brief="", enabled=True, hidden=False)
# async def math(ctx):
#     if ctx.invoked_subcommand is None:
#         await ctx.reply(f"No, ``{ctx.subcommand_passed}`` does not belong to ``simple``. (subcommands: simple, advanced)")

# @math.group(help="", brief="", enabled=True, hidden=False)
# async def simple(ctx):
#     if ctx.invoked_subcommand is None:
#         await ctx.reply(f"No, ``{ctx.subcommand_passed}`` does not belong to ``simple``. (subcommands: add, substract, multiply, divide)")

# @simple.command(aliases=['a', 'ad', 'addition'], help="", brief="", enabled=True, hidden=False)
# async def add(ctx, one: int, two: int):
#     await ctx.reply(f"{str(one)} + {str(two)} = {one + two}")

# @simple.command(aliases=['subtract', 's', 'substraction', 'subtraction'], help="", brief="", enabled=True, hidden=False)
# async def substract(ctx, one: int, two: int):
#     await ctx.reply(f"{str(one)} - {str(two)} = {one - two}")

# @simple.command(aliases=['m', 'multiplication'], help="", brief="", enabled=True, hidden=False)
# async def multiply(ctx, one: int, two: int):
#     await ctx.reply(f"{str(one)} * {str(two)} = {one * two}")

# @simple.command(aliases=['d', 'division'], help="", brief="", enabled=True, hidden=False)
# async def divide(ctx, one: int, two: int):
#     await ctx.reply(f"{str(one)} / {str(two)} = {float(one / two)}")


async def setup(bot):
    bot.add_command(math)
