from discord.ext import commands

# @commands.hybrid_command()
# async def cogs(ctx, reload_load_unload: str, cogs: str):
#     if ctx.author.id == 1117914448745738444:
#         if reload_load_unload == "reload":
#             await commands.reload_extension(f"cogs.{cogs}")
            
#             print(f"INFO       - bot             : cogs.{cogs} successfully reloaded")
#             await ctx.reply(f"successfully reloaded {cogs}")
        
#         elif reload_load_unload == "load":
#             await commands.load_extension(f"cogs.{cogs}")
            
#             print(f"INFO       - bot             : cogs.{cogs} successfully unloaded")
#             await ctx.reply(f"successfully loaded {cogs}")
        
#         elif reload_load_unload == "unload":
#             await commands.load_extension(f"cogs.{cogs}")
            
#             print(f"INFO       - bot             : cogs.{cogs} successfully unloaded")
#             await ctx.reply(f"successfully unloaded {cogs}")
        
#         else:
#             await ctx.reply("reload or load or unload", ephemeral=True)
#     else:
#         ctx.reply("Permission denied.")

@commands.group(hidden=True)
async def ext(ctx):
    if ctx.author.id == 1117914448745738444:
        if ctx.invoked_subcommand is None:
            await ctx.reply("Invalid subcommand.")
    else:
        await ctx.reply("Permission denied.")


@ext.command(hidden=True)
async def reload(ctx, cogs: str):
    if ctx.author.id == 1117914448745738444:
        await commands.reload_extension(f"cogs.{cogs.lower()}")
        print(f"INFO       - bot             : cogs.{cogs} successfully reloaded")
        await ctx.reply(f"successfully reloaded {cogs}")
    else:
        await ctx.reply("Permission denied.")

@ext.command(hidden=True)
async def load(ctx, cogs: str):
    if ctx.author.id == 1117914448745738444:
        await commands.load_extension(f"cogs.{cogs.lower()}")
        print(f"INFO       - bot             : cogs.{cogs} successfully loaded")
        await ctx.reply(f"successfully loaded {cogs}")
    else:
        await ctx.reply("Permission denied.")

@ext.command(hidden=True)
async def unload(ctx, cogs: str):
    if ctx.author.id == 1117914448745738444:
        if cogs != "owner":
            await commands.unload_extension(f"cogs.{cogs.lower()}")
            print(f"INFO       - bot             : cogs.{cogs} successfully unloaded")
            await ctx.reply(f"successfully unloaded {cogs}")
        elif cogs == "owner":
            await ctx.reply("Cannot unload cogs \"owner\"")

    else:
        await ctx.reply("Permission denied.")

async def setup(bot):
    bot.add_command(ext)