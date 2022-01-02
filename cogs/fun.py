import discord
from discord import embeds
from discord.ext import commands
from discord_components import DiscordComponents, Button, Select, SelectOption, ButtonStyle
from discord_components.client import ComponentsBot
import utils.embeds.fun, utils.api, utils.parsing, utils.threading, utils.config, utils.web

class fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.file_types = utils.config.get("file_types.json")
        self.api = utils.api
        self.embeds = utils.embeds.fun
        self.parsing = utils.parsing
        self.threading = utils.threading
    
    #Whatever you do, don't look at this code, it's illegal. I can't make it better I'm sorry.
    @commands.command()
    async def lookup(self, ctx, *args):
        if ctx.channel.is_nsfw():
            url = await self.api.gelbooru_nsfw(args)
        else:
            url = await self.api.gelbooru_sfw(args)
        if not url:
            raise commands.UserInputError("No matching images with that tag found!")
        elif not self.parsing.endswith_bool(self.file_types.fun.lookup, url):
            raise commands.UserInputError("Invalid file-type encountered, please try again!")
        else:
            embed, components = self.embeds.FunEmbed(ctx=ctx), [[Button(label="Delete", style=ButtonStyle.red, custom_id="LookupDelete")]]
        if self.parsing.endswith_bool(self.file_types.fun.lookup_vid, url):
            embed.LookupLoadingEmbed()
            msg = await ctx.reply(embed=embed.embed)
            file, nm = await self.threading.gif_handler(url, ctx.message.id)
            await msg.delete()
            embed.LookupFileEmbed(nm)
            await ctx.reply(embed=embed.embed, components=components, file=file)
            utils.config.remove_file(nm)
        else:
            embed.LookupURLEmbed(url)
            await ctx.reply(embed=embed.embed, components=components)
        
    @commands.command()
    async def sauce(self, ctx):
        embed = self.embeds.FunEmbed(ctx=ctx)
        url, file_type, message = self.parsing.predicate(await ctx.channel.history(limit=200).find(self.parsing.predicate))
        if file_type in self.file_types.fun.saucenao:
            results = await self.api.saucenao(url)
            embed.SauceNAOEmbed(results)
            await ctx.reply(embed=embed.embed)
        else:
            raise commands.UserInputError("No results found, or image is not a valid file-type!")
        
    @commands.command()
    async def tag(self, ctx, tag=None):
        if not tag:
            raise commands.UserInputError("No tag was inputted...")
        else:
            results = await self.api.gelbooru_tag(tag)
            embed = self.embeds.FunEmbed(ctx=ctx)
            embed.TagEmbed(results, tag)
            await ctx.reply(embed=embed.embed)
            
def setup(client):
    client.add_cog(fun(client))