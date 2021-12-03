import aiohttp, asyncio

async def get(url, fmt="text", *args, **kwargs):
    '''Get data from a url, supported "text" or "read"
    '''
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, *args, *kwargs) as resp:
                if fmt == "text":
                    return await resp.text()
                if fmt == "read":
                    return await resp.read()
                else:
                    raise "Invalid Parameters"
    except:
        return None

async def post(url, fmt="text", *args, **kwargs):
    '''Post and return data from a url, see aiohttp docs for args and kwargs
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url, *args, *kwargs) as resp:
            if fmt == "text":
                return await resp.text()
            if fmt == "read":
                return await resp.read()
            else:
                raise "Invalid Parameters"
    