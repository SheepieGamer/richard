import settings, discord, secrets
from string import ascii_letters, digits, punctuation

logger = settings.logging.getLogger(__name__)

async def print_user(bot):
    logger.info(f"User: {bot.user} (ID: {bot.user.id})")

async def load_cogs(bot):
    loaded = []
    for cog_file in settings.COGS_DIR.glob("*.py"):
        if cog_file.name != "__init__.py":
            await bot.load_extension(f"cogs.{cog_file.name[:-3]}")
            loaded.append("cogs." + cog_file.name[:-3])
    loaded_str = ""
    for i in loaded:
        loaded_str += f"{i}, "
    logger.info(f"{loaded_str} successfully loaded")

async def load_cmds(bot):
    loaded = []
    for cmd_file in settings.CMDS_DIR.glob("*.py"):
        if cmd_file.name != "__init__.py":
            await bot.load_extension(f"cmds.{cmd_file.name[:-3]}")
            loaded.append(cmd_file.name[:-3])
    loaded_str = ""
    for i in loaded:
        loaded_str += f"{i}, "
    logger.info(f"{loaded_str} successfully loaded") if loaded_str != "" else logger.info("no cmds to load")

async def other(bot):
    bot.tree.copy_global_to(guild=bot.guilds[0])
    await bot.tree.sync(guild=bot.guilds[0])
    logger.info("Tree synced")
    logger.info("--")
    logger.info("--")


# nothing after

games_list = {
    "unrailed": {
        "title": "Unrailed",
        "url": "https://cdn.cloudflare.steamstatic.com/steam/apps/1016920/header.jpg?t=1667079473"
    },
    "valorant": {
        "title": "Valorant",
        "url": "https://sm.ign.com/ign_in/screenshot/default/valorant-2_mdt7.jpg"
    },
    "csgo": {
        "title": "Counter-Strike: Global Offensive",
        "url": "https://cdn.cloudflare.steamstatic.com/steam/apps/730/header.jpg?t=1668125812"
    },
    "other": {
        "title": "a game",
        "url": "https://newmediaservices.com.au/wp-content/uploads/2022/01/customer-service-in-gaming-industry-importance-and-challenges.jpg"
    }
}

class ReadyOrNotView(discord.ui.View):

    joined_users = []
    declined_users = []
    tentative_users = []

    initiatior: discord.User = None
    players: int = 0

    async def send(self, interaction: discord.Interaction):
        self.joined_users.append(interaction.user.display_name)
        embed = self.create_embed()
        await interaction.response.send_message(view=self, embed=embed)
        self.message = await interaction.original_response()

    def convert_user_list_to_str(self, user_list, default_str="No one"):
        if len(user_list):
            return "\n".join(user_list) 
        return default_str

    def create_embed(self):
        desc = f"{self.initiatior.display_name} is looking for another {self.players - 1} players to play {self.game['title']}"
        embed = discord.Embed(title="Lets get together", description=desc)
        
        if self.game['url']:
            embed.set_image(url=self.game['url'])

        embed.add_field(inline=True, name="✅Joined", value=self.convert_user_list_to_str(self.joined_users))
        embed.add_field(inline=True, name="❌Declined", value=self.convert_user_list_to_str(self.declined_users))
        embed.add_field(inline=True, name="🔃Tentative", value=self.convert_user_list_to_str(self.tentative_users))

        return embed
    
    def check_players_full(self):
        if len(self.joined_users) >= self.players:
            return True
        return False

    def disable_all_buttons(self):
        self.join_button.disabled = True
        self.decline_button.disabled = True
        self.tentative_button.disabled = True

    async def update_message(self):
        if self.check_players_full():
            self.disable_all_buttons()

        embed = self.create_embed()
        await self.message.edit(view=self, embed=embed)

    @discord.ui.button(label="Join",
                       style=discord.ButtonStyle.green)
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

        if interaction.user.display_name not in self.joined_users:
            self.joined_users.append(interaction.user.display_name)
        if interaction.user.display_name in self.tentative_users:
            self.tentative_users.remove(interaction.user.display_name)
        if interaction.user.display_name in self.declined_users:
            self.declined_users.remove(interaction.user.display_name)

        await self.update_message()

    @discord.ui.button(label="Decline",
                       style=discord.ButtonStyle.red)
    async def decline_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

        if interaction.user.display_name not in self.declined_users:
            self.declined_users.append(interaction.user.display_name)
        if interaction.user.display_name in self.tentative_users:
            self.tentative_users.remove(interaction.user.display_name)
        if interaction.user.display_name in self.joined_users:
            self.joined_users.remove(interaction.user.display_name)

        await self.update_message()

    @discord.ui.button(label="Maybe",
                       style=discord.ButtonStyle.blurple)
    async def tentative_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

        if interaction.user.display_name not in self.tentative_users:
            self.tentative_users.append(interaction.user.display_name)
        if interaction.user.display_name in self.joined_users:
            self.joined_users.remove(interaction.user.display_name)
        if interaction.user.display_name in self.declined_users:
            self.declined_users.remove(interaction.user.display_name)

        await self.update_message()


def gen_pw(char: int = 10):
    return "".join(secrets.choice(ascii_letters + digits + punctuation) for i in range(int(char)))