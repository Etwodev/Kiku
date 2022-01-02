import discord, random, utils.referencing, datetime

class ProfilesEmbed:
    def __init__(self, ctx):
        self.ctx = ctx
        self.embed = discord.Embed()
        self.embed.timestamp = datetime.datetime.utcnow()
        self.embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        self.embed.color = random.choice([0x968FBF, 0xC39F14, 0xEF938C, 0x6F8452])
        
    def MarryEmbed(self, url: str, message=None):
        self.embed.title = f"{self.ctx.author.name} proposes to {self.ctx.message.mentions[0].name}!"
        self.embed.set_image(url=url)
        self.embed.set_footer(text=self.ctx.message.mentions[0].id)
        if message:
            self.embed.add_field(name="They say...", value=message)
        
    def DivorceEmbed(self, url: str, divorcee: discord.User):
        self.embed.title = f"{self.ctx.author.name} just divorced {divorcee.name}!"
        self.embed.set_image(url=url)
        
    def AfkEmbed(self, message=None):
        self.embed.title = "Your afk message has been set to:"
        if message:
            self.embed.description = '"' + message + '"'
        
    def ProfileEmbed(self, profile: utils.referencing.ProfileHeader, married: None):
        self.embed.title = f"{profile.user.name}'s Profile"
        if profile.is_afk():
            self.embed.description = "User is currently afk!"
        else:
            self.embed.description = "User is not afk!"
        self.embed.add_field(name="Account created at:", value=profile.user.created_at.__format__("%m/%d/%Y, %H:%M:%S"), inline=False)
        date = datetime.datetime.strptime(profile.date, "%Y-%m-%d %H:%M:%S.%f")
        self.embed.add_field(name="Profile created at:", value=date.strftime("%m/%d/%Y, %H:%M:%S"), inline=False)
        if married:
            self.embed.add_field(name="Married to:", value=married.name, inline=False)
            self.embed.set_image(url=married.avatar_url)