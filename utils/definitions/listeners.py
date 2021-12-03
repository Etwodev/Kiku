import discord, datetime
from utils import startup

class listeners(object):
    """Defines the embeds for each function
    """
    def __init__(self):
        self.config = startup.get("config.json")

    def on_ready_primary_clean(self, client):
        embed = discord.Embed(title=("Bot has started!"), color=0xa68591)
        embed.set_author(name=f"{client.user.name}", icon_url=(client.user.avatar_url))
        embed.add_field(name="Version:", value=(self.config.version))
        embed.add_field(name="Logged in as:", value=(client.user.name))
        embed.add_field(name="Discord Version:", value=(discord.__version__))
        embed.set_footer(text=f"{datetime.datetime.now().__format__('%A, %d %B %Y @ %H:%M:%S')} | {client.user.id}")
        return embed

    def on_guild_join_primary_clean(self):
        embed = discord.Embed(title="Thank you for adding Ayako!", description=f"For a list of help commands, click [here]({self.config.links.help}). If you need support, you can visit the support server [here](https://www.ayako.ga/support)!", color=0x968fbf)
        return embed

    def on_message_primary_afk(self, user: discord.User, value: str):
        embed = discord.Embed(title=f"{user.name} is currently afk!", color=0xc83737)
        embed.add_field(name="They say,", value=value, inline=True)
        return embed

    def on_button_click_primary_endpoll(self, results: dict, msg: str, file_name: str):
        embed = discord.Embed(title="The poll has ended, and the results are in!", description=(f"Question: {msg}"), color=0xc83737)
        embed.add_field(name="Yes:", value=f"{results["Yes"]} votes")
        embed.add_field(name="Abstained:", value=f"{results["Abstain"]} votes")
        embed.add_field(name="No:", value=f"{results["No"]} votes")
        embed.set_image(url=f"attachment://{file_name}")
        return embed
