from datetime import datetime
import requests, json
from discord.ext import commands
import discord, importlib, sys, secrets
import utils.referencing, utils.config, utils.web

command_attrs = {'hidden':True}

class OwnerCog(commands.Cog, name='Owner Commands', command_attrs=command_attrs):

    def __init__(self, client):
        self.client = client
        self.config = utils.config.get("config.json")

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
            await self.client.close()
        except EnvironmentError:
            await ctx.reply("**`An EnvironmentError Occured.`**")
            self.client.clear()
            
    @commands.command(name='keygen')
    async def generate_key(self, ctx):
        val = str(int(datetime.utcnow().timestamp())*256)
        payload = {"token": val, "username": self.config.api_keys.web_db.username, "password": self.config.api_keys.web_db.password}
        data = requests.post(url=self.config.links.db, data=payload)
        if data.status_code != 201:
            await ctx.reply(f"**`ERROR:`** Status code {data.status_code}")
        else:
            data = json.loads(data.content)
            await ctx.reply(f"**`SUCCESS:`** New token " + str(data["token"]))

    async def cog_check(self, ctx):
        if ctx.author.id in self.config.owners:
            return True
        await ctx.reply("**`You aren't authorised to run this command.`**")
        raise commands.NotOwner('**`You do not own this client.`**')

def setup(client):
    client.add_cog(OwnerCog(client))