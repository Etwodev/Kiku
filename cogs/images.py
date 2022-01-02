from concurrent.futures import thread
import discord
from discord import file
from discord.ext import commands
from discord.ext.commands.errors import PartialEmojiConversionFailure
import utils.threading, utils.parsing, utils.web, utils.embeds.images, utils.config, utils.pillows

class images(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.embeds = utils.embeds.images
        self.parsing = utils.parsing
        self.threading = utils.threading
        self.web = utils.web
        self.file_types = utils.config.get("file_types.json")
        
    @commands.command()
    async def glitch(self, ctx, size: int):
        if int(size) < 0 or int(size) > 10:
            raise commands.UserInputError("Size must be an integer between 10 and 0!")
        url, file_type = self.parsing.ext_pred(await ctx.channel.history(limit=200).find(self.parsing.ext_pred))
        bin_img = await self.web.get(url, fmt="read")
        if file_type in self.file_types.images.glitch:
            file, file_name = await self.threading.glitch_handler(bin_img, size)
            embed = self.embeds.ImageEmbed(ctx=ctx, file_name=file_name)
            embed.GlitchEmbed()
            await ctx.reply(embed=embed.embed, file=file)
        else:
            raise commands.UserInputError("File type must be a 'png' or 'jpg'!")

    @commands.command()
    async def polarize(self, ctx, bits: int):
        if 0 > int(bits) or int(bits) >= 9:
            raise commands.UserInputError("Size must be an integer between 10 and 0!")
        url, file_type = self.parsing.ext_pred(await ctx.channel.history(limit=200).find(self.parsing.ext_pred))
        bin_img = await self.web.get(url, fmt="read")
        if file_type in self.file_types.images.polarize:
            file, file_name = await self.threading.polarize_handler(bin_img, int(bits))
            embed = self.embeds.ImageEmbed(ctx=ctx, file_name=file_name)
            embed.PolarizeEmbed()
            await ctx.reply(embed=embed.embed, file=file)
        else:
            raise commands.UserInputError("File type must be a 'png' or 'jpg'!")

    @commands.command()
    async def duotone(self, ctx, color1: str, color2: str):
        if not self.parsing.is_hex(color1) or not self.parsing.is_hex(color2):
            raise commands.UserInputError("Please use hex colour codes! Try [this](https://htmlcolorcodes.com/color-picker/) site.")
        url, file_type = self.parsing.ext_pred(await ctx.channel.history(limit=200).find(self.parsing.ext_pred))
        bin_img = await self.web.get(url, fmt="read")
        if file_type in self.file_types.images.duotone:
            file, file_name = await self.threading.duotone_handler(bin_img, self.parsing.hex_to_rgb(color1), self.parsing.hex_to_rgb(color2))
            embed = self.embeds.ImageEmbed(ctx=ctx, file_name=file_name)
            embed.DuotoneEmbed()
            await ctx.reply(embed=embed.embed, file=file)
        else:
            raise commands.UserInputError("File type must be a 'png' or 'jpg'!")

    @commands.command()
    async def deepfry(self, ctx):
        url, file_type = self.parsing.ext_pred(await ctx.channel.history(limit=200).find(self.parsing.ext_pred))
        bin_img = await self.web.get(url, fmt="read")
        if file_type in self.file_types.images.deepfry:
            file, file_name = await utils.pillows.deepfry(bin_img)
            embed = self.embeds.ImageEmbed(ctx=ctx, file_name=file_name)
            embed.DeepfryEmbed()
            await ctx.reply(embed=embed.embed, file=file)
        else:
            raise commands.UserInputError("File type must be a 'png' or 'jpg'!")

def setup(client):
    client.add_cog(images(client))