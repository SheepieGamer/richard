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

    def get_random_cat_local_image():
        cat_images = pathlib.Path(settings.BASE_DIR / "images" / "cats").glob("**/*")
        return random.choice(list(cat_images))

    def get_random_dog_image_url():
        url = "https://dog.ceo/api/breeds/image/random"
        res = requests.get(url)
        data = res.json()
        if "message" in data:
            return data["message"]
        return None

    @commands.command()
    async def dog(self, ctx):
        random_dog_image = self.get_random_dog_image_url()
        if not random_dog_image:
            await ctx.reply("The API didn't respond. Try again later")
            return

        embed = discord.Embed(title="Woof!", color=discord.Color.random())
        embed.set_image(url=random_dog_image)
        await ctx.reply(embed=embed)



    @commands.command()
    async def cat(self, ctx):
        random_cat_image = self.get_random_cat_image_url()
        if not random_cat_image:
            await ctx.reply("The API didn't respond. Try again later")
            return

        embed = discord.Embed(title="Meow!", color=discord.Color.random())
        embed.set_image(url=random_cat_image)
        await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Animals(bot))