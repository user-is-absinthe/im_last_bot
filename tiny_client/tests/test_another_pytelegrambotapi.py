import os
import logging

import telebot

from end import cl_func as to_db


PATH_TO_TOKEN = '/Users/owl/Pycharm/PycharmProjects/im_last_bot/tiny_client/bot_token.txt'
PATH_TO_LOG = '/Users/owl/Pycharm/PycharmProjects/im_last_bot/files/test.log'
OVERWRITE_LOG = False
PATH_TO_DB = '/Users/owl/Pycharm/PycharmProjects/im_last_bot/files/test.db'

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

logging.info('Program start.')

to_db.start_defaullt()

bot = telebot.TeleBot(token)

# telebot.apihelper.proxy = {
#     # 'https': 'socks5h://user:pass@ip',
#     'https': 'socks5://user:pass@ip'
# }


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
        to_send = 'Вы выбрали регистрацию.\nПожалуйста, укажите имя. ' \
                  'Выбирайте мудро, так как вы будете видны под этим именем окружающим.'
        bot.send_message(message.from_user.id, to_send)
        # bot.reply_to(message, to_send)
        bot.register_next_step_handler(message, get_name)
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
    bot.send_message(message.from_user.id, 'Для регистрации введите команду /reg.')

    # if message.text == '/reg':
    #     bot.send_message(message.from_user.id, 'Представтесь.\nИмя увидит преподаватель, выбирайте мудро.')
    #     bot.register_next_step_handler(message, get_name)


def get_name(message):
    name = message.text
    to_send = 'Вас зовут {0}, верно?\n' \
              'Если да, то нажмите /yes, иначе /no.'.format(name)
    # bot.reply_to(message, message=to_send)
    bot.send_message(message.from_user.id, to_send)
    bot.register_next_step_handler(message, check_name)


def check_name(message):
    if message.text == '/yes':
        # TODO: add user id and name in base primary key id
        # to_base(user_tg_id, user_chat_id, name) -> return true/false
        bot.send_message(message.from_user.id, 'Укажите причину для посещения.')
        bot.register_next_step_handler(message, reason)
    elif message.text == '/no':
        bot.send_message(message.from_user.id, 'Введите еще раз.')
        bot.register_next_step_handler(message, get_name)


def reason(message):
    # TODO: get user info from DB by user_tg_id
    # to_base(user_tg_id) -> name
    name = 'A'
    user_reason = message.text
    bot.send_message(message.from_user.id, '#TEST\nотлично. но у нас нет связи с внутренней логикой, поэтому...')

    keyboard = telebot.types.InlineKeyboardMarkup()
    key_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data='successful_register')
    key_no = telebot.types.InlineKeyboardButton(text='Нет', callback_data='register_failed')
    keyboard.add(key_yes, key_no)

    to_send = '''Проверьте введенные данные:\nВас зовут:\n{0}\nПричина посещения:\n{1}'''.format(name, user_reason)
    bot.send_message(message.from_user.id, to_send, reply_markup=keyboard)


def to_get_in_line(message):
    # TODO: update user info by id
    # to_base(user_id, reason) -> True/False
    bot.send_message()
    pass


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "successful_register":
        bot.send_message(call.message.chat.id, 'Добавляю в очередь.')
        # TODO: update user info by id
        # to_base(user_id, reason) -> True/False
        # to_base(call.message.from_user.id, reason???)
    elif call.data == "register_failed":
        bot.send_message(call.message.chat.id, 'Тогда начнем сначала.')
        # TODO: delete all user info by id
        # to_base(user_id) -> True/False


bot.polling(none_stop=True, interval=0)
