import discord
from discord.ext import commands
from utils import startup
import traceback, sys
from discord_components import DiscordComponents, Button, Select, SelectOption


config = startup.get("config.json")

client = commands.Bot(command_prefix=config.prefix, intents=discord.Intents(guilds=True, members=True, messages=True, reactions=True, presences=True), case_insensitive=True)
client.remove_command("help")

if __name__ == '__main__':
    for Extension in ["cogs.info", "cogs.listeners", "cogs.owner", "cogs.images", "cogs.fun"]:
        try:
            client.load_extension(Extension)
        except Exception as e:
            print(f'Failed to load extension {Extension}.', file=sys.stderr)
            traceback.print_exc()

try:
    client.run(config.api_keys.token, reconnect=True)
except Exception as e:
    print(f"Error when logging in: {e}")