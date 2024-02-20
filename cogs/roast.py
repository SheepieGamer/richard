import discord
import asyncio
from discord.ext import commands
import settings
import random
import json
from time import time
from discord.ext.commands import (BucketType, Context, MemberConverter,
                                  cooldown, max_concurrency)
from roastedbyai import (CharacterLimitExceeded, Conversation,
                         MessageLimitExceeded)

logger = settings.logging.getLogger(__name__)

with open("database/roast.json", "r", encoding="UTF-8") as f:
  roasts = json.load(f)
f.close()
mc = MemberConverter()
class PromptButtons(discord.ui.View):

  def __init__(self, *, timeout=180):
    self.msg: discord.Message = None
    self.ctx: Context = None
    super().__init__(timeout=None)

  @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, custom_id="confirmRoast")
  async def confirm_button(self, interaction: discord.Interaction,
                            button: discord.ui.Button):
#    if interaction.user.id != self.ctx.author.id:
#      await interaction.response.send_message("This is not your roast battle.", ephemeral=True)
#      return
    await self.msg.edit(
      content=
      "You accepted the roast battle. May the biggest chicken be the hottest roast.",
      view=None)
    msg = await self.ctx.reply(
      f"{self.ctx.author.mention} Alright, give me your best roast and we'll take turns.\nIf you want to stop, simply click the button or send \"stop\" or \"quit\"."
    )
    await _roast_battle(self.ctx, prev_msg=msg)

  @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, custom_id="cancelRoast")
  async def cancel_button(self, interaction: discord.Interaction,
                          button: discord.ui.Button):
    if interaction.user.id != self.ctx.author.id:
      await interaction.response.send_message("This is not your roast battle.",
                                              ephemeral=True)
      return
    await self.msg.edit(
      content="You cancelled and chickened out of the roast battle.",
      view=None)


class RoastBattleCancel(discord.ui.View):

  def __init__(self, *, timeout=180):
    self.ctx: Context = None
    self.convo: Conversation = None
    super().__init__(timeout=None)

  @discord.ui.button(label="Stop", style=discord.ButtonStyle.grey, custom_id="roastStop")
  async def stop_button(self, interaction: discord.Interaction,
                        button: discord.ui.Button):
#    if interaction.user.id != self.ctx.author.id:
#      await interaction.response.send_message("This is not your roast battle.",
#                                              ephemeral=True)
#      return
    self.convo.kill()
    self.convo.killed = True
    await interaction.message.edit(content=interaction.message.content,
                                   view=None)
    await interaction.response.send_message("Boo, you're no fun.")
    return


async def _roast_battle(ctx: Context, prev_msg: discord.Message):
  convo = Conversation()

  def check(m: discord.Message):
    return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

  while convo.alive is True:
    try:
      msg: discord.Message = await ctx.bot.wait_for("message",
                                                check=check,
                                                timeout=300)
      response = None
      while response is None:
        try:
          if hasattr(convo, "killed"):
            return
          ctx.typing()
          if msg.content.lower() in ["stop", "quit"]:
            await ctx.channel.send(
              f"{ctx.author.mention} you're so lame bro, chickening out like this. "
              f"But I wouldn't want to hurt your few little braincells much more, buh-bye."
            )
            convo.kill()
            return
          else:
            response = convo.send(msg.content)
        except TimeoutError:
          asyncio.sleep(1)
          await ctx.reply(
            f"{ctx.author.mention} I'm too tired to continue talking right now, buh-bye."
          )
          convo.kill()
          return
        except MessageLimitExceeded:
          await ctx.reply(
            "It's been enough roasting now, I can already smell you're starting to burn..."
          )
          return
        except CharacterLimitExceeded:
          await ctx.reply(
            "Too much to read. Send 250 characters maximum, no need to write a whole book about me!\nCome on, try again!"
          )
          break
        else:
          await prev_msg.edit(content=prev_msg.content, view=None)
          rbc = RoastBattleCancel()
          prev_msg = await msg.reply(response, view=rbc)
          rbc.ctx = ctx
          rbc.convo = convo
    except TimeoutError:
      convo.kill()
  if convo.alive:
    convo.kill()


