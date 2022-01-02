from saucenao_api import AIOSauceNao
from pygelbooru import Gelbooru

import json

import random

from utils import web, config

config = config.get("config.json")

async def saucenao(url: str):
    results = await AIOSauceNao(api_key=config.api_keys.saucenao).from_url(url)
    if not results:
        return None
    results[0].urls.append(results[0].thumbnail)
    return results

async def tenor(key_word: str, max_return: int):
    results = json.loads(await web.get(f"https://api.tenor.com/v1/search?q={key_word}&key=XRK7Z66G3CUH&limit={max_return}"))
    if not results:
        return None
    return results['results'][random.randint(1, max_return-1)]['media'][0]['gif']['url']

async def waifu_pics(safety: str, catagory: str):
    results = json.loads(await web.get(f'https://waifu.pics/api/{safety}/{catagory}'))
    if not results:
        return None
    return str(results['url'])

async def gelbooru_sfw(tags: list):
    gelbooru = Gelbooru(config.api_keys.gelbooru.userid, config.api_keys.gelbooru.key)
    results = await gelbooru.search_posts(tags=tags, exclude_tags=config.exclude_sfw_tags)
    if not results:
        return None
    return str(results[random.randint(0, len(results)-1)])

async def gelbooru_nsfw(tags: list):
    gelbooru = Gelbooru(config.api_keys.gelbooru.userid, config.api_keys.gelbooru.key)
    results = await gelbooru.search_posts(tags=tags, exclude_tags=config.exclude_nsfw_tags)
    if not results:
        return None
    return str(results[random.randint(0, len(results)-1)])

async def gelbooru_tag(tag: str):
    gelbooru = Gelbooru(config.api_keys.gelbooru.userid, config.api_keys.gelbooru.key)
    results = await gelbooru.tag_list(name_pattern=f"%{tag}%", limit=6)
    for i, value in enumerate(results):
        results[i] = value.name
    if not results:
        return None
    return results
