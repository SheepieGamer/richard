import aiohttp, settings, discord
from discord.ext import commands, tasks

logger = settings.logging.getLogger(__name__)




amount_cmds = 0

class AutorespondBot(commands.Cog):

    message_list = list()

    def __init__(self, bot):
        self.bot = bot
        file = open("amount-cmds.txt", "r")
        self.amount_cmds = int(file.readline(-1))
        file.close()
        self.update_file.start()

    def cog_unload(self) -> None:
        self.update_file.stop()

    @commands.Cog.listener(name="on_message")
    async def on_message(self, message):
        if message.content.startswith(self.bot.command_prefix):
            self.amount_cmds += 1
        if not message.author.bot:
            if not message.content.startswith(self.bot.command_prefix):
                if len(self.message_list) > 0:
                    for respond_config in self.message_list:
                        if respond_config['trigger'] in message.content:
                            await message.channel.send(respond_config['message'])
                            break 
        # await commands.process_commands(message)

    @tasks.loop(seconds=5)
    async def update_file(self):
        file = open("amount-cmds.txt", "w+")
        file.write(str(self.amount_cmds)+"\n")


    # gpt
    @commands.Cog.listener(name="on_message")
    async def on_mention(self, message):
        if self.bot.user in message.mentions:
            if message.author.id != self.bot.user.id:
                await message.channel.typing()
        try:
            msg = message.content.split("<@1167904817922977933>")[1]
        except IndexError:
            msg = message
        if message.author.id != self.bot.user.id and not message.author.bot and self.bot.user in message.mentions:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{settings.AI_API}&uid={message.author.id}&msg={msg}") as r:
                    if r.status != 200:
                        if msg == "" or msg == " ":
                            return await message.reply("Please supply some text after ``@mentioning`` me")
                        return await message.reply("An error occured while accessing the chat API! ")
                    j = await r.json()
                    await message.reply(j['cnt'], mention_author=True)
        # await commands.process_commands(message)

    @commands.group()
    async def autorespond(self, ctx):
        ...

    @autorespond.command()
    async def create(self, ctx, trigger: str = "Hi", answer: str = "Hello!"):
        respond_config = {
            'trigger': trigger,
            "message": answer
        }
        self.message_list.append(respond_config)
        await ctx.reply(f"Now listening for **{trigger}**. Will respond with **{answer}**")

    @autorespond.command()
    async def edit(self, ctx, index: int, answer: str):
        self.message_list[index]["message"] = answer
        await ctx.reply(f"Successfully edited the answer of index {index} to {answer}")

    @autorespond.command()
    async def delete(self, ctx, index: int):
        self.message_list.pop(index)
        await ctx.reply(f"Successfully deleted index {index}")

    @autorespond.command()
    async def show(self, ctx,):
        result = "This is the configuration. Use the index at the front to edit and delete\n"
        code = "```"
        for index, item in enumerate(self.message_list):
            code += f"{index}: {item['trigger']} -> {item['message']}\n"
        code += "```"
        result += code
        await ctx.reply(result)
        

async def setup(bot):
    await bot.add_cog(AutorespondBot(bot))