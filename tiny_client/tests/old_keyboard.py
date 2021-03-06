import os
import logging

import telebot
from telebot import types

from end import cl_func as to_db

"""
documentation:
https://pypi.org/project/pyTelegramBotAPI/
"""


PATH_TO_TOKEN = '/Users/owl/Pycharm/PycharmProjects/im_last_bot/tiny_client/bot_token.txt'
PATH_TO_LOG = '/Users/owl/Pycharm/PycharmProjects/im_last_bot/files/test.log'
OVERWRITE_LOG = False
PATH_TO_DB = '/Users/owl/Pycharm/PycharmProjects/im_last_bot/files/test.db'
OVERWRITE_BASE = True


token_file = open(PATH_TO_TOKEN, 'r')
token = token_file.read()

if OVERWRITE_LOG:
    try:
        os.remove(PATH_TO_LOG)
    except FileNotFoundError:
        pass

if OVERWRITE_BASE:
    try:
        os.remove(PATH_TO_DB)
    except FileNotFoundError:
        pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)s] [%(funcName)s] [%(levelname)s]  %(message)s",
    handlers=[
        logging.FileHandler(PATH_TO_LOG),
        logging.StreamHandler()
    ])

logging.info('Program start.')


to_db.start_defaullt(PATH_TO_DB)
logging.info('Database connected.')

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help', 'reg', 'count', 'word'])
def start_help(message):
    logging.info('User {0} (user id is {1}) send {2}.'.format(
        '@' + message.from_user.username,
        message.from_user.id,
        message.text
    ))
    if message.text == '/start':
        to_send = 'Доброго времени суток.\nДля продолжения работы Вам необходимо зарегистрироваться.' + \
                  '\nДля этого используйте команду /reg.'
        # bot.send_message(message.from_user.id, 'first message')
        bot.reply_to(message, to_send)
    elif message.text == '/help':
        to_send = 'Доступные команды:\n' \
                  '\t/help - вывод меню помощи;\n' \
                  '\t/reg - регистрация нового пользователя;\n' \
                  '\t/count - узнать свое место в очереди и ближайших соседей;\n' \
                  '\t/word - ввод секретного слова.\n'
        bot.send_message(message.from_user.id, to_send)
    elif message.text == '/reg':
        pre_get_name(message=message)
    elif message.text == '/count':
        # TODO: сколько человек до тебя в очереди, предыдущий
        pass
    elif message.text == '/word':
        to_send = 'Введите секретное слово.'
        bot.send_message(message.from_user.id, to_send)
        # bot.register_next_step_handler(message, FUNC_NAME)
        # TODO: add secret word


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    logging.info('Catch message: {}.'.format(message))
    # print(message.text)
    bot.send_message(message.from_user.id, 'lost.')

    # if message.text == '/reg':
    #     bot.send_message(message.from_user.id, 'Представтесь.\nИмя увидит преподаватель, выбирайте мудро.')
    #     bot.register_next_step_handler(message, get_name)


def pre_get_name(message):
    to_send = 'Вы выбрали регистрацию.\nПожалуйста, укажите имя. ' \
              'Выбирайте мудро, так как вы будете видны под этим именем окружающим.'
    bot.send_message(message.from_user.id, to_send)
    print(message)
    bot.register_next_step_handler(message, get_name)


def get_name(message):
    global PATH_TO_DB
    name = message.text
    # to_send = 'Вас зовут {0}, верно?\n' \
    #           'Если да, то нажмите /yes, иначе /no.'.format(name)
    to_send = 'Вас зовут {0}, верно?'.format(name)
    # bot.reply_to(message, message=to_send)

    # TODO: add user id and name in base primary key id
    user_id = message.from_user.id
    tg_name = message.chat.username

    logging.info('Try add user {0} into DB.'.format(user_id))
    check_exist = to_db.registr(
        path=PATH_TO_DB, id_tg_user=user_id, nickname=name, tgname=tg_name
    )

    # keyboard = telebot.types.InlineKeyboardMarkup()
    # key_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data='get_name_yes')
    # key_no = telebot.types.InlineKeyboardButton(text='Нет', callback_data='get_name_no')
    # keyboard.add(key_yes, key_no)
    #
    # # bot.send_message(message.from_user.id, to_send)
    # # bot.register_next_step_handler(message, check_name)

    if check_exist:
        logging.info('User {0} added into DB.'.format(user_id))
        # bot.send_message(message.from_user.id, to_send, reply_markup=keyboard)
    else:
        logging.info('User {0} exist into DB.'.format(user_id))
        bot.send_message(message.from_user.id, 'От вашего аккаунта в базе уже есть запись...')

    markup = types.ReplyKeyboardMarkup(row_width=2)
    call_yes = types.KeyboardButton('Да')
    call_no = types.KeyboardButton('Нет')
    markup.add(call_yes, call_no)
    bot.send_message(message.from_user.id, "Вас зовут {0}, верно?".format(name), reply_markup=markup)
    bot.register_next_step_handler(message, pre_reason)
    # markup = types.ReplyKeyboardRemove(selective=False)
    # bot.send_message(message.from_user.id, message, reply_markup=markup)


def pre_reason(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    # bot.send_message(message.from_user.id, 'Немного магии: прячу клавиатуру.', reply_markup=markup)
    if message.text == 'Да':
        text_message = 'Укажите причину для посещения.'
        print(text_message)
        bot.send_message(message.from_user.id, text_message, reply_markup=markup)
        bot.register_next_step_handler(message, reason)
    elif message.text == 'Нет':
        text_message = 'Жаль. Введите имя еще раз.'
        bot.send_message(message.from_user.id, text_message, reply_markup=markup)
        bot.register_next_step_handler(message, get_name)
    else:
        text_message = 'Я вас не понимаю. Воспользуйтесь справкой.'
        print(text_message)
        bot.send_message(message.from_user.id, text_message, reply_markup=markup)
    pass


def reason(message):
    # TODO: get user info from DB by user_tg_id
    # to_base(user_tg_id) -> name
    print('u a here')
    name = 'A'
    user_reason = message.text
    bot.send_message(message.from_user.id, '#TEST\nотлично. но у нас нет связи с внутренней логикой, поэтому...')

    keyboard = telebot.types.InlineKeyboardMarkup()
    key_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data='reason_successful_register')
    key_no = telebot.types.InlineKeyboardButton(text='Нет', callback_data='reason_register_failed')
    keyboard.add(key_yes, key_no)

    to_send = '''Проверьте введенные данные:\nВас зовут:\n{0}\nПричина посещения:\n{1}'''.format(name, user_reason)
    bot.send_message(message.from_user.id, to_send, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "reason_successful_register":
        bot.send_message(call.message.chat.id, 'Добавляю в очередь.')
        # TODO: update user info by id
        # to_base(user_id, reason) -> True/False
        # to_base(call.message.from_user.id, reason???)
    elif call.data == "reason_register_failed":
        bot.send_message(call.message.chat.id, 'Тогда начнем сначала.')
        # TODO: delete all user info by id
        # to_base(user_id) -> True/False

    # register:
    elif call.data == 'get_name_yes':
        print(call.message)
        bot.register_next_step_handler(call.message, pre_reason)
        pass
    elif call.data == 'get_name_no':
        # bot.send_message(call.message.chat.id, 'Введите имя.')
        bot.register_next_step_handler(call.message, reason)


bot.polling(none_stop=False, interval=0)
