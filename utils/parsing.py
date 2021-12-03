import re, os 

#######CHECK PARSING#######

def is_hex(string: str):
    '''Checks if a string is a hex value
    '''
    match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', string)
    if match:
        return True
    else:
        return False

def hex_to_rgb(hex: str):
    '''Converts a hex value to rgb
    '''
    if hex[0] == "#":
        hex = hex.lstrip('#')
    lv = len(hex)
    return tuple(int(hex[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

#######CONVERT CHECK#######

def endswith_iter(val: list, tmp: str):
    '''Checks if the specifed list of values end on a string
    '''
    for x in val:
        if tmp.lower().endswith(x):
            return True
    return False

def remove_file(path: str):
    '''Removes from specified file path
    '''
    if os.path.exists(path):
        os.remove(path)
    else:
        return

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