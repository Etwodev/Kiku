from saucenao_api import AIOSauceNao
from pygelbooru import Gelbooru

import json

import discord

import random

from utils import web, config

util = config.get("config.json")

async def saucenao(url: str):
    results = await AIOSauceNao(api_key=util.api_keys.saucenao).from_url(url)
    if not results:
        return None
    results[0].urls.append(results[0].thumbnail)
    return results

async def tenor(key_word: str, max_return: int):
    results = json.loads(await web.get(f"https://api.tenor.com/v1/search?q={key_word}&key=XRK7Z66G3CUH&limit={max_return}"))
    if not results:
        return None
    return results['results'][random.randint(1, max_return-1)]['media'][0]['gif']['url']

async def ayako_pics(catagory: str):
    results = json.loads(await web.get(f'https://ayako.one/api/?kind={catagory}&token={util.api_keys.ayako_api}'))
    if not results or config.keys_exists(results, "error"):
        return None
    return str(results['url'])

async def gelbooru_sfw(tags: list):
    gelbooru = Gelbooru(util.api_keys.gelbooru.userid, util.api_keys.gelbooru.key)
    results = await gelbooru.search_posts(tags=tags, exclude_tags=util.exclude_sfw_tags)
    if not results:
        return None, None
    rand = random.randint(0, len(results)-1)
    return str(results[rand]), results[rand].score

async def gelbooru_nsfw(tags: list):
    gelbooru = Gelbooru(util.api_keys.gelbooru.userid, util.api_keys.gelbooru.key)
    results = await gelbooru.search_posts(tags=tags, exclude_tags=util.exclude_nsfw_tags)
    if not results:
        return None, None
    rand = random.randint(0, len(results)-1)
    return str(results[rand]), results[rand].score

async def gelbooru_tag(tag: str):
    gelbooru = Gelbooru(util.api_keys.gelbooru.userid, util.api_keys.gelbooru.key)
    results = await gelbooru.tag_list(name_pattern=f"%{tag}%", limit=6)
    for i, value in enumerate(results):
        results[i] = value.name
    if not results:
        return None
    return results

async def fetch_banner(client: discord.Client, user_id: int):
    req = await client.http.request(discord.http.Route("GET", "/users/{uid}", uid=user_id))
    banner_id = req["banner"]
    if banner_id:
        if await web.get(f"https://cdn.discordapp.com/banners/{user_id}/{banner_id}.gif?size=1024", "200"):
            return f"https://cdn.discordapp.com/banners/{user_id}/{banner_id}.gif?size=1024"
        return f"https://cdn.discordapp.com/banners/{user_id}/{banner_id}?size=1024"
    return None