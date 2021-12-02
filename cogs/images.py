import discord
from discord.ext import commands
from utils import api, definitions, handle, web, pillows





class images(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.file_types = definitions.file_types()
        self.embeds = definitions.embeded()

    @commands.command()
    async def glitch(self, ctx, size: int):
        if 0 > int(size) or int(size) >= 10:
            raise commands.UserInputError("Size must be an integer between 10 and 0!")
        url, file_type = api.predicate(await ctx.channel.history(limit=200).find(api.predicate))
        img = await web.get(url, fmt="read")
        if file_type in self.file_types.glitch:
            img, file_name = await handle.glitch_handler(img, size)
            await ctx.reply(embed=self.embeds.glitcher(img, file_name), file=img)
        else:
            raise commands.UserInputError("File type must be .png or .jpg!")

    @commands.command()
    async def polarize(self, ctx, bits: int):
        if 0 > int(bits) or int(bits) >= 9:
            raise commands.UserInputError("Size must be an integer between 10 and 0!")
        url, file_type = api.predicate(await ctx.channel.history(limit=200).find(api.predicate))
        img = await web.get(url, fmt="read")
        if file_type in self.file_types.polarize:
            img, file_name = await handle.polarize_handler(img, int(bits))
            await ctx.reply(embed=self.embeds.polarizer(img, file_name), file=img)
        else:
            raise commands.UserInputError("File type must be .png or .jpg!")

    @commands.command()
    async def duotone(self, ctx, color1: str, color2: str):
        if not api.is_hex(color1) or not api.is_hex(color2):
            raise commands.UserInputError("Please use hex colour codes! Try [this](https://htmlcolorcodes.com/color-picker/) site.")
        url, file_type = api.predicate(await ctx.channel.history(limit=200).find(api.predicate))
        img = await web.get(url, fmt="read")
        if file_type in self.file_types.duotone:
            img, file_name = await handle.duotone_handler(img, api.hex_to_rgb(color1), api.hex_to_rgb(color2))
            await ctx.reply(embed=self.embeds.duotoner(img, file_name), file=img)
        else:
            raise commands.UserInputError("File type must be .png or .jpg!")

    @commands.command()
    async def deepfry(self, ctx):
        url, file_type = api.predicate(await ctx.channel.history(limit=200).find(api.predicate))
        img = await web.get(url, fmt="read")
        if file_type in self.file_types.deepfry:
            img, file_name = await pillows.deepfry(img)
            await ctx.reply(embed=self.embeds.deepfry(img, file_name), file=img)
        else:
            raise commands.UserInputError("File type must be .png or .jpg!")

def setup(client):
    client.add_cog(images(client))