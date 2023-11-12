from discord.ext import commands
import settings

logger = settings.logging.getLogger(__name__)


class Math(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def math(self, ctx, operator: str,  one, two, simple_advanced: str = "simple",):
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


async def setup(bot):
    await bot.add_cog(Math(bot))