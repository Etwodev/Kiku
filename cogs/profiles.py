import discord
from discord import embeds
from discord.enums import UserFlags
from discord.ext import commands
from discord_components import DiscordComponents, Button, Select, SelectOption, ButtonStyle
from discord_components.client import ComponentsBot
import utils.embeds.profiles, utils.referencing, utils.api

class profiles(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.referencing = utils.referencing
        self.embeds = utils.embeds.profiles
        self.api = utils.api
        
        
    @commands.command()
    async def marry(self, ctx):
        if not ctx.message.mentions:
            raise commands.UserInputError("Please mention a user first!")
        else:
            profile = self.referencing.ProfileHeader(ctx.author)
            mention = self.referencing.ProfileHeader(ctx.message.mentions[0])
            if not profile.is_married() and not mention.is_married():
                embed, components = self.embeds.ProfilesEmbed(ctx=ctx), [[Button(label="I do", style=ButtonStyle.green, custom_id='{"I do": ' + str(ctx.message.mentions[0].id) + '}'), Button(label="Denied", style=ButtonStyle.red, custom_id='{"Denied": ' + str(ctx.message.mentions[0].id) + '}')]]
                embed.MarryEmbed(await self.api.tenor("anime+marriage", 8))
                await ctx.reply(embed=embed.embed, components=components)
            else:
                raise commands.UserInputError("One of you is already married!")
            
    @commands.command()
    async def divorce(self, ctx):
        user = self.referencing.ProfileHeader(ctx.author)
        if user.remove_marriage():
            embed = self.embeds.ProfilesEmbed(ctx=ctx)
            embed.DivorceEmbed(await self.api.tenor("anime+sad", 8))
        else:
            raise commands.UserInputError("Thankfully, you are not married!")
            
    @commands.command()
    async def profile(self, ctx):
        if not ctx.message.mentions:
            tmp = ctx.author
        else:
            tmp = ctx.message.mentions[0]
        user = self.referencing.ProfileHeader(tmp)
        if user.is_married():
            married = self.client.fetch_user(user.marriage.id)
        else:
            married = None
        embed = self.embeds.ProfilesEmbed(ctx=ctx)
        embed.ProfileEmbed(user, married)
        await ctx.reply(embed=embed.embed)
        
    @commands.command()
    async def afk(self, ctx, *msg: str):
        user = self.referencing.ProfileHeader(ctx.author)
        msg = " ".join(msg)
        if 50 < len(msg):
            msg = msg[:49]
        elif not msg:
            msg = "User is afk."
        user.set_afk(msg)
        embed = self.embeds.ProfilesEmbed(ctx=ctx)
        embed.AfkEmbed(msg)
        await ctx.reply(embed=embed.embed)
            
            
def setup(client):
    client.add_cog(profiles(client))