import discord
from discord.ext import commands
from utils import api, definitions, handle





class images(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.file_types = definitions.file_types()

    @commands.command()
    async def glitch(self, ctx, size: int):
        if 0 > int(size) and int(size) >= 10:
            raise commands.MissingRequiredArgument("Size must be an integer between 10 and 0!")
        message, file_type = api.predicate(await ctx.channel.history(limit=200).find(api.predicate))
        if file_type in self.file_types.glitch:
            handle.glitch_handler(message, size)
        else:
            raise commands.MissingRequiredArgument("File type must be .png or .jpg!")
        

    # @commands.command()
    # async def duotone(self, ctx):
    #     message, file_type = api.predicate(await ctx.channel.history(limit=200).find(api.predicate))

    # @commands.command()
    # async def deepfry(self, ctx):
    #     message, file_type = api.predicate(await ctx.channel.history(limit=200).find(api.predicate))

def setup(client):
    client.add_cog(images(client))