import discord, random, datetime

class FunEmbed:
    def __init__(self, ctx):
        self.ctx = ctx
        self.embed = discord.Embed()
        self.embed.timestamp = datetime.datetime.utcnow()
        self.embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        self.embed.color = random.choice([0x968FBF, 0xC39F14, 0xEF938C, 0x6F8452])

    def LookupLoadingEmbed(self):
        self.embed.title = "Your image is loading..."

    def LookupURLEmbed(self, url: str, score: int):
        self.embed.title = "Here you go!"
        self.embed.add_field(name="Score:", value=score)
        self.embed.description = "I hope you enjoy it..."
        self.embed.set_image(url=url)
        
    def BannerEmbed(self, url: str, user):
        self.embed.title = f"{user.name}'s Banner"
        self.embed.set_image(url=url)
        
    def ProfilePictureEmbed(self, url: str, user):
        self.embed.title = f"{user.name}'s Profile Picture"
        self.embed.set_image(url=url)
        
    def LookupFileEmbed(self, file_name: str, score: int):
        self.embed.title = "Here you go!"
        self.embed.add_field(name="Score:", value=score)
        self.embed.description = "I hope you enjoy it..."
        self.embed.set_image(url=f"attachment://{file_name}")

    def SauceNAOEmbed(self, results):
        self.embed.title = results[0].title
        self.embed.url = results[0].urls[0]
        self.embed.description = f"{results[0].similarity}% Similarity"
        self.embed.set_author(name=results[0].author)
        self.embed.set_thumbnail(url=results[0].thumbnail)

    def TagEmbed(self, results: list, tag: str):
        self.embed.title = f"Showing matches for {tag}..."
        self.embed.description = f"{len(results)} matches found!"
        for i, n in enumerate(results):
            self.embed.add_field(name=n, value=i+1, inline=False)
        