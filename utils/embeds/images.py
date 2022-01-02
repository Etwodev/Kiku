import discord, random, datetime

class ImageEmbed:
    def __init__(self, ctx, file_name):
        self.embed = discord.Embed()
        self.embed.timestamp = datetime.datetime.utcnow()
        self.embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        self.embed.set_image(url=f"attachment://{file_name}")
        self.embed.description = "Here is your image."
        self.embed.color = random.choice([0x968FBF, 0xC39F14, 0xEF938C, 0x6F8452])
        
    def GlitchEmbed(self):
        self.embed.title = "Image has been glitched!"
    
    def PolarizeEmbed(self):
        self.embed.title = "Image has been polarized!"
        
    def DeepfryEmbed(self):
        self.embed.title = "Deepfrying has finished!"
        
    def DuotoneEmbed(self):
        self.embed.title = "Duotone has finished!"