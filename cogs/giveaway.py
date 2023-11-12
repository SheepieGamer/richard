import discord
import random
from discord.ext import commands
import settings

logger = settings.logging.getLogger(__name__)


class Giveaway(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def giveaway(ctx, prize: str, winners: int = 1, role: discord.Role = None):
        members_selection = []
        if role:
            members_selection = role.members
        else:
            members_selection = ctx.channel.guild.members

        filtered_members = []
        for member in members_selection:
            if not member.bot:
                filtered_members.append(member)
            
        if not len(filtered_members):
            return
        
        if len(filtered_members) < winners:
            await ctx.author.send("Hey refinde your list. everyone would win!")
            return
        winner_list = []

        while len(winner_list) < winners:
            winner = random.choice(filtered_members)
            if winner not in winner_list:
                await ctx.send(f"The winner for **{prize}** is {winner.mention}")
                winner_list.append(winner)

async def setup(bot):
    await bot.add_cog(Giveaway(bot))