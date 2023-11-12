import discord
from discord.ext import commands
import settings
import asyncio
import requests
from typing import Union
from PIL import Image
import random
from jokeapi import Jokes

from PIL import Image


COLORS = {
    (0, 0, 0): "⬛",
    (0, 0, 255): "🟦",
    (255, 0, 0): "🟥",
    (255, 255, 0): "🟨",
    (255, 165, 0): "🟧",
    (255, 255, 255): "⬜",
    (0, 255, 0): "🟩"
}


def euclidean_distance(c1, c2):
    r1, g1, b1 = c1
    r2, g2, b2 = c2
    d = ((r2 - r1) ** 2 + (g2 - g1) ** 2 + (b2 - b1) ** 2) ** 0.5

    return d


def find_closest_emoji(color):
    c = sorted(list(COLORS), key=lambda k: euclidean_distance(color, k))
    return COLORS[c[0]]


def emojify_image(img, size=14):

    WIDTH, HEIGHT = (size, size)
    small_img = img.resize((WIDTH, HEIGHT), Image.NEAREST)

    emoji = ""
    small_img = small_img.load()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            emoji += find_closest_emoji(small_img[x, y])
        emoji += "\n"
    return emoji

player1 = ""
player2 = ""
turn = ""
gameOver = True

ttt_board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


logger = settings.logging.getLogger(__name__)


