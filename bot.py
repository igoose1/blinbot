import telebot
import json
from pymorphy2 import MorphAnalyzer
from time import sleep
from datetime import datetime
import logging

from painter import check_days, draw, get_text, get_days


telebot.apihelper.proxy = {
    'https': 'socks5://proxy:e9eM04JNIEZ2@81.2.240.15:1337'}


with open('data.json', 'r') as file:
    data = json.load(file)

parsed_word = None
bot = telebot.TeleBot(data['telegram']['token'])
logging.basicConfig(
    format='%(filename)s:%(lineno)d# %(levelname)-8s [%(asctime)s]  %(message)s',
    level=logging.INFO)


@bot.message_handler(commands=['start', 'help'])
def send_start(message):
    try:
        text = open(data['message_path']['start'], 'r').read()
        bot.send_message(message.chat.id, text,
                         reply_to_message_id=message.message_id)
    except Exception as exception:
        logging.error(exception)


@bot.message_handler(commands=['get_meme'])
def send_meme(message):
    try:
        bot.send_chat_action(message.chat.id, 'upload_photo')
        bot.send_photo(message.chat.id, data['last']['file_id'],
                       reply_to_message_id=message.message_id)
        logging.info('Meme sent')
    except Exception as exception:
        logging.error(exception)
        try:
            text = open(data['message_path']['error'], 'r').read()
            bot.send_message(message.chat.id, text)
        except Exception as exception:
            logging.error(exception)


@bot.message_handler(commands=['source'])
def send_start(message):
    try:
        text = open(data['message_path']['source'], 'r').read()
        bot.send_message(message.chat.id, text,
                         reply_to_message_id=message.message_id)
    except Exception as exception:
        logging.error(exception)


def morph_word():
    global parsed_word
    morph = MorphAnalyzer()
    parsed_word = morph.parse(data['text']['word'])[0]


def update_picture(*messages):
    now_time = datetime.now().timestamp()
    if check_days(data['last']['day'], data['to_time'], now_time):
        return

    logging.info('Picture started to update')
    draw(data['picture_path']['in'], data['picture_path']['out'],
         data['text']['font']['path'],
         data['to_time'],
         data['text']['coordinate']['x'], data['text']['coordinate']['y'],
         data['text']['font']['size'],
         data['text']['format'],
         parsed_word)

    logging.info('Picture updated')

    try:
        bot.send_chat_action(data['telegram']['storage_chat_id'], 'upload_photo')
    except Exception as exception:
        logging.error(exception)

    try:
        img = open(data['picture_path']['out'], 'rb')
        request = bot.send_photo(data['telegram']['storage_chat_id'], img)
        data['last']['file_id'] = request.photo[-1].file_id
        data['last']['day'] = get_days(data['to_time'], now_time)
        logging.info('Picture loaded')
    except Exception as exception:
        logging.error(exception)

    with open('data.json', 'w') as file:
        json.dump(data, file, indent=2, sort_keys=True)


bot.set_update_listener(update_picture)

if __name__ == '__main__':
    logging.info('Launching')
    morph_word()
    logging.info('Word parsed')

    logging.info('Word examples: {}'.format(
        ', '.join([get_text(i, parsed_word, data['text']['format'])
                   for i in range(12)])))

    while True:
        try:
            bot.polling(True)
        except Exception as exception:
            logging.error(exception)
            sleep(5)
