import discord, random, utils.config, datetime, utils.parsing

class InfoEmbed:
    def __init__(self, ctx):
        self.ctx = ctx
        self.embed = discord.Embed()
        self.config = utils.config.get("config.json")
        self.embed.timestamp = datetime.datetime.utcnow()
        self.embed.set_footer(text=self.ctx.author.name, icon_url=self.ctx.author.avatar_url)
        self.embed.color = random.choice([0x968FBF, 0xC39F14, 0xEF938C, 0x6F8452])
        
    def HelpEmbed(self):
        self.embed.title = "Commands List"
        self.embed.description = "Click the above link to visit the list of commands!"
        self.embed.url = self.config.links.commands
        
    def VoteEmbed(self):
        self.embed.title = "Vote for Ayako"
        self.embed.description = "Click on the link above to vote for Ayako!"
        self.embed.url = self.config.links.vote
        
    def GiveawayEmbed(self, msg: str):
        self.embed.title = f"Giveaway has started!"
        self.embed.description = f"'{msg}' is being given away..."
        
    def ChoiceEmbed(self, items: list):
        self.embed.title = "I have chosen:"
        self.embed.description = random.choice(items)
        
    def EmoteEmbed(self, emote: utils.parsing.PartialMessageEmoji, is_animated: bool):
        self.embed.title = "Here is your emote!"
        if is_animated:
            emote.emoji_url = f"https://cdn.discordapp.com/emojis/{emote.emoji_id}.gif"
        self.embed.set_image(url=emote.emoji_url)
        
    def PingEmbedA(self):
        self.embed.title = "Pong!"
        
    def PingEmbedB(self, ms: str):
        self.embed.description = f"Client took {ms}ms to respond!"
        
    def PollEmbed(self, msg: str):
        self.embed.title = f"{self.ctx.author.name} asks,"
        self.embed.description = '"' + msg + '"'