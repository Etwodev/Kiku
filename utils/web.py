import aiohttp, asyncio

async def get(url, fmt="text", path=None, *args, **kwargs):
    '''Get data from a url, supported "text" or "read"
    '''
    async with aiohttp.ClientSession() as session:
        async with session.get(url, *args, *kwargs) as resp:
            if fmt == "200":
                return str(resp.status) == "200"
            elif fmt == "text":
                return await resp.text()
            elif fmt == "read":
                return await resp.read()
            else:
                raise EnvironmentError