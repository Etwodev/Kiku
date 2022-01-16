import aiohttp, asyncio

async def get(url, fmt="text", path=None, *args, **kwargs):
    '''Get data from a url, supported "text" or "read"
    '''
    async with aiohttp.ClientSession() as session:
        async with session.get(url, *args, *kwargs) as resp:
            if fmt == "text":
                return await resp.text()
            elif fmt == "read":
                return await resp.read()
            else:
                raise EnvironmentError

async def post(url, fmt="text", *args, **kwargs):
    '''Post and return data from a url, see aiohttp docs for args and kwargs
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url, *args, *kwargs) as resp:
            if fmt == "text":
                return await resp.text()
            elif fmt == "read":
                return await resp.read()
            else:
                raise EnvironmentError
