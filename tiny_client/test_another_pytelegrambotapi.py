import os
import logging

import telebot


PATH_TO_TOKEN = 'bot_token.txt'
PATH_TO_LOG = '/Users/owl/Pycharm/PycharmProjects/im_last_bot/tiny_client/test_log.log'
OVERWRITE_LOG = True

token_file = open(PATH_TO_TOKEN, 'r')
token = token_file.read()

if OVERWRITE_LOG:
    try:
        os.remove(PATH_TO_LOG)
    except FileNotFoundError:
        pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)s] [%(levelname)s]  %(message)s",
    handlers=[
        logging.FileHandler(PATH_TO_LOG),
        logging.StreamHandler()
    ])

logging.info('Program start.')

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help', 'reg', 'count', 'word'])
def start_help(message):
    if message.text == '/start':
        to_send = ''
        # bot.send_message(message.from_user.id, 'first message')
        bot.reply_to(message, "first msg")
    elif message.text == '/help':
        # TODO: описание команд
        to_send = ''
        bot.send_message(message.from_user.id, 'help')
    elif message.text == '/reg':
        to_send = 'Вы выбрали регистрацию.\nВведите имя. Выбирайте мудро.'
        bot.send_message(message.from_user.id, to_send)
        bot.register_next_step_handler(message, get_name)
    elif message.text == '/count':
        # сколько человек до тебя в очереди, предыдущий
        pass
    elif message.text == '/word':
        to_send = ''
        bot.send_message(message.from_user.id, to_send)
        # bot.register_next_step_handler(message, FUNC_NAME)


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    logging.info('Catch message: {}.'.format(message))
    # print(message.text)
    bot.send_message(message.from_user.id, 'Для регистрации введите команду /reg.')

    if message.text == '/reg':
        bot.send_message(message.from_user.id, 'Представтесь, пожалуйста.\nИмя увидит преподаватель, выбирайте мудро.')
        bot.register_next_step_handler(message, get_name)


def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Укажите причину для посещения.')
    bot.register_next_step_handler(message, reason)


def reason(message):
    global user_reason
    user_reason = message.text
    bot.send_message(message.from_user.id, 'отлично. но у нас нет связи с внутренней логикой, поэтому...')

    keyboard = telebot.types.InlineKeyboardMarkup()
    key_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data='yes')
    key_no = telebot.types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_yes, key_no)

    to_send = '''Проверьте введенные данные:\n{0}\nПричина посещения:\n{1}'''.format(name, user_reason)
    bot.send_message(message.from_user.id, to_send, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Добавляю в очередь.')

    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Тогда начнем сначала.')


bot.polling(none_stop=True, interval=0)
