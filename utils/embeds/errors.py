import discord, random, datetime
from utils import config

class ErrorsEmbed:
    def __init__(self, ctx, err):
        self.err = err
        self.ctx = ctx
        self.config = config.get("config.json")
        self.embed = discord.Embed()
        self.embed.title = "An error has occured!"
        self.embed.timestamp = datetime.datetime.utcnow()
        self.embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        self.embed.color = random.choice([0x968FBF, 0xC39F14, 0xEF938C, 0x6F8452])

    def CommandOnCooldown(self):
        self.embed.description = "You are being ratelimited! Please try again in {:.2f}s".format(self.err.retry_after)

    def MaxConcurrencyReached(self):
        self.embed.description = "You've reached max capacity of command usage at once, please finish the previous one..."

    def MissingPermissions(self):
        self.embed.description = "You need special permissions to use that command!"

    def MissingRequiredArgument(self):
        self.embed.description = f'Missing the required argument "{self.err.param}"! Please try the command again. Use "{self.config.prefix[0]}help" to get command-specific information.'

    def UserInputError(self):
        self.embed.description = str(self.err)

    def TooManyArguments(self):
        self.embed.description = f'Too many arguments! Please try the command again. Use "{self.config.prefix[0]}help" to get command-specific information.'
    
    def MessageNotFound(self):
        self.embed.description = "Failed to find a message, please try again."

    def ChannelNotFound(self):
        self.embed.description = "Failed to find the channel, please try again."

    def NSFWChannelRequired(self):
        self.embed.description = "This channel must be marked as 'NSFW' to be used!"

    def NoPrivateMessage(self):
        self.embed.description = "I'm, this command cannot be used in private messages."

    def Forbidden(self):
        self.embed.description = "I was forbidden from doing that! Am I blocked?"

    def BadArgument(self):
        self.embed.description = f'Invalid argument! Try using "{self.config.prefix[0]}help" for more information about commands...'

    def UnknownDiscordError(self):
        self.embed.description = "I don't know what happened, sorry! Please try again."
