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
SECRET_WORD = '123'


SECRET_USERS = list()


token_file = open(PATH_TO_TOKEN, 'r')
token = token_file.read()

if OVERWRITE_LOG:
    try:
        os.remove(PATH_TO_LOG)
    except FileNotFoundError:
        pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)s] [%(funcName)s] [%(levelname)s]  %(message)s",
    handlers=[
        logging.FileHandler(PATH_TO_LOG),
        logging.StreamHandler()
    ])

if OVERWRITE_BASE:
    try:
        os.remove(PATH_TO_DB)
        to_db.start_defaullt(PATH_TO_DB)
    except FileNotFoundError:
        pass

logging.info('Database connected.')

logging.info('Program start.')

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
        to_send = 'Обычные команды:\n' \
                  '\t/help - вывод меню помощи\n' \
                  '\t/reg - регистрация нового пользователя\n' \
                  '\t/count - узнать свое место в очереди и ближайших соседей\n' \
                  '\t/word - ввод секретного слова\n' \
                  '\t/reason - уточнить причину посещения\n' \
                  '\t/game - поиграть в игрушку\n'
        if message.from_user.id in SECRET_USERS:
            special = '\nСпециальные команды:\n' \
                      '\t/get_all - показать всех пользователей;\n' \
                      '\t/go_away - распустить очередь:\n' \
                      '\t/new_secret - установить новое секретное слово\n' \
                      '\t/next_user - вызвать следующего по очереди пользователя\n' \
                      '\t/stop - приостновить прием\n' \
                      '\t/get_user - вызвать конкретного пользователя\n' \
                      '\t/send_message - отправить сообщение конкретному пользователю\n' \
                      '\t/send_message_all - отправить сообщение всем\n'
            to_send += special
        bot.send_message(message.from_user.id, to_send)

    elif message.text == '/reg':
        pre_get_name(message=message)
    elif message.text == '/count':
        # TODO: сколько человек до тебя в очереди, предыдущий
        print('amkd')
        count_before_i = to_db.count_before_id(id_tg_user=message.from_user.id, path=PATH_TO_DB)
        prev_user = to_db.prev_client(me_num=message.from_user.id, path=PATH_TO_DB)
        print(count_before_i)
        print(prev_user)
        to_send = 'Перед вами {0} человек в очереди.\nПредыдущий товарищ {1}.'
        bot.send_message(message.from_user.id, to_send)
        pass
    elif message.text == '/word':
        to_send = 'Введите секретное слово.'
        bot.send_message(message.from_user.id, to_send)
        bot.register_next_step_handler(message, check_secret)
        # TODO: add secret word
    elif message.text == '/reason':
        send_message = 'Укажите причину для посещения.'
        bot.send_message(message.from_user.id, send_message)
        bot.register_next_step_handler(message, reason)

    # TODO: fix special func
    elif message.text == '/get_all' and message.from_user.id in SECRET_USERS:
        print('awdjbl')
        pass
    elif message.text == '/go_away' and message.from_user.id in SECRET_USERS:
        pass
    elif message.text == '/new_secret' and message.from_user.id in SECRET_USERS:
        pass
    elif message.text == '/next_user' and message.from_user.id in SECRET_USERS:
        pass
    elif message.text == '/stop' and message.from_user.id in SECRET_USERS:
        pass
    elif message.text == '/get_user' and message.from_user.id in SECRET_USERS:
        pass
    elif message.text == '/send_message' and message.from_user.id in SECRET_USERS:
        pass

        pass


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    logging.info('Catch message: {}.'.format(message))
    # print(message.text)
    bot.send_message(message.from_user.id, 'catch')

    # if message.text == '/reg':
    #     bot.send_message(message.from_user.id, 'Представтесь.\nИмя увидит преподаватель, выбирайте мудро.')
    #     bot.register_next_step_handler(message, get_name)


