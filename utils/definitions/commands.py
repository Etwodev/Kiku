import discord, datetime
from utils import startup

class commands(object):
    """Defines the embeds for each function
    """
    def __init__(self):
        self.config = startup.get("config.json")

    def emote_primary_clean(self, ctx, emote_name: str, emote_url: str):
        embed = discord.Embed(title=(f"{ctx.author.name} requests the emote: {emote_name}"), color=0xc83737)
        embed.set_image(url=emote_url)
        embed.set_footer(text=f"{datetime.datetime.now().__format__('Today at %H:%M:%S')} | {ctx.author.id}")
        return embed
    
    def afk_primary_clean(self, ctx, afk_message: str):
        embed = discord.Embed(title=f"{ctx.author.name}, you are now afk!", color=0xc83737)
        embed.add_field(name="Your afk message has been set to:", value=afk_message)
        return embed

    def poll_primary_clean(self, ctx, question: str):
        embed = discord.Embed(title=f"{ctx.author.name}, asks:", description=(question), color=0xc83737)
        embed.set_footer(text="Poll in progress...")
        return embed

    def help_primary_clean(self):
        embed = discord.Embed(title="Commands List.", url=self.config.links.commands, description="Click the above link to visit the commands page.", color=0x344c93)
        return embed

    def reactions_primary_clean(self):
        embed=discord.Embed(title="Add Reaction Gifs.", url="https://waifu.pics/upload", description="Click on the link above to visit the upload page.")
        embed.set_footer(text="Here, you can upload your own anime gifs to be used by the bot.")
        return embed

    def ping_primary_loading(self):
        embed = discord.Embed(title=('Pong!'), color=0xbb54aa)
        return embed

    def ping_secondary_clean(self, ms):
        embed = discord.Embed(title=('Pong!'), description=(f'Client took {ms}ms to send to discord.'), color=0xbb54aa)
        return embed

    def glitch_primary_clean(self, img, file_name):
        embed = discord.Embed(title="Glitching has finished!", description=("Here is your image."), color=0xc83737)
        embed.set_image(url=f"attachment://{file_name}")
        return embed

    def saucenao_primary_clean(self, results):
        embed = discord.Embed(title=(f'{results[0].title}'), url=(results[0].urls[0]), description=(f'{results[0].similarity}% Similarity'), color=0xc83737)
        embed.set_author(name=results[0].author)
        embed.set_thumbnail(url=results[0].thumbnail)
        return embed

    def polarize_primary_clean(self, img, file_name):
        embed = discord.Embed(title="Image has been polarized!", description=("Here is your image."), color=0xc83737)
        embed.set_image(url=f"attachment://{file_name}")
        return embed

    def duotone_primary_clean(self, img, file_name):
        embed = discord.Embed(title="Duotone has finished!", description=("Here is your image."), color=0xc83737)
        embed.set_image(url=f"attachment://{file_name}")
        return embed

    def deepfry_primary_clean(self, img, file_name):
        embed = discord.Embed(title="Deepfrying has finished!", description=("Here is your image."), color=0xc83737)
        embed.set_image(url=f"attachment://{file_name}")
        return embed

    def lookup_primary_loading(self):
        embed = discord.Embed(title="Loading...", color=0xc83737)
        return embed

    def lookup_secondary_urlclean(self, url):
        embed = discord.Embed(title="Here you go!", description=("Enjoy..."), color=0xc83737)
        embed.set_image(url=url)
        return embed

    def lookup_secondary_fileclean(self, img, file_name):
        embed = discord.Embed(title="Here you go!", description=("Enjoy..."), color=0xc83737)
        embed.set_image(url=f"attachment://{file_name}")
        return embed

    def tag_primary_clean(self, results, tag):
        embed = discord.Embed(title=f"I found '{len(results)}' matches for '{tag}'!", color=0xc83737)
        for i, x in enumerate(results):
            embed.add_field(name=x, value=i)
        return embed

    def tag_primary_none(self):
        embed = discord.Embed(title=f"I found no matching tags...", color=0xc83737)
        return embed