from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from time import time
import random


def get_colour(days):
    random.seed(days)
    # colour = random.choice(["red",
    #                         "green",
    #                         "blue",
    #                         "orange",
    #                         "purple",
    #                         "pink",
    #                         "yellow"])

    colour = '#%06x' % random.randint(0, 0xFFFFFF)
    return colour


def get_day(time=time()):
    return time // (60 * 60 * 24)


def get_days(to_time, from_time=time()):
    difference_time = get_day(to_time) - get_day(from_time)
    return int(difference_time)


def check_days(last_time, now_time=time()):
    return get_day(last_time) == get_day(now_time)


def get_text(days, parsed_word):
    try:
        word = parsed_word.make_agree_with_number(abs(days)).word
    except:
        word = parsed_word.word

    return '{} {}'.format(days, word)


def draw(in_file_path, out_file_path, font_file, to_time, x, y, size, parsed_word):
    img = Image.open(in_file_path)
    drw = ImageDraw.Draw(img)

    font = ImageFont.truetype(font_file, size)

    days = get_days(to_time)
    text = get_text(days, parsed_word)
    drw.text((x, y), text, get_colour(days), font=font)

    img.save(out_file_path)
