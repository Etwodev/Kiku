# FIXME

# import discord
# from discord import embeds
# from discord.enums import UserFlags
# from discord.ext import commands
# import utils.embeds.reactions, utils.referencing, utils.api, utils.parsing

# class reactions(commands.Cog):
#     def __init__(self, client):
#         self.client = client
#         self.api = utils.api
#         self.embeds = utils.embeds.reactions
#         self.parsing = utils.parsing

#     @commands.command()
#     async def hug(self, ctx, *msg):
#         if not ctx.message.mentions:
#             raise commands.UserInputError("Please mention someone!")
#         msg = self.parsing.input_check(msg)
#         url = await self.api.ayako_pics("hug")
#         embed = self.embeds.ReactionsEmbed(ctx, self.client, url, msg)
#         embed.HugEmbed()
#         await ctx.reply(embed=embed.embed)
        
#     @commands.command()
#     async def yeet(self, ctx, *msg):
#         if not ctx.message.mentions:
#             raise commands.UserInputError("Please mention someone!")
#         msg = self.parsing.input_check(msg)
#         url = await self.api.ayako_pics("yeet")
#         embed = self.embeds.ReactionsEmbed(ctx, self.client, url, msg)
#         embed.YeetEmbed()
#         await ctx.reply(embed=embed.embed)
        
#     @commands.command()
#     async def wink(self, ctx, *msg):
#         if not ctx.message.mentions:
#             raise commands.UserInputError("Please mention someone!")
#         msg = self.parsing.input_check(msg)
#         url = await self.api.ayako_pics("wink")
#         embed = self.embeds.ReactionsEmbed(ctx, self.client, url, msg)
#         embed.WinkEmbed()
#         await ctx.reply(embed=embed.embed)
        
#     @commands.command()
#     async def wave(self, ctx, *msg):
#         if not ctx.message.mentions:
#             raise commands.UserInputError("Please mention someone!")
#         msg = self.parsing.input_check(msg)
#         url = await self.api.ayako_pics("wave")
#         embed = self.embeds.ReactionsEmbed(ctx, self.client, url, msg)
#         embed.WaveEmbed()
#         await ctx.reply(embed=embed.embed)
        
#     @commands.command()
#     async def smug(self, ctx, *msg):
#         if not ctx.message.mentions:
#             raise commands.UserInputError("Please mention someone!")
#         msg = self.parsing.input_check(msg)
#         url = await self.api.ayako_pics("smug")
#         embed = self.embeds.ReactionsEmbed(ctx, self.client, url, msg)
#         embed.SmugEmbed()
#         await ctx.reply(embed=embed.embed)
        
#     @commands.command()
#     async def smile(self, ctx, *msg):
#         if not ctx.message.mentions:
#             raise commands.UserInputError("Please mention someone!")
#         msg = self.parsing.input_check(msg)
#         url = await self.api.ayako_pics("smile")
#         embed = self.embeds.ReactionsEmbed(ctx, self.client, url, msg)
#         embed.SmileEmbed()
#         await ctx.reply(embed=embed.embed)
        
# def setup(client):
#     client.add_cog(reactions(client))