def check_secret(message):
    if message.text == SECRET_WORD:
        send_text = 'Отлично, вам доступны новые команды. Воспользуйтесь командой /help.'
        SECRET_USERS.append(message.from_user.id)
        bot.send_message(message.from_user.id, send_text)
    else:
        send_text = 'Неправильный секрет.'
        bot.send_message(message.from_user.id, send_text)
    pass


def pre_get_name(message):
    to_send = 'Вы выбрали регистрацию.\nПожалуйста, укажите имя. ' \
              'Выбирайте мудро, так как вы будете видны под этим именем окружающим.'
    bot.send_message(message.from_user.id, to_send)
    print(message)
    bot.register_next_step_handler(message, get_name)


def get_name(message):
    global PATH_TO_DB
    name = message.text

    # TODO: add user id and name in base primary key id
    user_id = message.from_user.id
    tg_name = message.chat.username

    logging.info('Try add user {0} into DB.'.format(user_id))
    check_exist = to_db.registr(
        path=PATH_TO_DB, id_tg_user=user_id, nickname=name, tgname=tg_name
    )

    if check_exist:
        logging.info('User {0} added into DB.'.format(user_id))

        markup = types.ReplyKeyboardMarkup(row_width=2)
        call_yes = types.KeyboardButton('Да')
        call_no = types.KeyboardButton('Нет')
        markup.add(call_yes, call_no)
        bot.send_message(message.from_user.id, "Вас зовут {0}, верно?".format(name), reply_markup=markup)
        bot.register_next_step_handler(message, pre_reason)
    else:
        logging.info('User {0} exist into DB.'.format(user_id))
        send_message = 'От вашего аккаунта в базе уже есть запись. 🧐\n' \
                       'Укажите причину для посещения.'
        bot.send_message(message.from_user.id, send_message)
        bot.register_next_step_handler(message, reason)


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
        text_message = 'Я вас не понимаю. Воспользуйтесь справкой.\n/help'
        print(text_message)
        bot.send_message(message.from_user.id, text_message, reply_markup=markup)
    pass


def reason(message):
    global PATH_TO_DB
    # TODO: get user info from DB by user_tg_id
    # to_base(user_tg_id) -> name
    print('u a here')
    user_id = message.from_user.id
    # name = 'A'
    name = to_db.select_cl_id_tg(user_id, PATH_TO_DB)
    user_reason = message.text
    # bot.send_message(message.from_user.id, '#TEST\nотлично. но у нас нет связи с внутренней логикой, поэтому...')

    markup = types.ReplyKeyboardMarkup(row_width=2)
    call_yes = types.KeyboardButton('Да')
    call_no = types.KeyboardButton('Нет')
    markup.add(call_yes, call_no)
    # bot.send_message(message.from_user.id, "Причина посещения:\n{0}\nВсе так?".format(name), reply_markup=markup)
    # bot.register_next_step_handler(message, pre_reason)

    print(message.from_user.id, user_reason)
    to_db.upd_message(
        id_tg=message.from_user.id,
        msg=user_reason,
        path=PATH_TO_DB
    )

    to_send = '''Проверьте введенные данные:\nВас зовут:\n{0}
    \nПричина посещения:\n{1}'''.format(name, user_reason)
    bot.send_message(message.from_user.id, to_send, reply_markup=markup)
    bot.register_next_step_handler(message, pre_reason)


def check_reason(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    if message.text == 'Да':
        text_message = 'Отлично, вы добавлены в базу.'
        bot.send_message(message.from_user.id, text_message, reply_markup=markup)
        pass
    elif message.text == 'Нет':
        text_message = 'Тогда начнем сначала.'
        bot.send_message(message.from_user.id, text_message, reply_markup=markup)
        bot.register_next_step_handler(message, pre_get_name)
    else:
        text_message = 'Я вас не понимаю. Воспользуйтесь справкой.\n/help'
        bot.send_message(message.from_user.id, text_message, reply_markup=markup)
    pass


def random_message(id_tg_user, text_message):
    bot.send_message(id_tg_user, text_message)


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
