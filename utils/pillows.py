import matplotlib
matplotlib.use('Agg')

from matplotlib import pyplot as plt
import numpy as np
import PIL, discord, io

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