import discord, settings, datetime
from discord.ext import commands

logger = settings.logging.getLogger(__name__)


class ModeratorCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(pass_context = True, help='clears messages above it based on the number passed in, or pass in "all" to purge all')
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = 10):
        if amount <= 100:
            await ctx.channel.purge(limit=(int(amount)))
            embed = discord.Embed(title=f"Purged {amount} messages", color = discord.Color.random())
            await ctx.reply(embed=embed)
        else:
            await ctx.reply("Limit is 100")

    @commands.hybrid_command(aliases=['k'])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member,*,reason="No reason provided"):
        await ctx.reply(f":white_check_mark: **{member.display_name}** was kicked for reason: ``{reason}``")
        await member.kick(reason=reason)


    @commands.hybrid_command(aliases=['b'])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member,*,reason="No reason provided"):
        try:
            embed = discord.Embed(title=":white_check_mark: Banned", description=f"{member} was banned for reason: **{reason}**", color=discord.Color.random())
            await member.send(f":warning:Sorry! You were banned for reason: **{reason}**")
            await ctx.reply(embed=embed)
            await member.ban(reason=reason)
        except KeyError:
            pass

    @commands.command(aliases=['unb'])
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: int, *, reason: str="None"):
        not_work_msg = ":warning: If it isn't working, make sure to put in the user's ID after ``r!unban``"
        try:
            user = await self.bot.fetch_user(user)
            await ctx.guild.unban(user, reason=reason)
            embed = discord.Embed(title=":white_check_mark: Unban", description=f"{user.name} ({user.id}) has been unbanned.", color=discord.Color.random())
            await ctx.reply(embed=embed)
        except discord.NotFound:
            embed = discord.Embed(title=":x: Error", description=f"Banned User with ID {user} not found.", color=discord.Color.random())
            await ctx.reply(f"{not_work_msg}", embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(title=":x: Error", description="I do not have permission to unban users, or this user is higher up on the role list than me.", color=discord.Color.random())
            await ctx.reply(f"{not_work_msg}", embed=embed)
        except Exception as e:
            embed = discord.Embed(title=":x: Unkown Error", description=str(e), color=discord.Color.random())
            await ctx.reply(f"{not_work_msg}", embed=embed)

    @commands.command(aliases=['m'])
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, timelimit, *,reason="reason unspecified"):
        if "s" in timelimit:
            gettime = timelimit.strip("s")
            newtime = datetime.timedelta(seconds=int(gettime))
            await member.timeout(discord.utils.utcnow() + newtime, reason=reason)
            await ctx.reply(f"{member} has been successfully muted for {gettime} seconds")
        elif "m" in timelimit:
            time = timelimit.strip("m")
            gettime = int(time) * 60
            newtime = datetime.timedelta(seconds=int(gettime))
            await member.timeout(discord.utils.utcnow() + newtime, reason=reason)
            await ctx.reply(f"{member} has been successfully muted for {time} minutes")
        elif "h" in timelimit:
            time = timelimit.strip("h")
            gettime = (int(time) * 60) * 60
            newtime = datetime.timedelta(seconds=int(gettime))
            await member.timeout(discord.utils.utcnow() + newtime, reason=reason)
            await ctx.reply(f"{member} has been successfully muted for {time} hours")
        elif "d" in timelimit:
            time = timelimit.strip("d")
            gettime = ((int(time) * 60) * 60) * 24
            newtime = datetime.timedelta(seconds=int(gettime))
            await member.timeout(discord.utils.utcnow() + newtime, reason=reason)
            await ctx.reply(f"{member} has been successfully muted for {time} days")
        




async def setup(bot):
    await bot.add_cog(ModeratorCommands(bot))