from saucenao_api import AIOSauceNao
from pygelbooru import Gelbooru
from discord.ext import commands
import re, discord, json, random, os
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
# ---------------------

config = startup.get("config.json")

#######API FUNCTIONS########

async def saucenao(url: str):
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
    results = await AIOSauceNao(api_key=config.api_keys.saucenao).from_url(url)
    results[0].urls.append(results[0].thumbnail)
    return results

async def tenor(key_word: str, max_return: int):
    data = json.loads(await web.get(f"https://api.tenor.com/v1/search?q={key_word}&key=XRK7Z66G3CUH&limit={max_return}"))
    return data['results'][random.randint(1, max_return-1)]['media'][0]['gif']['url']

async def waifu_pics(safety: str, catagory: str):
    data = json.loads(await web.get(f'https://waifu.pics/api/{safety}/{catagory}'))
    return data['url']

async def gelbooru_sfw(tags: list):
    gelbooru = Gelbooru(config.api_keys.gelbooru.userid, config.api_keys.gelbooru.key)
    results = await gelbooru.search_posts(tags=tags, exclude_tags=config.exclude_sfw_tags)
    if len(results) == 0:
        raise commands.UserInputError(f"I could not find anything with those tags! Are you inputting correctly? Try looking up the tag with {config.prefix[0]}tag [tag] and try again!")
    return results[random.randint(0, len(results)-1)]

async def gelbooru_nsfw(tags: list):
    gelbooru = Gelbooru(config.api_keys.gelbooru.userid, config.api_keys.gelbooru.key)
    results = await gelbooru.search_posts(tags=tags, exclude_tags=config.exclude_nsfw_tags)
    if len(results) == 0:
        raise commands.UserInputError(f"I could not find anything with those tags! Are you inputting correctly? Try looking up the tag with {config.prefix[0]}tag [tag] and try again!")
    return results[random.randint(0, len(results)-1)]

async def gelbooru_tag(tag: str):
    gelbooru = Gelbooru(config.api_keys.gelbooru.userid, config.api_keys.gelbooru.key)
    results = await gelbooru.tag_list(name_pattern=tag, limit=6)
    return results

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
                return attachment.url, image_type
    for embed in message.embeds:
        if embed.image.url is not discord.Embed.Empty:
            for image_type in formats:
                if embed.image.url.lower().endswith(image_type):
                    return embed.image.url, image_type
    for url in list(re.findall(r'(https?://[^\s]+)', message.content)):
        for image_type in formats:
            if url.lower().endswith(image_type):
                return url, image_type

def message_predicate(message, formats=["png", "jpeg", "jpg", "webp", "webp?size=1024", "gif", "mkv", "mov", "mp4", "webm"]):
    """Alternate version of predicate that returns the message as well.
    """
    for attachment in message.attachments:
        for image_type in formats:
            if attachment.filename.lower().endswith(image_type):
                return attachment.url, image_type, message
    for embed in message.embeds:
        if embed.image.url is not discord.Embed.Empty:
            for image_type in formats:
                if embed.image.url.lower().endswith(image_type):
                    return embed.image.url, image_type, message
    for url in list(re.findall(r'(https?://[^\s]+)', message.content)):
        for image_type in formats:
            if url.lower().endswith(image_type):
                return url, image_type, message

#######CHECK PARSING#######

def is_hex(string: str):
    match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', string)
    if match:
        return True
    else:
        return False

def hex_to_rgb(hex: str):
    hex = hex.lstrip('#')
    lv = len(hex)
    return tuple(int(hex[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

#######CONVERT CHECk#######

def exts_allowed(exts: list, url: str):
    for x in exts:
        if url.lower().endswith(x):
            return True
    return False

def cleanup_gif(msg_id):
    if os.path.exists(f"tmp/{msg_id}.gif"):
        os.remove(f"tmp/{msg_id}.gif")
    else:
        return