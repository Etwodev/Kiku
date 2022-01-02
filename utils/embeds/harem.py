import discord, random, datetime, utils.referencing

class HaremEmbed:
    def __init__(self, ctx):
        self.ctx = ctx
        self.embed = discord.Embed()
        self.embed.timestamp = datetime.datetime.utcnow()
        self.embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        self.embed.color = random.choice([0x968FBF, 0xC39F14, 0xEF938C, 0x6F8452])
        
    def InviteEmbed(self, mention: discord.User, url: str):
        self.embed.title = f"{self.ctx.author.name} invites {mention.name} into their harem!"
        self.embed.description = "Do they accept?"
        self.embed.set_image(url=url)
        
    def LeaveEmbed(self, profile: utils.referencing.HaremHeader, harem: discord.User, url: str):
        self.embed.title = f"{self.ctx.author.name} leaves {harem.name}'s Harem!"
        self.embed.set_image(url=url)
        
    def EndEmbed(self, profile: utils.referencing.HaremHeader, url: str):
        self.embed.title = f"{self.ctx.author.name}'s harem has ended"
        self.embed.description = "What a sad day..."
        self.embed.set_image(url=url)
        
    def CreateEmbed(self, profile: utils.referencing.HaremHeader, url: str):
        self.embed.title = f"{self.ctx.author.name} has started a harem!"
        self.embed.description = "How far will you go?"
        self.embed.set_image(url=url)
        
    def OwnerEmbed(self, owner: discord.User, harem: list):
        self.embed.title = f"{owner.name}'s Harem"
        for i, user in enumerate(harem):
            self.embed.add_field(name=i+1, value=user)