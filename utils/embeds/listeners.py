import discord, random, utils.config, datetime, utils.parsing

class ListenersEmbed:
    def __init__(self):
        self.embed = discord.Embed()
        self.config = utils.config.get("config.json")
        self.embed.color = random.choice([0x968FBF, 0xC39F14, 0xEF938C, 0x6F8452])
        
    def MessageAFKEmbed(self, message, fields: dict):
        self.embed.title = "Someone was afk!"
        self.embed.timestamp = datetime.datetime.utcnow()
        self.embed.set_footer(text=message.author.name, icon_url=message.author.avatar_url)
        for key, value in fields.items():
            self.embed.add_field(name=key, value=value)
            
    def ButtonPollEmbed(self, message: str, file_name: str, results: dict):
        self.embed.title = "The poll has ended, and the results are in!"
        self.embed.description = f"Question: {message}"
        self.embed.add_field(name="Yes:", value=f"{results['Yes']} votes")
        self.embed.add_field(name="Abstained:", value=f"{results['Abstain']} votes")
        self.embed.add_field(name="No:", value=f"{results['No']} votes")
        self.embed.set_image(url=f"attachment://{file_name}")
        
    def ButtonMarriageYesEmbed(self, url: str, user_a: discord.User, user_b: discord.User):
        self.embed.title = f"{user_a.name} and {user_b.name} just married!"
        self.embed.description = "Congratulations!"
        self.embed.set_image(url=url)
        
    def ButtonMarriageNoEmbed(self, url: str, user: discord.User):
        self.embed.title = f"{user.name} was denied."
        self.embed.description = "What a bad day for rain..."
        self.embed.set_image(url=url)
  
    def ButtonHaremYesEmbed(self, url: str, user_a: discord.User, user_b: discord.User):
        self.embed.title = f"{user_a.name} just joined {user_b.name}'s harem!"
        self.embed.description = "Congratulations!"
        self.embed.set_image(url=url)
        
    def ButtonHaremNoEmbed(self, url: str, user: discord.User):
        self.embed.title = f"{user.name} got their harem invite denied."
        self.embed.description = "What a bad day for rain..."
        self.embed.set_image(url=url)
        
    def OnReadyEmbed(self, client):
        self.embed.title = "Bot has started!"
        self.embed.set_author(name=f"{client.user.name}", icon_url=(client.user.avatar_url))
        self.embed.add_field(name="Version:", value=(self.config.version))
        self.embed.add_field(name="Logged in as:", value=(client.user.name))
        self.embed.add_field(name="Pycord version:", value=(discord.__version__))
        self.embed.add_field(name="Servers joined:", value=len(client.guilds))
        self.embed.add_field(name="Modules loaded:", value=len(self.config.modules))
        self.embed.add_field(name="Seen users:", value=len(client.users))
        self.embed.set_footer(text=f"{client.user.id}")
        self.embed.timestamp = datetime.datetime.utcnow()
        
    def OnGuildEmbed(self, client: discord.Client, guild: discord.Guild):
        self.embed.timestamp = datetime.datetime.utcnow()
        self.embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
        self.embed.title = f"Thank you for adding me to {guild.name}!"
        self.embed.description = f"For a list of help commands, click [here]({self.config.links.commands}). Or if you need support, you can visit our website [here](https://www.ayako.one/support)!"
        self.embed.set_image(url="https://ayako.one/guild.png")