import discord
from discord.ext import commands
from utils import api, definitions, web, handle
from discord_components import DiscordComponents, Button, Select, SelectOption, ButtonStyle




class fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.file_types = definitions.file_types()
        self.embeds = definitions.embeded()

    @commands.command()
    async def sauce(self, ctx):
        url, file_type, message = api.message_predicate(await ctx.channel.history(limit=200).find(api.predicate))
        if file_type in self.file_types.saucenao:
            results = await api.saucenao(url)
            await message.reply(embed=self.embeds.saucenao(results))
        else:
            raise commands.UserInputError("File type must be .png, .gif, or .jpg!")

    @commands.command()
    async def lookup(self, ctx, *args):
        if ctx.channel.is_nsfw():
            url = str(await api.gelbooru_nsfw(args))
        else:
            url = str(await api.gelbooru_sfw(args))
        if api.exts_allowed(self.file_types.lookup, url):
            if api.exts_allowed(self.file_types.lookup_ext, url):
                msg = await ctx.reply(embed=self.embeds.lookup_wt())
                img, name = await handle.convert_gif(url, ctx.message.id)
                await msg.delete()
                await ctx.reply(embed=self.embeds.lookup_ld(img, name), file=img, components=[[Button(label = "Delete", style=ButtonStyle.red)]])
                api.cleanup_gif(ctx.message.id)
            else:
                await ctx.reply(embed=self.embeds.lookup_rw(url), components=[[Button(label = "Delete", style=ButtonStyle.red)]])
        else:
            raise commands.UserInputError("Invalid file-type encountered, please try again!")

    @commands.command()
    async def tag(self, ctx, tag=None):
        if tag is None:
            raise commands.UserInputError("No tag inputted...")
        else:
            results = api.gelbooru_tag(tag)
            await ctx.reply(embed=self.embeds.tags(results))

def setup(client):
    client.add_cog(fun(client))