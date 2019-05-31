import os
import logging

import telebot
from telebot import types

from end import cl_func as to_db

"""
documentation:
https://pypi.org/project/pyTelegramBotAPI/
https://habr.com/ru/post/442800/
"""


PATH_TO_TOKEN = '/Users/owl/Pycharm/PycharmProjects/im_last_bot/tiny_client/bot_token.txt'


if __name__ == '__main__':
    PATH_TO_LOG = '/Users/owl/Pycharm/PycharmProjects/im_last_bot/files/test.log'
    OVERWRITE_LOG = False
    PATH_TO_DB = '/Users/owl/Pycharm/PycharmProjects/im_last_bot/files/test.db'
    OVERWRITE_BASE = False
    SECRET_WORD = '123'

    SECRET_USERS = list()

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
        except FileNotFoundError:
            pass
    to_db.start_defaullt(PATH_TO_DB)
    logging.info('Database connected.')

    logging.info('Program start.')


token_file = open(PATH_TO_TOKEN, 'r')
token = token_file.read()

bot = telebot.TeleBot(token)


@bot.message_handler(commands=[
    'start', 'help', 'reg', 'count', 'reason', 'game', 'word', 'get_all',
    'go_away', 'next_user', 'stop', 'get_user', 'send_message', 'send_message_all'
])
def start_help(message):
    logging.info('User {0} (user id is {1}) send {2}.'.format(
        'None' if message.from_user.username is None else message.from_user.username,
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
        count_before_i = to_db.count_before(id_tg_user=message.from_user.id, path=PATH_TO_DB)
        prev_user_raw = to_db.prev_client(id_tg_user=message.from_user.id, path=PATH_TO_DB)
        prev_user = '{0} (@{1})'.format(prev_user_raw[2], prev_user_raw[3])
        to_send = 'Перед вами {0} человек в очереди.\nПредыдущий товарищ - {1}.'.format(count_before_i, prev_user)
        bot.send_message(message.from_user.id, to_send)
        pass
    elif message.text == '/word':
        to_send = 'Введите секретное слово.'
        bot.send_message(message.from_user.id, to_send)
        bot.register_next_step_handler(message, check_secret)
    elif message.text == '/reason':
        send_message = 'Укажите причину для посещения.'
        bot.send_message(message.from_user.id, send_message)
        bot.register_next_step_handler(message, reason)
    elif message.text == '/game':
        # send_message = 'Если вы видите это сообщение, а не игру, значит кое-кто кое-что так и не сделал.'
        send_message = 'Вы можете сыграть в игру перейдя по ссылке:\nhttps://biggest-brother.github.io/'
        bot.send_message(message.from_user.id, send_message)

    elif message.text == '/get_all' and message.from_user.id in SECRET_USERS:
        all_users = to_db.all_client(PATH_TO_DB)
        regular_row = '{0} пользователь (@{1}) хочет попасть к вам по причине {2}.\n'
        all_rows = 'Список всех пользователей в порядке очередности:\n'
        for user in all_users:
            all_rows += regular_row.format(
                user[2], user[3], user[5]
            )
        bot.send_message(message.from_user.id, all_rows)
    elif message.text == '/go_away' and message.from_user.id in SECRET_USERS:
        for user in to_db.all_client(PATH_TO_DB):
            send_message = 'На сегодня прием окончен.'
            try:
                bot.send_message(user[0], send_message)
            except telebot.apihelper.ApiException:
                pass
        bot.send_message(message.from_user.id, 'Очередь успешно распущена.')
        to_db.drop_all_cl(PATH_TO_DB)
    elif message.text == '/next_user' and message.from_user.id in SECRET_USERS:
        # TODO: change status this user and send message to next user
        # TODO: test it
        all_users = to_db.all_client(PATH_TO_DB)
        keyboard = types.InlineKeyboardMarkup()
        for user in all_users:
            face_button = '{0} пользователь хочет попасть к вам по причине {1}.'.format(
                user[2], user[5]
            )
            keyboard.add(types.InlineKeyboardButton(text=face_button, callback_data=user[0]))
        send_message = 'Выберите пользователя:'
        bot.send_message(message.from_user.id, text=send_message, reply_markup=keyboard)
        pass
    elif message.text == '/stop' and message.from_user.id in SECRET_USERS:
        # TODO: change status this user
        pass
    elif message.text == '/get_user' and message.from_user.id in SECRET_USERS:
        # TODO: send message to next user
        pass
    elif message.text == '/send_message' and message.from_user.id in SECRET_USERS:
        #
        pass
    elif message.text == '/send_message_all' and message.from_user.id in SECRET_USERS:
        pass


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    logging.info('Catch message: {}.'.format(message))
    # print(message.text)
    bot.send_message(message.from_user.id, 'Я поймал какое-то ваше сообщение. '
                                           'Не волнуйтесь, все будет записано.\n/help для помощи.')


def check_secret(message):
    if message.text == SECRET_WORD:
        send_text = 'Отлично, вам доступны новые команды. Воспользуйтесь командой /help.'
        SECRET_USERS.append(message.from_user.id)
        to_db.drop_client_tg_id(message.from_user.id, PATH_TO_DB)
        bot.send_message(message.from_user.id, send_text)
    else:
        send_text = 'Неправильный секрет.'
        bot.send_message(message.from_user.id, send_text)
    pass


def pre_get_name(message):
    if message.from_user.id in SECRET_USERS:
        to_send = 'Вы авторизованы как "супер-пользователь". ' \
                  'Пожалуйста, не вносите сумятицу в очередь своим появлением.'
        bot.send_message(message.from_user.id, to_send)
        return 0
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
    tg_name = 'None' if message.from_user.username is None else message.from_user.username

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
    print('u a here')
    user_id = message.from_user.id
    name = to_db.select_cl_id_tg(user_id, PATH_TO_DB)[2]
    user_reason = message.text

    markup = types.ReplyKeyboardMarkup(row_width=2)
    call_yes = types.KeyboardButton('Да')
    call_no = types.KeyboardButton('Нет')
    markup.add(call_yes, call_no)

    print(message.from_user.id, user_reason)
    to_db.upd_message(
        id_tg=message.from_user.id,
        msg=user_reason,
        path=PATH_TO_DB
    )

    to_send = '''Проверьте введенные данные:\nВас зовут:\n{0}
    \nПричина посещения:\n{1}'''.format(name, user_reason)
    bot.send_message(message.from_user.id, to_send, reply_markup=markup)
    bot.register_next_step_handler(message, check_reason)


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
    all_users = to_db.all_client(PATH_TO_DB)
    for user in all_users:
        if user[0] == call.data:
            send_message = 'Заходите в кабинет.'
            bot.send_message(user[0], send_message)


bot.polling(none_stop=False, interval=0)
