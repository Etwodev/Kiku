import discord
from discord import embeds
from discord.enums import UserFlags
from discord.ext import commands
from discord_components import DiscordComponents, Button, Select, SelectOption, ButtonStyle
from discord_components.client import ComponentsBot
import utils.embeds.harem, utils.referencing, utils.api

class harem(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.referencing = utils.referencing
        self.embeds = utils.embeds.harem
        self.api = utils.api
        
    @commands.command()
    async def invite(self, ctx):
        profile = self.referencing.HaremHeader(ctx.author)
        if not ctx.message.mentions:
            raise commands.UserInputError("Please mention a user first!")
        else:
            mention = self.referencing.HaremHeader(ctx.message.mentions[0])
            if profile.is_owner() and not mention.in_harem() and profile.count < 5:
                embed, components = self.embeds.HaremEmbed(ctx=ctx), [[Button(label="Accept", style=ButtonStyle.green, custom_id='{"Accept": ' + str(ctx.message.mentions[0].id) + '}'), Button(label="Reject", style=ButtonStyle.red, custom_id='{"Reject": ' + str(ctx.message.mentions[0].id) + '}')]]
                embed.InviteEmbed(ctx.message.mentions[0], await self.api.tenor("anime+propose", 8))
                await ctx.reply(embed=embed.embed, components=components)
            else:
                raise commands.UserInputError("You are not the owner of the harem or do not own one; or the user you mentioned is already a part of one! There is also a limit of 5 people per harem.")
    
    @commands.command()
    async def leave(self, ctx):
        profile = self.referencing.HaremHeader(ctx.author)
        if profile.leave():
            embed = self.embeds.HaremEmbed(ctx=ctx)
            embed.LeaveEmbed(profile=profile, harem=ctx.author, url=await self.api.tenor("anime+sad", 8))
            await ctx.reply(embed=embed.embed)
        else:
            raise commands.UserInputError("You are the owner of the harem or are not in one!")
        
    @commands.command()
    async def end(self, ctx):
        profile = self.referencing.HaremHeader(ctx.author)
        if profile.end():
            embed = self.embeds.HaremEmbed(ctx=ctx)
            embed.EndEmbed(profile=profile, url=await self.api.tenor("anime+sad", 8))
            await ctx.reply(embed=embed.embed)
        else:
            raise commands.UserInputError("You are not the owner of the harem or do not own one!")
        
    @commands.command()
    async def create(self, ctx):
        profile = self.referencing.HaremHeader(ctx.author)
        if profile.create():
            embed = self.embeds.HaremEmbed(ctx=ctx)
            embed.CreateEmbed(profile=profile, url=await self.api.tenor("anime+celebrate", 8))
            await ctx.reply(embed=embed.embed)
        else:
            raise commands.UserInputError("You are already part of a harem!")
        
    @commands.command()
    async def harem(self, ctx):
        if ctx.message.mentions:
            user = ctx.message.mentions[0]
        else:
            user = ctx.author
        profile = self.referencing.HaremHeader(user)
        if profile.in_harem():
            embed = self.embeds.HaremEmbed(ctx=ctx)
            tmp = []
            for x in profile.users():
                if x == profile.owner:
                    pass
                else:
                    x = await self.client.fetch_user(x)
                    tmp.append(x.name)
            owner = await self.client.fetch_user(profile.owner)
            embed.OwnerEmbed(owner=owner, harem=tmp)
            await ctx.reply(embed=embed.embed)
        else:
            raise commands.UserInputError("You are not part of a harem!")
    
        
def setup(client):
    client.add_cog(harem(client))