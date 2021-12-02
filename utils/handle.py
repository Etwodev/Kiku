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

async def glitch_handler(img, amount: int):
    """Data will be the parameters for this.
    """
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        img, name = await loop.run_in_executor(pool, pillows.glitcher, img, int(amount))
    return img, name

async def polarize_handler(img, bits: int):
    """Data will be the parameters for this.
    """
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        img, name = await loop.run_in_executor(pool, pillows.polarize, img, int(bits))
    return img, name

async def duotone_handler(img, white: str, black: str):
    """Data will be the parameters for this.
    """
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        img, name = await loop.run_in_executor(pool, pillows.duotone, img, black, white)
    return img, name

async def convert_gif(url, msg_id):
    """Data will be the parameters for this.
    """
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        img, name = await loop.run_in_executor(pool, pillows.seek_gif_save, url, msg_id)
    return img, name
