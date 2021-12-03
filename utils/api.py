from saucenao_api import AIOSauceNao
from pygelbooru import Gelbooru
import re, json, random
from utils import web, startup

config = startup.get("config.json")

#######API FUNCTIONS########

async def saucenao(url: str):
    '''This is a basic-level saucenao handler.
    
    returns a SauceNao object, results.
    -> results[0].thumbnail     # temporary URL for picture preview
    -> results[0].similarity    # similarity to the original
    -> results[0].title         # title of the piece
    -> results[0].urls          # list of urls to the piece
    -> results[0].author        # author of the piece
    -> results[0].raw           # raw result
    '''
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
        return None
    return results[random.randint(0, len(results)-1)]

async def gelbooru_nsfw(tags: list):
    gelbooru = Gelbooru(config.api_keys.gelbooru.userid, config.api_keys.gelbooru.key)
    results = await gelbooru.search_posts(tags=tags, exclude_tags=config.exclude_nsfw_tags)
    if len(results) == 0:
        return None
    return results[random.randint(0, len(results)-1)]

async def gelbooru_tag(tag: str):
    gelbooru = Gelbooru(config.api_keys.gelbooru.userid, config.api_keys.gelbooru.key)
    results = await gelbooru.tag_list(name_pattern=tag, limit=6)
    return results

#######OTHER WEB BASED FUNCTIONS#######

async def emoji_handler(emoji: str):
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
