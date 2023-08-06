from os import environ
from platform import uname
from enum import Enum
from typing import Union

class colours(Enum):
    black = 0
    red = 1
    green = 2
    yellow = 3
    blue = 4
    magenta = 5
    cyan = 6
    white = 7
    none = 9

class styles(Enum):
    none = 0
    bright = 1
    dim = 2
    italic = 3
    underline = 4
    slow_blink = 5
    fast_blink = 6
    invert = 7
    hide = 8
    strikethrough = 9
    double_underline = 21
    overline = 53

class settings:
    force_colours = False

class __config:
    escape_start = "\033[0;"
    escape_end = "m"

    colour_prefix = {
        "foreground": 3,
        "background": 4
    }

    colour_suffix = {
        "black": 0,
        "red": 1,
        "green": 2,
        "yellow": 3,
        "blue": 4,
        "magenta": 5,
        "cyan": 6,
        "white": 7,
        "none": 9,
    }

    style_prefix = {
        "none": 0,
        "bright": 1,
        "dim": 2,
        "italic": 3,
        "underline": 4,
        "slow blink": 5, 
        "fast blink": 6,
        "invert": 7,
        "hide": 8,
        "strikethrough": 9,
        "double underline": 21,
        "overline": 53,
    }

colour_list = []

def colour(text:str, foreground:Union[colours,str] = colours.none, background:Union[colours,str] = colours.none):
    if ("TERM" not in environ.keys() or uname().system == "Windows") and not settings.force_colours:
        return text

    foreground_num = __config.colour_suffix[foreground] if type(foreground) == str else foreground.value
    background_num = __config.colour_suffix[background] if type(background) == str else background.value
    
    if type(foreground) == str:
        if foreground not in __config.colour_suffix:
            raise TypeError(f"\"{foreground}\" is not a valid colour")
    else:
        if foreground not in colours:
            raise TypeError(f"\"{foreground.name}\" is not a valid colour")

    if type(background) == str:
        if background not in __config.colour_suffix:
            raise TypeError(f"\"{background}\" is not a valid colour")
    else:
        if background not in colours:
            raise TypeError(f"\"{background.name}\" is not a valid colour")
    
    prefix = f"{__config.escape_start}3{foreground_num};4{background_num}{__config.escape_end}"
    suffix = f"{__config.escape_start}39;49{__config.escape_end}"

    return f"{prefix}{text}{suffix}"

def style(text:str, style:Union[styles, str] = styles.none):
    if ("TERM" not in environ.keys() or uname().system == "Windows") and not settings.force_colours:
        return text

    style_num = __config.colour_suffix[style] if type(style) == str else style.value

    if type(style) == str:
        if style not in __config.style_prefix:
            raise TypeError(f"\"{style}\" is not a valid colour")
    else:
        if style not in styles:
            raise TypeError(f"\"{style.name}\" is not a valid colour")

    prefix = f"{__config.escape_start}{style_num}{__config.escape_end}"
    suffix = suffix = f"{__config.escape_start}0{__config.escape_end}"
    return f"{prefix}{text}{suffix}"

def colour_start(foreground:str = "none", background:str = "none"):
    colour_list.append([foreground, background, "none"])
    return f"{__config.escape_start}3{__config.colour_suffix[foreground]};4{__config.colour_suffix[background]}{__config.escape_end}"

def colour_end():
    global colour_list
    if len(colour_list) == 0:
        return
    
    if len(colour_list) == 1:
        colour_list = colour_list[0:-1]
        return f"{__config.escape_start}3{__config.colour_suffix['none']};4{__config.colour_suffix['none']}{__config.escape_end}"
    
    previous_colour = colour_list[-2]
    colour_list = colour_list[0:-1]
    if previous_colour[0] == "none" and previous_colour[1] == "none" and previous_colour[2] != ["none"]:
        return f"{__config.escape_start}{__config.style_prefix[previous_colour[2]]}{__config.escape_end}"

    return f"{__config.escape_start}3{__config.colour_suffix[previous_colour[0]]};4{__config.colour_suffix[previous_colour[1]]}{__config.escape_end}"

def style_start(style:str = "none"):
    colour_list.append(["none", "none", style])
    return f"{__config.escape_start}{__config.style_prefix[style]}{__config.escape_end}"

def style_end():
    return colour_end()

def help():
    print("Foreground Colours")
    for _colour in __config.colour_suffix:
        print("  \u21B3", f"\"{_colour}\"", "foreground: ", colour(_colour, foreground = _colour))

    print("Background Colours")
    for _colour in __config.colour_suffix:
        print("  \u21B3", f"\"{_colour}\"", "background: ", colour(_colour, background = _colour))

    print("Styles")
    for _style in __config.style_prefix:
        print("  \u21B3", f"\"{_style}\"", "style: ", style(_style, _style))