import matplotlib

import subprocess

matplotlib.use('Agg')

from matplotlib import pyplot as plt
import numpy as np
import PIL, discord, io

from glitch_this import ImageGlitcher

import deeppyer

def seek_save(img: PIL.Image, fmt: str, nm: str):
    '''Saves pillow files into memory
    '''
    arr = io.BytesIO()
    img.save(arr, format=fmt)
    arr.seek(0)
    file = discord.File(arr, nm)
    return file, nm

def seek_savempl(img: PIL.Image, fmt: str, nm: str):
    '''Saves matplotlib files into memory
    '''
    arr = io.BytesIO()
    img.savefig(arr, format=fmt)
    arr.seek(0)
    file = discord.File(arr, nm)
    return file, nm

def poll(data: dict):
    '''Converts dictionary data into a matplotlib image
    '''
    data = {key:val for key, val in data.items() if val != 0}
    plt.pie(data.values(), labels = data.keys(), startangle = 90)
    file, name = seek_savempl(plt, "png", "pie_chart.png")
    return file, name

def glitcher(file, amount: int):
    '''Glitches the input image
    '''
    glitcher = ImageGlitcher()
    gltch_img = PIL.Image.open(io.BytesIO(file)).convert("RGB") 
    gltch_img = glitcher.glitch_image(gltch_img, amount, color_offset=True)
    file, name = seek_save(gltch_img, "png", "glitch_image.png")
    return file, name

def polarize(file, bits: int):
    '''Polarizes the input image
    '''
    polar_img = PIL.Image.open(io.BytesIO(file)).convert("RGB") 
    polar_img = PIL.ImageOps.posterize(polar_img, bits)
    file, name = seek_save(polar_img, "png", "polar_image.png")
    return file, name

def duotone(file, black: tuple, white: tuple):
    '''Applies a duotone effect on an image, using colorize. Accepts tuples of rgb for input
    '''
    duo_img = PIL.Image.open(io.BytesIO(file)).convert("L")
    duo_img = PIL.ImageOps.colorize(duo_img, black=black, white=white, blackpoint=126, whitepoint=128)
    file, name = seek_save(duo_img, "png", "duotone_image.png")
    return file, name

async def deepfry(file):
    '''Deepfries the input image
    '''
    deep_img = PIL.Image.open(io.BytesIO(file)).convert("RGB") 
    deep_img = await deeppyer.deepfry(deep_img, flares=False)
    file, name = seek_save(deep_img, "png", "deep_image.png")
    return file, name

def seek_gif_save(url: str):
    '''Converts a video file to a gif, with a max length of 5 seconds due to discord file-size restrictions
    '''
    pipe = subprocess.run(
        ['ffmpeg', '-hide_banner', 
         '-loglevel', 'error',
         '-i', url,
         '-vf',
         'fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse',
         '-fs','8M',
         '-loop', '0', "-f", "gif", "pipe:1"], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
        )

    name = "output.gif"
    output = io.BytesIO(pipe.stdout)
    file = discord.File(output, name)
    return file, name
