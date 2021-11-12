import discord, asyncio
from discord.ext import commands
from utils import definitions, referencing, api
from discord_components import DiscordComponents, Button, Select, SelectOption, ButtonStyle


class info(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.embeds = definitions.embeded()
        self.poll_emojis = ["✅", "♻️", "❌"]

    @commands.command()
    async def help(self, ctx):
        await ctx.reply(embed=self.embeds.help())

    @commands.command()
    async def reactions(self, ctx):
        await ctx.reply(embed=self.embeds.reactions())

    @commands.command()
    @commands.guild_only()
    async def emote(self, ctx, emote):
        emote_url, emote_name = await api.emoji_handler(emote)
        if emote_name != None and emote_name != None:
            await ctx.reply(embed=(self.embeds.emote(ctx, emote_name, emote_url)))

    @commands.command()
    async def ping(self, ctx):
        msg = await ctx.reply(embed=self.embeds.ping_discord_a())
        ms = str((msg.created_at-ctx.message.created_at).total_seconds() * 1000)
        await msg.edit(embed=self.embeds.ping_discord_b(ms))
    
    @commands.command()
    async def afk(self, ctx, *msg: str):
        msg = " ".join(msg)
        if 50 < len(msg):
            msg = msg[:49]
        elif len(msg) == 0:
            msg = "User is afk."
        referencing.update_handler(ctx.author, msg, 1)
        await ctx.reply(embed=(self.embeds.afk(ctx, msg)))

    @commands.command()
    async def poll(self, ctx, *poll: str):
        msg = " ".join(poll)
        if 50 < len(msg):
            msg = msg[:49]
        await ctx.reply(embed=(self.embeds.create_poll(ctx, msg)), components=[[Button(label = "End Poll", style=ButtonStyle.blue, custom_id="pollend"), Button(label = "Yes", style=ButtonStyle.green, custom_id="Yes"),Button(label = "Abstain", style=ButtonStyle.grey, custom_id="Abstain"), Button(label = "No", style=ButtonStyle.red, custom_id="No")]])

def setup(client):
    client.add_cog(info(client))