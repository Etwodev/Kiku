import discord, datetime
from utils import startup

class file_types(object):
    """Defines the file_types for each function
    """
    def __init__(self):
        self.glitch = ["jpg", "jpeg", "png"]
        self.saucenao = ["jpg", "jpeg", "png", "gif"]
        self.polarize = ["jpg", "jpeg", "png"]
        self.duotone = ["jpg", "jpeg", "png"]
        self.deepfry = ["jpg", "jpeg", "png"]
        self.lookup = ["jpg", "jpeg", "png", "gif", "mov", "mp4", "webm"]
        self.lookup_ext = ["mov", "mp4", "webm"]
        self.config = startup.get("config.json")


class embeded(object):
    """Defines the embeds for each function
    """
    def __init__(self):
        self.config = startup.get("config.json")

    def on_ready(self, client):
        embed = discord.Embed(title=("Bot has started!"), color=0xa68591)
        embed.set_author(name=f"{client.user.name}", icon_url=(client.user.avatar_url))
        embed.add_field(name="Version:", value=(self.config.version))
        embed.add_field(name="Logged in as:", value=(client.user.name))
        embed.add_field(name="Discord Version:", value=(discord.__version__))
        embed.set_footer(text=f"{datetime.datetime.now().__format__('%A, %d %B %Y @ %H:%M:%S')} | {client.user.id}")
        return embed

    def on_guild_join(self):
        embed = discord.Embed(title="Thank you for adding Ayako!", description="For a list of help commands, click [here](https://www.ayako.ga/help). If you need support, you can visit the support server [here](https://www.ayako.ga/support)!", color=0x968fbf)
        return embed

    def on_message(self, user: discord.User, value: str):
        embed = discord.Embed(title=f"{user.name} is currently afk!", color=0xc83737)
        embed.add_field(name="They say,", value=value, inline=True)
        return embed

    def emote(self, ctx, emote_name: str, emote_url: str):
        embed = discord.Embed(title=(f"{ctx.author.name} requests the emote: {emote_name}"), color=0xc83737)
        embed.set_image(url=emote_url)
        embed.set_footer(text=f"{datetime.datetime.now().__format__('Today at %H:%M:%S')} | {ctx.author.id}")
        return embed
    
    def afk(self, ctx, afk_message: str):
        embed = discord.Embed(title=f"{ctx.author.name}, you are now afk!", color=0xc83737)
        embed.add_field(name="Your afk message has been set to:", value=afk_message)
        return embed

    def create_poll(self, ctx, question: str):
        embed = discord.Embed(title=f"{ctx.author.name}, asks:", description=(question), color=0xc83737)
        embed.set_footer(text="Poll in progress...")
        return embed
    
    def end_poll(self, res, msg, file_name):
        YesRES = res["Yes"]
        NoRES = res["No"]
        AbstainRES = res["Abstain"]
        embed = discord.Embed(title="The poll has ended, and the results are in!", description=(f"Question: {msg}"), color=0xc83737)
        embed.add_field(name="Yes:", value=f"{YesRES} votes")
        embed.add_field(name="Abstained:", value=f"{AbstainRES} votes")
        embed.add_field(name="No:", value=f"{NoRES} votes")
        embed.set_image(url=f"attachment://{file_name}")
        return embed
    
    def CommandOnCooldown(self, err):
        msg = 'You are being ratelimited! Please try again in {:.2f}s'.format(err.retry_after)
        embed = discord.Embed(description=msg, color=0xc83737)
        return embed

    def MaxConcurrencyReached(self):
        msg = "You've reached max capacity of command usage at once, please finish the previous one..."
        embed = discord.Embed(description=msg, color=0xc83737)
        return embed

    def MissingPermissions(self):
        msg = "You need special permissions to use that command!"
        embed = discord.Embed(description=msg, color=0xc83737)
        return embed
    
    def MissingRequiredArgument(self, err):
        msg = f'Missing the required argument "{err.param}"! Please try the command again. Use "{self.config.prefix[0]}help" to get command-specific information.'
        embed = discord.Embed(description=msg, color=0xc83737)
        return embed

    def UserInputError(self, err):
        msg = f'Something went wrong with your input! {err}'
        embed = discord.Embed(description=msg, color=0xc83737)
        return embed

    def TooManyArguments(self):
        msg = f'Too many arguments! Please try the command again. Use "{self.config.prefix[0]}help" to get command-specific information.'
        embed = discord.Embed(description=msg, color=0xa68591)
        return embed

    def MessageNotFound(self):
        msg = "Failed to find a message, please try again."
        embed = discord.Embed(description=msg, color=0xa68591)
        return embed

    def ChannelNotFound(self):
        msg = "Failed to find the channel, please try again."
        embed = discord.Embed(description=msg, color=0xa68591)
        return embed

    def NSFWChannelRequired(self):
        msg = "Channel must be NSFW to use this command!"
        embed = discord.Embed(description=msg, color=0xa68591)
        return embed

    def NoPrivateMessage(self):
        msg = "This command cannot be used in private messages."
        embed = discord.Embed(description=msg, color=0xa68591)
        return embed

    def Forbidden(self):
        msg = "I was unable to do that... Sorry!"
        embed = discord.Embed(description=msg, color=0xa68591)
        embed.add_field(name="Is this a DM?", value="Check your message permissions!")
        embed.add_field(name="Something else?", value="Try resending the command!")
        return embed

    def BadArgument(self):
        msg = f'Bad argument! Are you inputting string for an amount? Try using "{self.config.prefix[0]}help" for more information...'
        embed = discord.Embed(description=msg, color=0xc83737)
        return embed

    def UnknownDiscordError(self):
        msg = "I don't know what happened, sorry! Please try again."
        embed = discord.Embed(description=msg, color=0xa68591)
        return embed

    def help(self):
        embed = discord.Embed(title="Commands List.", url="https://www.ayako.ga/commands", description="Click the above link to visit the commands page.", color=0x344c93)
        return embed

    def reactions(self):
        embed=discord.Embed(title="Add Reaction Gifs.", url="https://waifu.pics/upload", description="Click on the link above to visit the upload page.")
        embed.set_footer(text="Here, you can upload your own anime gifs to be used by the bot.")
        return embed

    def ping_discord_a(self):
        embed = discord.Embed(title=('Pong!'), color=0xbb54aa)
        return embed

    def ping_discord_b(self, ms):
        embed = discord.Embed(title=('Pong!'), description=(f'Client took {ms}ms to send to discord.'), color=0xbb54aa)
        return embed

    def glitcher(self, img, file_name):
        embed = discord.Embed(title="Glitching has finished!", description=("Here is your image."), color=0xc83737)
        embed.set_image(url=f"attachment://{file_name}")
        return embed

    def saucenao(self, results):
        embed = discord.Embed(title=(f'{results[0].title}'), url=(results[0].urls[0]), description=(f'{results[0].similarity}% Similarity'), color=0xc83737)
        embed.set_author(name=results[0].author)
        embed.set_thumbnail(url=results[0].thumbnail)
        return embed

    def polarizer(self, img, file_name):
        embed = discord.Embed(title="Image has been polarized!", description=("Here is your image."), color=0xc83737)
        embed.set_image(url=f"attachment://{file_name}")
        return embed

    def duotoner(self, img, file_name):
        embed = discord.Embed(title="Duotone has finished!", description=("Here is your image."), color=0xc83737)
        embed.set_image(url=f"attachment://{file_name}")
        return embed

    def deepfry(self, img, file_name):
        embed = discord.Embed(title="Deepfrying has finished!", description=("Here is your image."), color=0xc83737)
        embed.set_image(url=f"attachment://{file_name}")
        return embed

    def lookup_rw(self, url):
        embed = discord.Embed(title="Here you go!", description=("Enjoy..."), color=0xc83737)
        embed.set_image(url=url)
        return embed

    def lookup_wt(self):
        embed = discord.Embed(title="Loading...", color=0xc83737)
        return embed

    def lookup_ld(self, img, file_name):
        embed = discord.Embed(title="Here you go!", description=("Enjoy..."), color=0xc83737)
        embed.set_image(url=f"attachment://{file_name}")
        return embed

    def tags(self, results, tag):
        if len(results) == 0:
            embed = discord.Embed(title=f"I found no matching tags...", color=0xc83737)
            return embed
        else:
            embed = discord.Embed(title=f"I found '{len(results)}' matches for '{tag}'!", color=0xc83737)
            for i, x in enumerate(results):
                embed.add_field(name=x, value=i)
            return embed
