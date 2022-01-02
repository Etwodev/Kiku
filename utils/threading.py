from utils import pillows
import asyncio, concurrent.futures

async def poll_handler(data: dict):
    '''Data in this case would be referenced poll data, see usage in code
    '''
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        img, name = await loop.run_in_executor(pool, pillows.poll, data)
    return img, name

async def glitch_handler(img, amount: int):
    '''An integer "amount" will be used for glitch amount. Bytes-type/read object expected for img
    '''
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        img, name = await loop.run_in_executor(pool, pillows.glitcher, img, amount)
    return img, name

async def polarize_handler(img, bits: int):
    '''Bits is expected as an integer, read or bytes-type object expected for img
    '''
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        img, name = await loop.run_in_executor(pool, pillows.polarize, img, bits)
    return img, name

async def duotone_handler(img, white: tuple, black: tuple):
    '''White and Black are RGB Tuple values converted from hex. Read or bytes-type is again expected for img
    '''
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        img, name = await loop.run_in_executor(pool, pillows.duotone, img, black, white)
    return img, name

async def gif_handler(url: str, msg_id: str):
    '''Both url and msg_id is expected as a string for parsing
    '''
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        file, nm = await loop.run_in_executor(pool, pillows.seek_gif_save, url, msg_id)
    return file, nm
