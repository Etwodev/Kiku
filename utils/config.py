import json
from collections import namedtuple
import os


def get(file: str):
    '''Seamlessly open any json files, used for configuration
    '''
    try:
        with open(file, encoding='utf8') as data:
            return json.load(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    except AttributeError:
        raise AttributeError("Unknown argument")
    except FileNotFoundError:
        raise FileNotFoundError("JSON file wasn't found")


def keys_exists(element, *keys):
    '''Check if a key exists in a dictionary
    '''
    if not isinstance(element, dict):
        raise AttributeError('keys_exists() expects dict as first argument.')
    if len(keys) == 0:
        raise AttributeError('keys_exists() expects at least two arguments, one given.')
    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return False
    return True


def remove_file(file: str, dir="tmp/"):
    '''Removes from specified file
    '''
    try:
        if file != "README.txt":
            os.remove(dir + file)
    except FileNotFoundError:
        raise FileNotFoundError("Specified file was not found")
    except PermissionError:
        raise PermissionError("Insufficient permissions to execute this process")