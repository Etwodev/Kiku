from utils import startup

class errors(object):
    '''Defines the error messages for each error
    '''
    def __init__(self):
        self.config = startup.get("config.json")

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