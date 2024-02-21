from discord.ext import commands
import discord, utils, settings
logger = settings.logging.getLogger(__name__)


class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(aliases=['latency'], help="Replys with:\nPong! [bot's ping]ms", brief="Gets the bot's ping in milliseconds", enabled=True, hidden=False)
    async def ping(self, ctx):
        await ctx.reply(f"Pong! {round(ctx.bot.latency * 1000, 1)}ms")


    @commands.hybrid_command(help="", brief="", enabled=True, hidden=False)
    async def joined(self, ctx, who: discord.Member):
        await ctx.reply(f"welcome {who.mention}. {who} joined at {who.joined_at}")

    @commands.command(aliases=['serverinfo'])
    async def server(self, ctx):
        """ Shows basic information about Guild """
        
        embed = discord.Embed(
                            title=f"{ctx.guild.name} - Server Info ", 
                            description="Your server information")
        
        embed.add_field(name="Server Name", value=ctx.guild.name, inline=False)
        embed.add_field(name="GUID", value=ctx.guild.id, inline=False)
        embed.add_field(name="Created at", value=discord.utils.format_dt(ctx.guild.created_at), inline=False)
        embed.add_field(name="Server Description", value=ctx.guild.description, inline=False)

        embed.add_field(name="Owner Name", value=ctx.guild.owner.nick, inline=False)
        embed.add_field(name="Owner Account Created", value=discord.utils.format_dt(ctx.guild.owner.created_at), inline=False)
        
        embed.add_field(name="Server Users", value=ctx.guild.member_count, inline=True)
        embed.add_field(name="Channels", value=len(ctx.guild.channels), inline=True)
        embed.add_field(name="Voice", value=len(ctx.guild.voice_channels), inline=True)
        embed.add_field(name="Stage", value=len(ctx.guild.stage_channels), inline=True)
        embed.add_field(name="Text", value=len(ctx.guild.text_channels), inline=True)
        embed.add_field(name="Categories", value=len(ctx.guild.categories), inline=True)
        embed.add_field(name="Forums", value=len(ctx.guild.forums), inline=True)
        
        
        embed.add_field(name="File Size Limit", value=f"%.2f Mb" % float(ctx.guild.filesize_limit / 1024 / 1024), inline=False)
        embed.add_field(name="Bitrate Limit", value=f"%.2f kbit" %  float(ctx.guild.bitrate_limit / 1000), inline=False)
        
        embed.add_field(name="Tier", value=ctx.guild.premium_tier, inline=True)
        embed.add_field(name="Sub Count", value=ctx.guild.premium_subscription_count, inline=True)
        
        if len(ctx.guild.features):
            features = ":".join(ctx.guild.features)    
            embed.add_field(name="Features", value=features, inline=False)
        
        embed.add_field(name="MFA", value="Disabled" if ctx.guild.mfa_level == discord.MFALevel.disabled else "Enabled", inline=False)
        embed.add_field(name="Is large?", value="Yes" if ctx.guild.large else "No", inline=False)
        
        
        embed.add_field(name="AFK Channel", value=ctx.guild.afk_channel, inline=False)
        embed.add_field(name="Rules Channel", value=ctx.guild.rules_channel, inline=False)
        embed.add_field(name="System Channel", value=ctx.guild.system_channel, inline=False)
        
        
        embed.add_field(name="Default Role", value=ctx.guild.default_role.name, inline=True)
        if ctx.guild.premium_subscriber_role:
            embed.add_field(name="Premium Subscriber Role", value=ctx.guild.premium_subscriber_role.name, inline=True)
        embed.add_field(name="# Roles", value=len(ctx.guild.roles), inline=True)
            
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        if ctx.guild.banner:        
            embed.set_image(url=ctx.guild.banner.url)
    
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="generate-password")
    async def password_gen(self, ctx, characters: int = 8):
        await ctx.author.send(f"Your password is ||{utils.gen_pw(characters)}||")
        await ctx.reply("Your password is in your DMs")

async def setup(bot):
    await bot.add_cog(General(bot))