import re, os, discord
from utils import web
from discord.ext import commands
import functools


def bitmask_gen(indexes: list):
    return functools.reduce(lambda x, y: x + (1 << y), indexes, 0)

def input_check(msg: tuple):
    if len(msg) > 1:
        msg = list(msg)
        msg.pop(0)
        msg = '"' + f"{' '.join(msg)}" + '"'
    elif 50 < len(msg):
        msg = msg[:49]
    else:
        msg = None
    return msg

def tuple_to_str(val: tuple, lim=50) -> str:
    if len(val) == 1 or 0:
        return None
    val = list(val)
    val.pop(0)
    val = ' '.join(val)[:lim]
    return '"' + val + '"'

def is_hex(string: str) -> bool:
    '''Checks if a string is a hex value
    '''
    return re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', string) != None

def hex_to_rgb(hex: str) -> tuple:
    '''Converts a hex value to rgb
    '''
    if not is_hex(hex):
        return None
    if hex[0] == "#":
        hex = hex.lstrip('#')
    lv = len(hex)
    return tuple(int(hex[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def endswith_iter(val: list, i: str) -> str:
    '''Checks if the specifed list of values end on a string
    '''
    for n in val:
        if i.lower().endswith(n):
            return n
    return None

def endswith_bool(val: list, i: str) -> str:
    '''Checks if the specifed list of values end on a string
    '''
    for n in val:
        if i.lower().endswith(n):
            return True
    return False

#######BASIC PARSING#######

def predicate(message, formats=["png", "jpeg", "jpg", "webp", "webp?size=1024", "gif", "mkv", "mov", "mp4", "webm"]):
    '''Fetches the newest attachment in the channel: returns url, file extension and message
    '''
    for attachment in message.attachments:
        for image_type in formats:
            if attachment.filename.lower().endswith(image_type):
                return attachment.url, image_type, message
    for embed in message.embeds:
        if embed.image.url is not discord.Embed.Empty:
            for image_type in formats:
                if embed.image.url.lower().endswith(image_type):
                    return embed.image.url, image_type, message
    for url in list(re.findall(r'(https?://[^\s]+)', message.content)):
        for image_type in formats:
            if url.lower().endswith(image_type):
                return url, image_type, message

def ext_pred(message, formats=["png", "jpeg", "jpg", "webp", "webp?size=1024", "gif", "mkv", "mov", "mp4", "webm"]):
    '''Fetches the newest attachment in the channel: returns url, file extension and message
    '''
    for attachment in message.attachments:
        for image_type in formats:
            if attachment.filename.lower().endswith(image_type):
                return attachment.url, image_type
    for embed in message.embeds:
        if embed.image.url is not discord.Embed.Empty:
            for image_type in formats:
                if embed.image.url.lower().endswith(image_type):
                    return embed.image.url, image_type
    for url in list(re.findall(r'(https?://[^\s]+)', message.content)):
        for image_type in formats:
            if url.lower().endswith(image_type):
                return url, image_type


class PartialMessageEmoji:
    def __init__(self, emoji: str):
        self.emoji = emoji
        match = re.search(r'<a?:(\w+):(\d+)>', emoji)
        if match: 
            self.emoji_name, self.emoji_id = match.group(1), match.group(2)
        try:
            self.emoji_id = int(self.emoji_id)
            self.emoji_url = f"https://cdn.discordapp.com/emojis/{self.emoji_id}.png"
        except:
            raise commands.UserInputError("Passed string was not an emoji.")