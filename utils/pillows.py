import matplotlib
matplotlib.use('Agg')

from matplotlib import pyplot as plt
import numpy as np
import PIL, discord, io

from glitch_this import ImageGlitcher

import deeppyer

from moviepy.editor import *

def seek_gif_save(url: str, msg_id: int, path=f"tmp/", fmt="GIF",):
    nm = str(msg_id) + ".gif"
    clip = VideoFileClip(url)
    if round(clip.duration) > 5:
        clip = clip.subclip(0, 5)
    clip = clip.resize(0.3)
    clip.write_gif(path + nm, fps=10, loop=0, program="imageio", fuzz=50)
    file = discord.File(path + nm)
    return file, nm

def seek_save(img, fmt, nm):
    '''Saves pillow files into memory
    '''
    arr = io.BytesIO()
    img.save(arr, format=fmt)
    arr.seek(0)
    file = discord.File(arr, nm)
    return file, nm

def seek_savempl(img, fmt, nm):
    '''Saves matplotlib files into memory
    '''
    arr = io.BytesIO()
    img.savefig(arr, format=fmt)
    arr.seek(0)
    file = discord.File(arr, nm)
    return file, nm

def poll(data):
    labels = []
    num = []
    for key, value in data.items():
        if key == "Yes" and int(value) > 0:
            labels.append("Yes")
            num.append(value)
        elif key == "Abstain" and int(value) > 0:
            labels.append("Abstained")
            num.append(value)
        elif key == "No" and int(value) > 0:
            labels.append("No")
            num.append(value)
    plt.pie(num, labels = labels, startangle = 90)
    file, name = seek_savempl(plt, "png", "pie_chart.png")
    return file, name

def glitcher(file, amount: int):
    glitcher = ImageGlitcher()
    gltch_img = PIL.Image.open(io.BytesIO(file))
    gltch_img = glitcher.glitch_image(gltch_img, int(amount), color_offset=True)
    file, name = seek_save(gltch_img, "png", "glitch_image.png")
    return file, name

def polarize(file, bits: int):
    polar_img = PIL.Image.open(io.BytesIO(file))
    polar_img = PIL.ImageOps.posterize(polar_img, int(bits))
    file, name = seek_save(polar_img, "png", "polar_image.png")
    return file, name

def duotone(file, black: tuple, white: tuple):
    duo_img = PIL.Image.open(io.BytesIO(file)).convert("L")
    duo_img = PIL.ImageOps.colorize(duo_img, black=black, white=white, blackpoint=126, whitepoint=128)
    file, name = seek_save(duo_img, "png", "duotone_image.png")
    return file, name

async def deepfry(file):
    deep_img = PIL.Image.open(io.BytesIO(file))
    deep_img = await deeppyer.deepfry(deep_img, flares=False)
    file, name = seek_save(deep_img, "png", "deep_image.png")
    return file, name
