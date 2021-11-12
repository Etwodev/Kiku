from saucenao_api import SauceNao
from pygelbooru import Gelbooru
import re, discord
from utils import web, startup

########HANDLER########
# - Hanlder acts as a way to connect API and databases with command calls and embeds.
#########TODO#########
# ----------------------
# - Handler gets a!gacha request.
# - Checks if user has sufficient money with select.
# - If True, create a gatcha roll and return the result, then append profile.
# - If False, send the regarding message.
# ----------------------
# - Add Gelbooru API
# - Add Tenor API
# - Add WaifuPics API
# - Add Error Handler
# ---------------------

config = startup.get("config.json")

#######API FUNCTIONS########

def saucenao(url):
    """This is a basic-level saucenao handler.
    It can be run in executor, asyncronously, not recommened.
    
    returns a SauceNao object, results.
    -> results[0].thumbnail     # temporary URL for picture preview
    -> results[0].similarity    # similarity to the original
    -> results[0].title         # title of the piece
    -> results[0].urls          # list of urls to the piece
    -> results[0].author        # author of the piece
    -> results[0].raw           # raw result
    """
    return SauceNao(api_key=config.api_keys.saucenao).from_url(url)

#######OTHER WEB BASED FUNCTIONS#######

async def emoji_handler(emoji):
    """Handles fetching and managing emotes through regex.
    returns url, name
    """
    lookup, eid = emoji, None
    if ':' in emoji:
        # matches custom emote
        server_match = re.search(r'<a?:(\w+):(\d+)>', emoji)
        # matches global emote
        custom_match = re.search(r':(\w+):', emoji)
        if server_match:
            lookup, eid = server_match.group(1), server_match.group(2)
        elif custom_match:
            lookup, eid = custom_match.group(1), None
        else:
            lookup, eid = emoji.split(':')
        try:
            eid = int(eid)
        except (ValueError, TypeError):
            eid = None
        if await web.get(f"https://cdn.discordapp.com/emojis/{eid}.gif") == "202":
            return f"https://cdn.discordapp.com/emojis/{eid}.gif", lookup
        else:
            return f"https://cdn.discordapp.com/emojis/{eid}.png", lookup
    else:
        return None, None

#######BASIC PARSING#######

def predicate(message, formats=["png", "jpeg", "jpg", "webp", "webp?size=1024", "gif", "mkv", "mov", "mp4", "webm"]):
    """Fetches newest attachment in the channel: returns attachment path, file extension
    """
    for attachment in message.attachments:
        for image_type in formats:
            if attachment.filename.lower().endswith(image_type):
                return attachment, image_type
    for embed in message.embeds:
        if embed.image.url is not discord.Embed.Empty:
            for image_type in formats:
                if embed.image.url.lower().endswith(image_type):
                    return embed.image, image_type