from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from datetime import datetime
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


def get_days(to_time, from_time=datetime.now().timestamp()):
    to_time_stamp = datetime.fromtimestamp(to_time)
    from_time_stamp = datetime.fromtimestamp(from_time)
    difference_time = to_time_stamp - from_time_stamp
    return difference_time.days


def check_days(last_day, to_time, now_time=datetime.now().timestamp()):
    return get_days(to_time, now_time) == last_day


def get_text(days, parsed_word, text_format):
    try:
        word = parsed_word.make_agree_with_number(abs(days)).word
    except:
        word = parsed_word.word

    return text_format.format(days, word)


def draw(in_file_path, out_file_path, font_file, to_time, x, y, size, text_format, parsed_word):
    img = Image.open(in_file_path)
    drw = ImageDraw.Draw(img)

    font = ImageFont.truetype(font_file, size)

    days = get_days(to_time)
    text = get_text(days, parsed_word, text_format)
    drw.text((x, y), text, get_colour(days), font=font)

    img.save(out_file_path)
