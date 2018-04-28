import telebot
import json
from pymorphy2 import MorphAnalyzer
from time import time, sleep
import logging

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from painter import check_days, draw, get_text, get_day


# telebot.apihelper.proxy = {
#     'https': 'socks5://proxy:e9eM04JNIEZ2@81.2.240.15:1337'}


with open('data.json', 'r') as file:
    data = json.load(file)

parsed_word = None
bot = telebot.TeleBot(data['bot_token'])
logging.basicConfig(
    format='%(filename)s:%(lineno)d# %(levelname)-8s [%(asctime)s]  %(message)s',
    level=logging.INFO)


@bot.message_handler(commands=['start'])
def send_start(message):
    text = open(data['start_message_path'], 'r').read()
    try:
        bot.send_message(message.chat.id, text,
                         reply_to_message_id=message.message_id)
    except Exception as exception:
        logging.error(exception)


@bot.message_handler(commands=['get_meme'])
def send_meme(message):
    try:
        bot.send_chat_action(message.chat.id, 'upload_photo')
        bot.send_photo(message.chat.id, data['last_file_id'],
                       reply_to_message_id=message.message_id)
        logging.info('Meme sent')
    except Exception as exception:
        logging.error(exception)
        text = open(data['error_message_path'], 'r').read()
        try:
            bot.send_message(message.chat.id, text)
        except Exception as exception:
            logging.error(exception)


def morph_word():
    global parsed_word
    morph = MorphAnalyzer()
    parsed_word = morph.parse(data['word'])[0]


def update_picture(*messages):
    now_time = time()
    if check_days(data['last_time'], now_time):
        return

    logging.info('Picture started to update')
    draw(data['in_picture_path'], data['out_picture_path'],
         data['fonts_path'],
         data['to_time'],
         data['text_x'], data['text_y'],
         data['font_size'],
         parsed_word)

    logging.info('Picture updated')

    try:
        bot.send_chat_action(data['storage_chat_id'], 'upload_photo')
    except Exception as exception:
        logging.error(exception)

    with open(data['out_picture_path'], 'rb') as img:
        request = bot.send_photo(data['storage_chat_id'], img)
        data['last_file_id'] = request.photo[-1].file_id
        data['last_time'] = now_time
        logging.info('Picture loaded')

    with open('data.json', 'w') as file:
        json.dump(data, file)


bot.set_update_listener(update_picture)

if __name__ == '__main__':
    logging.info('Launching')
    morph_word()
    logging.info('Word parsed')

    logging.info('Word examples: {}'.format(
        ', '.join([get_text(i, parsed_word) for i in range(12)])))

    while True:
        try:
            bot.polling(True)
        except Exception as exception:
            logging.error(exception)
            sleep(5)
