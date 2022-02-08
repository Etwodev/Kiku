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
        
    @commands.command()
    async def banner(self, ctx):
        if not ctx.message.mentions:
            user = ctx.author
        else:
            user = ctx.message.mentions[0]
        url = await self.api.fetch_banner(self.client, user.id)
        if not url:
            raise commands.UserInputError("User does not have a valid banner!")
        embed = self.embeds.FunEmbed(ctx=ctx)
        embed.BannerEmbed(url=url, user=user)
        await ctx.reply(embed=embed.embed)
    
    @commands.command()
    async def pfp(self, ctx):
        if not ctx.message.mentions:
            user = ctx.author
        else:
            user = ctx.message.mentions[0]
        embed = self.embeds.FunEmbed(ctx=ctx)
        embed.ProfilePictureEmbed(url=user.avatar_url, user=user)
        await ctx.reply(embed=embed.embed)
    
    @commands.command()
    async def lookup(self, ctx, *args):
        if ctx.channel.is_nsfw():
            url, score = await self.api.gelbooru_nsfw(args)
        else:
            url, score = await self.api.gelbooru_sfw(args)
        if not url:
            raise commands.UserInputError("No matching images with those tags were found!")
        elif not self.parsing.endswith_bool(self.file_types.fun.lookup, url):
            raise commands.UserInputError("Invalid file-type encountered, please try again!")
        else:
            embed, components = self.embeds.FunEmbed(ctx=ctx), [[Button(label="Delete", style=ButtonStyle.red, custom_id="LookupDelete")]]
        if self.parsing.endswith_bool(self.file_types.fun.lookup_vid, url):
            embed.LookupLoadingEmbed()
            msg = await ctx.reply(embed=embed.embed)
            file, name = await self.threading.gif_handler(url)
            await msg.delete()
            embed.LookupFileEmbed(name, score)
            await ctx.reply(embed=embed.embed, components=components, file=file)
        else:
            embed.LookupURLEmbed(url, score)
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