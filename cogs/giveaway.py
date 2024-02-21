import discord, random, asyncio, datetime, settings
from discord.ext import commands

logger = settings.logging.getLogger(__name__)

async def end_giveaway(prize=None, channel=None, winner=None, users=None):
    winning_announcement = discord.Embed(color = 0xff2424)
    winning_announcement.set_author(name = f'THE GIVEAWAY HAS ENDED!', icon_url= 'https://i.imgur.com/DDric14.png')
    winning_announcement.add_field(name = f'🎉 Prize: {prize}', value = f'🥳 **Winner**: {winner.mention}\n 🎫 **Number of Entrants**: {len(users)}', inline = False)
    winning_announcement.set_footer(text = 'Thanks for entering!')
    await channel.send(f"{winner.mention}", embed = winning_announcement)


class Giveaway(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    # async def giveaway(self, ctx, prize: str, winners: int = 1, role: discord.Role = None):
    #     members_selection = []
    #     if role:
    #         members_selection = role.members
    #     else:
    #         members_selection = ctx.channel.guild.members

    #     filtered_members = []
    #     for member in members_selection:
    #         if not member.bot:
    #             filtered_members.append(member)
            
    #     if not len(filtered_members):
    #         return
        
    #     if len(filtered_members) < winners:
    #         await ctx.author.send("Hey refinde your list. everyone would win!")
    #         return
    #     winner_list = []

    #     while len(winner_list) < winners:
    #         winner = random.choice(filtered_members)
    #         if winner not in winner_list:
    #             await ctx.send(f"The winner for **{prize}** is {winner.mention}")
    #             winner_list.append(winner)


    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def giveaway(self, ctx):
        giveaway_questions = ['Which channel will I host the giveaway in?', 'What is the prize?', 'How long should the giveaway run for (in minutes)?',]
        giveaway_answers = []

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        for question in giveaway_questions:
            await ctx.send(question)
            try:
                message = await self.bot.wait_for('message', timeout= 30.0, check= check)
            except asyncio.TimeoutError:
                await ctx.send('You didn\'t answer in time. Please try again and be sure to send your answer within 30 seconds of the question.')
                return
            else:
                giveaway_answers.append(message.content)

        try:
            c_id = int(giveaway_answers[0][2:-1])
        except:
            await ctx.send(f'You failed to mention the channel correctly. Please do it like this: {ctx.channel.mention}')
            return
        
        channel = self.bot.get_channel(c_id)
        prize = str(giveaway_answers[1])
        time = float(giveaway_answers[2])

        await ctx.send(f'The giveaway for {prize} will begin shortly.\nPlease direct your attention to {channel.mention}, this giveaway will end in {time} minutes. ({time*60} seconds)')

        hours = round(time/60, 2)
        give = discord.Embed(color = 0x2ecc71)
        give.set_author(name = f'GIVEAWAY TIME!', icon_url = 'https://i.imgur.com/VaX0pfM.png')
        give.add_field(name= f'{ctx.author.display_name} is giving away: {prize}!', value = f'React with 🎉 to enter!\n Ends in {time} minutes! ({hours} hours)', inline = False)
        end = datetime.datetime.utcnow() + datetime.timedelta(seconds=time)
        end_ = end.strftime(f"%m/%d/%Y, %H:%M")
        give.set_footer(text = f'Giveaway ends at {end_} UTC!')
        my_message = await channel.send(embed = give)
        
        await my_message.add_reaction("🎉")
        await asyncio.sleep(time*60)

        new_message = await channel.fetch_message(my_message.id)

        try:
            users = [user async for user in new_message.reactions[0].users() if user.id != self.bot.user.id]
            winner = random.choice(users)
        except:
            await channel.send("No one entered :(")
        
        await end_giveaway(prize=prize, channel=channel, winner=winner, users=users)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def g_end(self, msg_id: int, channel: discord.TextChannel):
        new_message = await channel.fetch_message(msg_id)
        if new_message.author == self.bot.user:
            try:
                users = [user async for user in new_message.reactions[0].users() if user.id != self.bot.user.id]
                winner = random.choice(users)
            except:
                await channel.send("No one entered :(")

            await end_giveaway(prize="[UNKNOWN]", channel=channel, winner=winner, users=users)
            """
            winning_announcement = discord.Embed(color = 0xff2424)
            winning_announcement.set_author(name = f'THE GIVEAWAY HAS ENDED!', icon_url= 'https://i.imgur.com/DDric14.png')
            winning_announcement.add_field(name = f'🎉 Prize: [UNKNOWN]', value = f'🥳 **Winner**: {winner.mention}\n 🎫 **Number of Entrants**: {len(users)}', inline = False)
            winning_announcement.set_footer(text = 'Thanks for entering!')
            await channel.send(f"{winner.mention}", embed = winning_announcement)
            """

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def reroll(self, ctx, channel: discord.TextChannel, id_ : int):
        try:
            new_message = await channel.fetch_message(id_)
        except:
            await ctx.send("Incorrect id.")
            return
        
        # Picks a new winner
        users = [user async for user in new_message.reactions[0].users() if user.id != self.bot.user.id]
        winner = random.choice(users)


        # Announces the new winner to the server
        reroll_announcement = discord.Embed(color = 0xff2424)
        reroll_announcement.set_author(name = f'The giveaway was re-rolled by the host!', icon_url = 'https://i.imgur.com/DDric14.png')
        reroll_announcement.add_field(name = f'🥳 New Winner:', value = f'{winner.mention}', inline = False)
        await new_message.reply(f"{winner.mention}", embed = reroll_announcement)



async def setup(bot):
    await bot.add_cog(Giveaway(bot))