class fun_and_games(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def hack(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        wait_time = 3
        await ctx.reply(f":keyboard::robot: Hacking <@{member.id}>!")
        await ctx.send(embed=discord.Embed(
            title=f"Aquiring Email...",
            color=discord.Color.random()
        ))
        await asyncio.sleep(wait_time - 1)
        percent_one = random.randint(3, 38)
        await ctx.send(f"{percent_one}% done")
        await asyncio.sleep(wait_time - 1)
        percent_two = random.randint(41, 63)
        await ctx.send(f"{percent_two}% done")
        await asyncio.sleep(wait_time - 1)
        percent_three = random.randint(66, 92)
        await ctx.send(f"{percent_three}% done")
        await asyncio.sleep(wait_time - 1)
        await ctx.send("Email Hacked!")
        await asyncio.sleep(wait_time - 1)
        
        await ctx.send(embed=discord.Embed(
            title=f"Aquiring Passwords...",
            color=discord.Color.random()
        ))
        await asyncio.sleep(wait_time - 1)
        percent_one = random.randint(3, 38)
        await ctx.send(f"{percent_one}% done")
        await asyncio.sleep(wait_time - 1)
        percent_two = random.randint(41, 63)
        await ctx.send(f"{percent_two}% done")
        await asyncio.sleep(wait_time - 1)
        percent_three = random.randint(66, 92)
        await ctx.send(f"{percent_three}% done")
        await asyncio.sleep(wait_time - 1)
        await ctx.send("Passwords Hacked!")
        await asyncio.sleep(wait_time - 1)
        
        await ctx.send(embed=discord.Embed(
            title=f"Aquiring IP Address...",
            color=discord.Color.random()
        ))
        percent_one = random.randint(3, 47)
        await ctx.send(f"{percent_one}% done")
        await asyncio.sleep(wait_time - 1)
        percent_two = random.randint(51, 92)
        await ctx.send(f"{percent_two}% done")
        await asyncio.sleep(wait_time - 1)
        await ctx.send("IP Hacked!")
        embed = discord.Embed(title=f"{member.display_name} has been successfully hacked!", description=f"Click [here](https://homemade.sheepiegamer20.com/hacked-credentials/28ADJFE122HS721HG/) to see {member}'s credentials", color=discord.Color.random())
        await ctx.reply(embed=embed)
        await member.send("You have been hacked! (this is fake)")

    @commands.command()
    async def joke(self, ctx, nsfw: bool = False):
        if not nsfw:
            j = await Jokes()
            blacklist=['nsfw', 'religious', 'political', 'racist', 'sexist']
            joke = await j.get_joke(blacklist=blacklist)
            if joke["type"] == "single":
                await ctx.reply(joke["joke"])
            else:
                msg = await ctx.reply(joke["setup"])
                await asyncio.sleep(1)
                await msg.reply(joke["delivery"])
        elif nsfw:
            j = await Jokes()
            blacklist=['religious', 'political', 'racist', 'sexist']
            joke = await j.get_joke(blacklist=blacklist)
            if joke["type"] == "single":
                await ctx.reply(joke["joke"])
            else:
                msg = await ctx.reply(joke["setup"])
                await asyncio.sleep(1)
                await msg.reply(joke["delivery"])

    @commands.hybrid_command(help="", brief="", enabled=True, hidden=False)
    async def slap(self, ctx, using: str = "fish"):
        await ctx.reply(f"{ctx.author.display_name} slaps {random.choice(ctx.guild.members)} using {using}")

    @commands.command(aliases=[''], hidden=True)
    async def aaaaaaaaaaaaaaaaaaaaaaa(self, ctx):
        await ctx.reply("You have found the secret command. Good job. Have a cookie :cookie:")

    @commands.hybrid_command(help="", brief="", enabled=True, hidden=False)
    async def say(self, ctx,*, what_to_say):
        await ctx.reply(what_to_say)

    @commands.command()
    async def tictactoe(self, ctx, p1: discord.Member):
        p2 = ctx.author
        """plays a game of tictactoe in discord, mention your opponent!"""
        global count
        global player1
        global player2
        global turn
        global gameOver

        if gameOver:
            global ttt_board
            ttt_board = [":one:", ":two:", ":three:",
                    ":four:", ":five:", ":six:",
                    ":seven:", ":eight:", ":nine:"]
            turn = ""
            gameOver = False
            count = 0

            player1 = p1
            player2 = p2

            line = ""
            for x in range(len(ttt_board)):
                if x == 2 or x == 5 or x == 8:
                    line += " " + ttt_board[x]
                    await ctx.send(line)
                    line = ""
                else:
                    line += " " + ttt_board[x]

            # determine who goes first
            num = random.randint(1, 2)
            if num == 1:
                turn = player1
                await ctx.send("It is <@" + str(player1.id) + ">'s turn. Do s!place followed by the square you would like to mark")
            elif num == 2:
                turn = player2
                await ctx.send("It is <@" + str(player2.id) + ">'s turn. Do s!place followed by the square you would like to mark")
        else:
            embed = discord.Embed(title="A game is already in progress! Finish it before starting a new one.", color=discord.Color.random())
            await ctx.send(embed=embed)

    @commands.command()
    async def place(self, ctx, pos: int):
        """a command for tictactoe, do s!place while in a game of tictactoe, followed by the selected area you would like to mark"""
        global turn
        global player1
        global player2
        global ttt_board
        global count
        global gameOver

        if not gameOver:
            mark = ""
            if turn == ctx.author:
                if turn == player1:
                    mark = ":orange_circle:"
                elif turn == player2:
                    mark = ":red_circle:"
                if 0 < pos < 10 and ttt_board[pos - 1] == ":one:" or 0 < pos < 10 and ttt_board[pos - 1] == ":two:"  or 0 < pos < 10 and ttt_board[pos - 1] == ":three:" or 0 < pos < 10 and ttt_board[pos - 1] == ":four:" or 0 < pos < 10 and ttt_board[pos - 1] == ":five:" or 0 < pos < 10 and ttt_board[pos - 1] == ":six:" or 0 < pos < 10 and ttt_board[pos - 1] == ":seven:" or 0 < pos < 10 and ttt_board[pos - 1] == ":eight:" or 0 < pos < 10 and ttt_board[pos - 1] == ":nine:":
                    ttt_board[pos - 1] = mark
                    count += 1

                    line = ""
                    for x in range(len(ttt_board)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + ttt_board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + ttt_board[x]

                    self.checkWinner(winningConditions, mark)
                    if gameOver == True:
                        await ctx.send(mark + " wins!")
                    elif count >= 9:
                        gameOver = True
                        await ctx.send("It's a tie!")

                    # switch turns
                    if turn == player1:
                        turn = player2
                    elif turn == player2:
                        turn = player1
                else:
                    await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
            else:
                await ctx.send("It is not your turn.")
        else:
            await ctx.send("Please start a new game using the !tictactoe command.")

    def checkWinner(self, winningConditions, mark):
        global gameOver
        for condition in winningConditions:
            if ttt_board[condition[0]] == mark and ttt_board[condition[1]] == mark and ttt_board[condition[2]] == mark:
                gameOver = True

    @tictactoe.error
    async def tictactoe_error(ctx, error):
        print(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Please mention 2 players for this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.reply("Please make sure to mention/ping players (ie. <@1123692582006956042>).")

    @place.error
    async def place_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Please enter a position you would like to mark.")
        elif isinstance(error, commands.BadArgument):
            await ctx.reply("Please make sure to enter an integer.")

    @commands.command()
    async def emojify(self, ctx, url: Union[discord.Member, str], size: int = 14, help="turns an image url into an array of emojis"):
        """turns an image url into an array of emojis"""
        if not isinstance(url, str):
            url = url.display_avatar.url

        def get_emojified_image():
            r = requests.get(url, stream=True)
            image = Image.open(r.raw).convert("RGB")
            res = emojify_image(image, size)

            if size > 14:
                res = f"```{res}```"
            return res

        result = await self.bot.loop.run_in_executor(None, get_emojified_image)
        await ctx.reply(result)


async def setup(bot):
    await bot.add_cog(fun_and_games(bot))