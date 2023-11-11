import typing
import discord
from discord.ext import commands

import settings

logger = settings.logging.getLogger(__name__)

@commands.command()
async def channel(ctx, channel : typing.Union[discord.TextChannel, discord.VoiceChannel, discord.StageChannel]):    
    embed = discord.Embed(
        title=f"{channel.name} Info"
    )
    embed.add_field(name="ID", value=channel.id, inline=False)
    embed.add_field(name="Type", value=channel.type, inline=True)
    embed.add_field(name="Created at", value=discord.utils.format_dt(channel.created_at), inline=False)
    
    if channel.category:
        embed.add_field(name="Category", value=f"{channel.category.name} (ID: {channel.category.id})", inline=False)
    
    if isinstance(channel, discord.VoiceChannel):
        embed.add_field(name="Bitrate", value=channel.bitrate, inline=True)
        embed.add_field(name="User Limit", value=channel.user_limit, inline=True)
        embed.add_field(name="Members", value=len(channel.members), inline=True)
        if channel.members:
            members_list = ""
            for member in channel.members:
                members_list += f"{member.nick} (ID: {member.id}), "
            embed.add_field(name="Active Members Info", value=members_list[:-2], inline=False)
    
    if isinstance(channel, discord.TextChannel):
        embed.add_field(name="News?", value="Yes" if channel.is_news() else "No", inline=True)
        embed.add_field(name="NSFW?", value="Yes" if channel.is_nsfw() else "No", inline=True)
    
    if isinstance(channel, discord.StageChannel):
        embed.add_field(name="Bitrate", value=channel.bitrate, inline=True)
        if channel.moderators:
            moderators_list = ""
            for moderator in channel.moderators:
                moderators_list += f"{moderator.display_name} (ID {moderator.id}),"
            embed.add_field(name="Moderators", value=moderators_list[:-1], inline=False)
        
        if channel.listeners:
            listeners_list = ""
            for listener in channel.listeners:
                listeners_list += f"{listener.display_name} (ID {listener.id}),"
            embed.add_field(name="Listeners", value=listeners_list[:-1], inline=False)
        
        if channel.speakers:
            speakers_list = ""
            for speaker in channel.speakers:
                speakers_list += f"{speaker.display_name} (ID {speaker.id}),"
            embed.add_field(name="Speakers", value=speakers_list[:-1], inline=False)
        
    await ctx.send(embed=embed)
    
# @channel.error 
# async def debug_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):        
#         await ctx.send("Must have a channel to inspect")

async def setup(bot):
    bot.add_command(channel)