async def _roast_someone(ctx: Context, target: discord.Member | None = None):
  """Roast someone :smiling_imp:"""
  if target is None:
    dumb = ["do ``r!roast @mention`` to roast somebody once, or ``r!roast me`` for a roast battle "]
    await ctx.reply(random.choice(dumb))
    return
  elif target.id == ctx.author.id:
    dumb = [
      "Look in the mirror, there's my roast. Now next time give me someone else to roast",
      "Why do you even wanna roast yourself?",
      "https://tenor.com/view/roast-turkey-turkey-thanksgiving-gif-18067752",
      "You get no bitches, so lonely you're even trying to roast yourself...",
      "Stop roasting yourself, there's so many roasts ready to use on others",
      "Cooking up the perfect roast... Roast ready at <t:{}:f>".format(
        int(time() + random.randint(50_000, 500_000_000))),
      "Don't tell me there's {} other people to roast, and out of all those people you want to roast yourself??"
      .format(ctx.guild.member_count - 1),
      "Are you okay? Do you need mental help? Why is your dumbass trying to roast itself..."
    ]
    await ctx.reply(random.choice(dumb))
    return
  elif target.id == ctx.bot.user.id:
    dumb = [
      "You really think I'm gonna roast myself? :joy:",
      "You're just dumb as hell for thinking I would roast myself...",
      "Lol no", "Sike you thought. I'm not gonna roast myself, dumbass.",
      "I'm not gonna roast myself, so instead I'll roast you.\n",
      "Buddy, do you really think you're so funny? I might just be a Discord bot, but I'm not gonna roast myself :joy::skull:",
      "I'm just perfect, there's nothing to roast about me :angel:"
    ]
    await ctx.reply(random.choice(dumb))
  initroast = random.choice(roasts)
  roast_expl = None
  if type(initroast) is list:
    _roast = initroast[0].replace("{mention}",
                                  f"**{target.display_name}**").replace(
                                    "{author}",
                                    f"**{ctx.author.display_name}**")
    roast_expl = initroast[1].replace("{mention}",
                                      f"**{target.display_name}**").replace(
                                        "{author}",
                                        f"**{ctx.author.display_name}**")
  else:
    _roast = initroast
  roast = f"{target.mention} " + _roast

  def check(msg):
    return msg.channel.id == ctx.channel.id and msg.content.lower().startswith(
      ("what", "what?", "i dont get it", "i don't get it"))

  await ctx.channel.send(roast)
  if roast_expl:
    try:
      msg: discord.Message = await ctx.bot.wait_for("message",
                                                check=check,
                                                timeout=15)
      ctx.typing()
      asyncio.sleep(1.5)
      await msg.reply(roast_expl)
    except Exception as e:
      raise e






class Roast(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roast")
    @max_concurrency(1, BucketType.user)
    @max_concurrency(4, BucketType.channel)
    @cooldown(1, 15, BucketType.user)
    async def _roast(self, ctx: Context, target: str = None):
        """
        Start an AI roast session. Take turns in roasting the AI and the AI roasting you.
        If you want to stop, simply say "stop" or "quit".

        Subcommands:
        > - `me`: start a roast battle with the AI
        > - `@mention` | `<username>`: roast someone else

        Cooldown:
        > Once every minute per user

        Concurrency:
        > Maximum of 1 session per user at the same time
        > Maximum of 4 sessions per channel at the same time
        """
        if target != "me":
            try:
                target = await mc.convert(ctx, target)
            except:
                target = None
            await _roast_someone(ctx, target)
            return
        pb = PromptButtons()
        msg = await ctx.reply(
        "We'll be taking turns in trying to roast each other. Are you sure you can handle this and want to continue?",
        view=pb)
        pb.msg = msg
        pb.ctx = ctx

    @_roast.error
    async def command_name_error(self,ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"You're on cooldown!",description=f"Try again in {error.retry_after:.2f}s.")
            await ctx.reply(embed=em)  

async def setup(bot):
    await bot.add_cog(Roast(bot))