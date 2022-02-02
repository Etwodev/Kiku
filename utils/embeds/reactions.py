from typing_extensions import Self
import discord, random, utils.referencing, datetime

class ReactionsEmbed:
    def __init__(self, ctx, client, url: str, msg):
        self.ctx = ctx
        self.url = url
        self.client = client
        self.msg = msg
        self.embed = discord.Embed()
        self.embed.set_image(url=self.url)
        self.embed.timestamp = datetime.datetime.utcnow()
        self.embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        self.embed.color = random.choice([0x968FBF, 0xC39F14, 0xEF938C, 0x6F8452])
    
    def HugEmbed(self):
        if self.ctx.message.mentions[0] == self.client.user:
            self.embed.title = random.choice(["You... just hugged me...", "Eh-eh? A- hug? I... guess it's ok."])
            self.embed.description = random.choice(["T-thank you...", "You feel warm..."])
        elif self.ctx.message.mentions[0] == self.ctx.author:
            self.embed.title = "Here, I'll hug you instead"
            self.embed.description = "There there, it'll be ok..."
        else:
            self.embed.title = f"{self.ctx.author.name} just hugged {self.ctx.message.mentions[0].name}!"
            self.embed.description = "Aww, how cute!"
        if self.msg:
            self.embed.add_field(name="They say...", value=self.msg)