from discord.ext import commands
import discord
import requests
import pathlib
import settings
import random

logger = settings.logging.getLogger(__name__)


class Animals(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def get_random_cat_image_url():
        animal_you_want = 'cat'
        NUM_IMAGES = 1000
        num = random.randint(0, NUM_IMAGES+1)
        url = f"http://api.sheepiegamer20.com/images/{animal_you_want}/{animal_you_want}{num}.png"
        return url

    def get_random_dog_image_url():
        url = "https://dog.ceo/api/breeds/image/random"
        res = requests.get(url)
        data = res.json()
        if "message" in data:
            return data["message"]
        return None

    @commands.hybrid_command()
    async def dog(self, ctx):
        url = "https://dog.ceo/api/breeds/image/random"
        res = requests.get(url)
        data = res.json()
        if "message" in data:
            random_dog_image = data["message"]
        else:
            random_dog_image = None
        if not random_dog_image:
            await ctx.reply("The API didn't respond. Try again later")
            return
        embed = discord.Embed(title="Woof!", color=discord.Color.random())
        embed.set_image(url=random_dog_image)
        await ctx.reply(embed=embed)



    @commands.hybrid_command()
    async def cat(self, ctx):
        animal_you_want = 'cat'
        NUM_IMAGES = 1000
        num = random.randint(0, NUM_IMAGES+1)
        random_cat_image = f"http://api.sheepiegamer20.com/images/{animal_you_want}/{animal_you_want}{num}.png"
        if not random_cat_image:
            await ctx.reply("The API didn't respond. Try again later")
            return

        embed = discord.Embed(title="Meow!", color=discord.Color.random())
        embed.set_image(url=random_cat_image)
        await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Animals(bot))