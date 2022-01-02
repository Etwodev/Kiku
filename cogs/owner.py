from discord.ext import commands
import discord, importlib, sys

command_attrs = {'hidden':True}

class OwnerCog(commands.Cog, name='Owner Commands', command_attrs=command_attrs):

    def __init__(self, client):
        self.client = client

    @commands.command(name='load', hidden=True)
    async def load_cog(self, ctx, *, cog: str):
        '''Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner'''

        try:
            self.client.load_extension(cog)
        except Exception as e:
            await ctx.reply(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.reply('**`SUCCESS`**')

    @commands.command(name='unload')
    async def unload_cog(self, ctx, *, cog: str):
        '''Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner'''

        try:
            self.client.unload_extension(cog)
        except Exception as e:
            await ctx.reply(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.reply('**`SUCCESS`**')

    @commands.command(name='reload')
    async def reload_cog(self, ctx, *, cog: str):
        '''Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner'''

        try:
            self.client.unload_extension(cog)
            self.client.load_extension(cog)
        except Exception as e:
            await ctx.reply(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.reply('**`SUCCESS`**')

    @commands.command(name='shutdown')
    async def server_shutdown(self, ctx):
        try:
            await ctx.message.add_reaction(emoji="👍")
            await self.client.logout()
        except EnvironmentError:
            await ctx.reply("**`An EnvironmentError Occured.`**")
            self.client.clear()

    async def cog_check(self, ctx):
        if not await self.client.is_owner(ctx.author):
            await ctx.reply("**`You aren't authorised to run this command.`**")
            raise commands.NotOwner('**`You do not own this client.`**')
        return True

def setup(client):
    client.add_cog(OwnerCog(client))