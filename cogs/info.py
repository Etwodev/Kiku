import discord, asyncio, random
from discord.ext import commands
from discord_components import DiscordComponents, Button, Select, SelectOption, ButtonStyle
import utils.embeds.info, utils.parsing, utils.web

class info(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.embeds = utils.embeds.info
        self.parsing = utils.parsing
        self.web = utils.web

    @commands.command()
    async def help(self, ctx):
        embed = self.embeds.InfoEmbed(ctx=ctx)
        embed.HelpEmbed()
        await ctx.reply(embed=embed.embed)
        
    @commands.command()
    async def vote(self, ctx):
        embed = self.embeds.InfoEmbed(ctx=ctx)
        embed.VoteEmbed()
        await ctx.reply(embed=embed.embed)

    @commands.command()
    async def emote(self, ctx, emote):
        emote = utils.parsing.PartialMessageEmoji(emote)
        embed = self.embeds.InfoEmbed(ctx=ctx)
        if await self.web.get(f"https://cdn.discordapp.com/emojis/{emote.emoji_id}.gif", "200"):
            embed.EmoteEmbed(emote=emote, is_animated=True)
        else:
            embed.EmoteEmbed(emote=emote, is_animated=False)
        await ctx.reply(embed=embed.embed)

    @commands.command()
    async def ping(self, ctx):
        embed = self.embeds.InfoEmbed(ctx=ctx)
        embed.PingEmbedA()
        msg = await ctx.reply(embed=embed.embed)
        ms = str((msg.created_at-ctx.message.created_at).total_seconds() * 1000)
        embed.PingEmbedB(ms=ms)
        await msg.edit(embed=embed.embed)
        
    @commands.command()
    async def choice(self, ctx, *args):
        if len(args) > 1000:
            raise commands.UserInputError("You cannot have more than 1000 items in a choice")
        embed = self.embeds.InfoEmbed(ctx=ctx)
        embed.ChoiceEmbed(items=args)
        await ctx.reply(embed=embed.embed)

    @commands.command()
    async def poll(self, ctx, *poll: str):
        if not poll:
            raise commands.UserInputError("No question specified!")
        else:
            poll = list(poll)
            msg = " ".join(poll)
        if 50 < len(msg):
            msg = msg[:49]
        components = [[Button(label = "End", style=ButtonStyle.blue, custom_id="End"), Button(label = "Yes", style=ButtonStyle.green, custom_id="Yes"),Button(label = "Abstain", style=ButtonStyle.grey, custom_id="Abstain"), Button(label = "No", style=ButtonStyle.red, custom_id="No")]]
        embed = self.embeds.InfoEmbed(ctx=ctx)
        embed.PollEmbed(msg=msg)
        await ctx.reply(embed=embed.embed, components=components)
        
    # @commands.command()
    # async def giveaway(self, ctx, *poll: str):
    #     if not poll:
    #         raise commands.UserInputError("No question specified!")
    #     else:
    #         poll = list(poll)
    #         msg = " ".join(poll)
    #     if 50 < len(msg):
    #         msg = msg[:49]
    #     components = [[Button(label = "Stop", style=ButtonStyle.blue, custom_id="Stop"), Button(label = "Enter", style=ButtonStyle.green, custom_id="Enter")]]
    #     embed = self.embeds.InfoEmbed(ctx=ctx)
    #     embed.GiveawayEmbed(msg=msg)
    #     await ctx.reply(embed=embed.embed, components=components)

def setup(client):
    client.add_cog(info(client))