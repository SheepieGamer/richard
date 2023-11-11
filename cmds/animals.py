import discord, requests, pathlib, settings, random
from discord.ext import commands


def get_random_cat_image_url():
    url = "https://api.thecatapi.com/v1/images/search"
    res = requests.get(url)
    data = res.json()
    if "url" in data:
        return data["url"]
    return None

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
async def dog(ctx):
    random_dog_image = get_random_dog_image_url()
    if not random_dog_image:
        await ctx.reply("The API didn't respond. Try again later")
        return

    embed = discord.Embed(title="Woof!", color=discord.Color.random())
    embed.set_image(url=random_dog_image)
    await ctx.reply(embed=embed)

@commands.command()
async def cat(ctx):
    random_cat_local_image = get_random_cat_local_image()
    cat_image_file = discord.File(random_cat_local_image, filename=random_cat_local_image.name)
    
    embed = discord.Embed(title="Meow?", color=discord.Color.random())
    embed.set_image(url=f"attachment://{random_cat_local_image.name}")
    await ctx.reply(embed=embed, file=cat_image_file)

@commands.command()
async def cat2(ctx):
    random_cat_image = get_random_cat_image_url()
    if not random_cat_image:
        await ctx.reply("The API didn't respond. Try again later")
        return

    embed = discord.Embed(title="Meow!", color=discord.Color.random())
    embed.set_image(url=random_cat_image)
    await ctx.reply(embed=embed)

async def setup(bot):
    bot.add_command(dog)
    bot.add_command(cat)
    bot.add_command(cat2)