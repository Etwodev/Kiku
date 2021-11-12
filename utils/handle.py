from utils import web, startup, pillows
import asyncio, concurrent.futures

#######ASYNCIO EXECUTOR HANDLERS#########

async def poll_handler(data):
    """Data in this case would be referenced poll data, see usage in code
    """
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result, name = await loop.run_in_executor(pool, pillows.poll, data)
    return result, name

async def glitch_handler(message, size):
    """Data will be the parameters for this.
    """
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        img, name = await loop.run_in_executor(pool, pillows.glitcher, message, size)
    return img, name